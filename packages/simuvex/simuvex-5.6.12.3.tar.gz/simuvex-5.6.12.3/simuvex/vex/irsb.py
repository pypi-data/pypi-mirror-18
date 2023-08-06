#!/usr/bin/env python
"""This module handles constraint generation for IRSBs."""

# because pylint can't load pyvex
# pylint: disable=F0401

import logging
l = logging.getLogger("simuvex.vex.irsb")
#l.setLevel(logging.DEBUG)

import pyvex
from ..s_run import SimRun


class IMark(object):
    """
    An IMark is an IR statement that indicates the address and length of the original instruction.
    """
    def __init__(self, i):
        self.addr = i.addr
        self.len = i.len

#pylint:disable=unidiomatic-typecheck


class SimIRSB(SimRun):
    """
    Symbolically parse a basic block.

    :ivar irsb:             The pyvex IRSB to parse.
    :ivar provided_state:   The symbolic state at the beginning of the block.
    :ivar id:               The ID of the basic block.
    :ivar whitelist:        A whitelist of the statements to execute. (default: all)
    :ivar last_stmt:        The statement to stop execution at.
    """

    def __init__(self, state, irsb, irsb_id=None, whitelist=None, last_stmt=None, force_bbl_addr=None, **kwargs):
        SimRun.__init__(self, state, **kwargs)

        if irsb.size == 0:
            raise SimIRSBError("Empty IRSB passed to SimIRSB.")

        self.irsb = irsb
        self.first_imark = IMark(next(i for i in self.irsb.statements if type(i) is pyvex.IRStmt.IMark))
        self.last_imark = self.first_imark
        self.state.scratch.bbl_addr = self.addr if force_bbl_addr is None else force_bbl_addr
        self.state.scratch.executed_block_count = 1
        self.state.sim_procedure = None
        self.id = "%x" % self.first_imark.addr if irsb_id is None else irsb_id
        self.whitelist = whitelist
        self.last_stmt = last_stmt
        self.default_exit_guard = self.state.se.true if last_stmt is None else self.state.se.false

        self.state._inspect('irsb', BP_BEFORE, address=self.addr)

        # this stuff will be filled out during the analysis
        self.num_stmts = 0
        self.next_expr = None
        self.statements = [ ]
        self.conditional_exits = [ ]
        self.default_exit = None
        self.postcall_exit = None
        self.has_default_exit = False

        if o.BLOCK_SCOPE_CONSTRAINTS in self.state.options and 'solver_engine' in self.state.plugins:
            self.state.release_plugin('solver_engine')

        try:
            self._handle_irsb()
        except SimError as e:
            e.record_state(self.state)
            raise

        # It's for debugging
        # irsb.pp()
        # if whitelist != None:
        #    print "======== whitelisted statements ========"
        #    pos = 0
        #    for s in self.statements:
        #        print "%d: " % whitelist[pos],
        #        s.stmt.pp()
        #        print ""
        #        pos += 1
        #    print "======== end ========"

        self.state._inspect('irsb', BP_AFTER)
        self.cleanup()

    def __repr__(self):
        return "<SimIRSB %s>" % self.id_str

    def _handle_irsb(self):
        if o.BREAK_SIRSB_START in self.state.options:
            import ipdb
            ipdb.set_trace()

        # finish the initial setup
        self._prepare_temps(self.state)

        # handle the statements
        try:
            self._handle_statements()
        except (SimSolverError, SimMemoryAddressError):
            l.warning("%s hit an error while analyzing statement %d", self, self.state.scratch.stmt_idx, exc_info=True)

        # some finalization
        self.num_stmts = len(self.irsb.statements)
        self.state.scratch.stmt_idx = self.num_stmts

        # If there was an error, and not all the statements were processed,
        # then this block does not have a default exit. This can happen if
        # the block has an unavoidable "conditional" exit or if there's a legitimate
        # error in the simulation
        self.default_exit = None
        if self.has_default_exit:
            l.debug("%s adding default exit.", self)

            try:
                self.next_expr = translate_expr(self.irsb.next, self.last_imark, self.num_stmts, self.state)

                self.state.log.extend_actions(self.next_expr.actions)

                if o.TRACK_JMP_ACTIONS in self.state.options:
                    target_ao = SimActionObject(self.next_expr.expr, reg_deps=self.next_expr.reg_deps(), tmp_deps=self.next_expr.tmp_deps())
                    self.state.log.add_action(SimActionExit(self.state, target_ao, exit_type=SimActionExit.DEFAULT))

                exit_ins_addr = self.state.scratch.last_ins_addr if self.state.arch.branch_delay_slot else \
                    self.state.scratch.ins_addr
                self.default_exit = self.add_successor(self.state, self.next_expr.expr, self.default_exit_guard,
                                                       self.irsb.jumpkind, exit_stmt_idx='default',
                                                       exit_ins_addr=exit_ins_addr
                                                       )

            except KeyError:
                # For some reason, the temporary variable that the successor relies on does not exist. It can be
                # intentional (e.g. when executing a program slice)
                # We save the current state anyways
                self.unsat_successors.append(self.state)
                self.default_exit = None

                l.debug("The temporary variable for default exit of %s is missing.", self)
        else:
            l.debug("%s has no default exit", self)

        # do return emulation and calless stuff
        successors = self.successors
        all_successors = self.successors + self.unsat_successors
        self.successors = [ ]
        for exit_state in successors:
            self.successors.append(exit_state)

        for exit_state in all_successors:
            exit_jumpkind = exit_state.scratch.jumpkind
            if exit_jumpkind is None: exit_jumpkind = ""

            if o.CALLLESS in self.state.options and exit_jumpkind == "Ijk_Call":
                exit_state.registers.store(exit_state.arch.ret_offset,
                                           exit_state.se.Unconstrained('fake_ret_value', exit_state.arch.bits))
                exit_state.scratch.target = exit_state.se.BVV(self.addr + self.irsb.size, exit_state.arch.bits)
                exit_state.scratch.jumpkind = "Ijk_Ret"
                exit_state.regs.ip = exit_state.scratch.target

            elif o.DO_RET_EMULATION in exit_state.options and \
                    (exit_jumpkind == "Ijk_Call" or exit_jumpkind.startswith('Ijk_Sys')):
                l.debug("%s adding postcall exit.", self)

                ret_state = exit_state.copy()
                guard = ret_state.se.true if o.TRUE_RET_EMULATION_GUARD in self.state.options else ret_state.se.false
                target = ret_state.se.BVV(self.addr + self.irsb.size, ret_state.arch.bits)
                if ret_state.arch.call_pushes_ret:
                    ret_state.regs.sp = ret_state.regs.sp + ret_state.arch.bytes
                exit_ins_addr = self.state.scratch.last_ins_addr if self.state.arch.branch_delay_slot else \
                    self.state.scratch.ins_addr
                self.add_successor(ret_state, target, guard, 'Ijk_FakeRet', exit_stmt_idx='default',
                                   exit_ins_addr=exit_ins_addr
                                   )

        if o.BREAK_SIRSB_END in self.state.options:
            import ipdb
            ipdb.set_trace()

    # This function receives an initial state and imark and processes a list of pyvex.IRStmts
    # It returns a final state, last imark, and a list of SimIRStmts
    def _handle_statements(self):
        # Translate all statements until something errors out
        stmts = self.irsb.statements

        skip_stmts = 0
        if o.SUPER_FASTPATH in self.state.options:
            # Only execute the last but two instructions
            imark_counter = 0
            for i in xrange(len(stmts) - 1, -1, -1):
                if type(stmts[i]) is pyvex.IRStmt.IMark:
                    imark_counter += 1
                if imark_counter >= 2:
                    skip_stmts = i
                    break

        for stmt_idx, stmt in enumerate(stmts):
            if self.last_stmt is not None and stmt_idx > self.last_stmt:
                l.debug("%s stopping analysis at statement %d.", self, self.last_stmt)
                break

            if stmt_idx < skip_stmts:
                continue

            #l.debug("%s processing statement %s of max %s", self, stmt_idx, self.last_stmt)
            self.state.scratch.stmt_idx = stmt_idx

            # we'll pass in the imark to the statements
            if type(stmt) == pyvex.IRStmt.IMark:
                self.last_imark = IMark(stmt)
                self.state.scratch.last_ins_addr = self.state.scratch.ins_addr
                self.state.scratch.ins_addr = stmt.addr + stmt.delta

                for subaddr in xrange(stmt.addr, stmt.addr + stmt.len):
                    if subaddr in self.state.scratch.dirty_addrs:
                        raise SimReliftException(self.state)
                self.state._inspect('instruction', BP_AFTER)

                l.debug("IMark: %#x", stmt.addr)
                self.state.scratch.num_insns += 1
                if o.INSTRUCTION_SCOPE_CONSTRAINTS in self.state.options:
                    if 'solver_engine' in self.state.plugins:
                        self.state.release_plugin('solver_engine')

                self.state._inspect('instruction', BP_BEFORE, instruction=self.last_imark.addr)

            if self.whitelist is not None and stmt_idx not in self.whitelist:
                l.debug("... whitelist says skip it!")
                continue
            elif self.whitelist is not None:
                l.debug("... whitelist says analyze it!")

            # process it!
            self.state._inspect('statement', BP_BEFORE, statement=stmt_idx)
            s_stmt = translate_stmt(self.irsb, stmt_idx, self.last_imark, self.state)
            if s_stmt is not None:
                self.state.log.extend_actions(s_stmt.actions)
            self.statements.append(s_stmt)
            self.state._inspect('statement', BP_AFTER)

            # for the exits, put *not* taking the exit on the list of constraints so
            # that we can continue on. Otherwise, add the constraints
            if type(stmt) == pyvex.IRStmt.Exit:
                l.debug("%s adding conditional exit", self)

                exit_ins_addr = self.state.scratch.last_ins_addr if self.state.arch.branch_delay_slot else \
                    self.state.scratch.ins_addr
                e = self.add_successor(self.state.copy(), s_stmt.target, s_stmt.guard, s_stmt.jumpkind,
                                       exit_stmt_idx=stmt_idx, exit_ins_addr=exit_ins_addr)
                self.conditional_exits.append(e)
                self.state.add_constraints(self.state.se.Not(s_stmt.guard))
                self.default_exit_guard = self.state.se.And(self.default_exit_guard, self.state.se.Not(s_stmt.guard))

                if o.SINGLE_EXIT in self.state.options and e.satisfiable():
                    l.debug("%s returning after taken exit due to SINGLE_EXIT option.", self)
                    return

        if self.last_stmt is None:
            self.has_default_exit = True

    def _prepare_temps(self, state):
        # prepare symbolic variables for the statements if we're using SYMBOLIC_TEMPS
        if o.SYMBOLIC_TEMPS in self.state.options:
            for n, t in enumerate(self.irsb.tyenv.types):
                state.scratch.temps[n] = self.state.se.Unconstrained('t%d_%s' % (n, self.id), size_bits(t))
            l.debug("%s prepared %d symbolic temps.", len(state.scratch.temps), self)

    def imark_addrs(self):
        """
        Returns a list of instructions that are part of this block.
        """
        return [ i.addr for i in self.irsb.statements if type(i) == pyvex.IRStmt.IMark ]

    def reanalyze(self, mode=None, new_state=None, irsb_id=None, whitelist=None):
        new_state = self.initial_state.copy() if new_state is None else new_state

        if mode is not None:
            new_state.set_mode(mode)

        irsb_id = self.id if irsb_id is None else irsb_id
        whitelist = self.whitelist if whitelist is None else whitelist
        return SimIRSB(new_state, self.irsb, addr=self.addr, irsb_id=irsb_id, whitelist=whitelist) #pylint:disable=E1124

from .statements import translate_stmt
from .expressions import translate_expr

from . import size_bits
from .. import s_options as o
from ..plugins.inspect import BP_AFTER, BP_BEFORE
from ..s_errors import SimError, SimIRSBError, SimSolverError, SimMemoryAddressError, SimReliftException
from ..s_action import SimActionExit, SimActionObject
