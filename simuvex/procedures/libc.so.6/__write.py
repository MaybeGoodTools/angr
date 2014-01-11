import simuvex
import symexec

######################################
# __write
######################################

import struct

class __write(simuvex.SimProcedure):
        def __init__(self, state, options=None, mode=None):
            simuvex.SimProcedure.__init__(self, state, options=options, mode=mode)
            if isinstance(self.initial_state.arch, simuvex.SimAMD64):
                dst = self.get_arg(0)
                src = self.get_arg(1)
                length = self.get_arg(2)

                ## TODO handle errors
                data = self.initial_state.mem_expr(src, length)
                self.initial_state.store_mem(dst, data)
                self.set_return_expr(length)
                ret_target = self.do_return()

                sim_src = simuvex.SimValue(src)
                sim_dst = simuvex.SimValue(dst)
                self.add_refs(simuvex.SimMemRead(sim_src, data, length))
                self.add_refs(simuvex.SimMemWrite(sim_dst, data, length))
                #TODO: also SimMemRef??

                self.add_exit(SimExit(expr=ret_target, state=self.initial_state))
            else:
                raise Exception("Architecture %s is not supported yet." % self.initial_state.arch)
