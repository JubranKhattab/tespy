from tespy.networks import Network
from tespy.components import (Source, Sink, Valve)
from tespy.connections import Connection, Ref, Bus
from CoolProp.CoolProp import PropsSI as PSI
from tespy.tools.helpers import mass_flow

# network
fluid_list = ["Water"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

# components
valv = Valve("Valve")
so = Source("Source")
si = Sink("Sink")

# Connections
so_2_valv = Connection(so, 'out1', valv, 'in1', label="83")
valv_2_si = Connection(valv, 'out1', si, 'in1', label="84")

nw.add_conns(so_2_valv, valv_2_si)

# define parameters
so_2_valv.set_attr(fluid={'Water': 1}, T=145.15, p=1,  m=30.49)
valv.set_attr(pr=0.704)

# solve
nw.solve(mode='design')
nw.print_results()
