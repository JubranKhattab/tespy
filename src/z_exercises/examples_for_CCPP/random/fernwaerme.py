from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchanger)
from tespy.connections import Connection


# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

hk1 = HeatExchanger('HK1')
so_84m = Source('Source 84m')
so_71 = Source('Source 71')
si_85 = Sink('Sink 85')
si_72 = Sink('Sink 72')

# connections
c71 = Connection(so_71, 'out1', hk1, 'in2', label='71')
c72 = Connection(hk1, 'out2', si_72, 'in1', label='72')
c84m = Connection(so_84m, 'out1', hk1, 'in1', label='84m')
c85 = Connection(hk1, 'out1', si_85, 'in1', label='85')

nw.add_conns(c72, c71, c85, c84m)

# parameters
c71.set_attr(T=65, p=14.5, fluid={'Water': 1})
c72.set_attr(T=87)
c84m.set_attr(T=90, p=0.704,  fluid={'Water': 1})
hk1.set_attr(pr1=0.99, pr2=0.97, ttd_l=3, Q=-80000000)

nw.solve(mode="design")
nw.print_results()
