from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchanger)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d



# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
vw = HeatExchanger('VW')
so_33 = Source("Source 33")
so_85 = Source("Source 85")
si_85 = Sink("Sink 85")
si_34 = Sink("Sink 34")
si_mix = Sink("Sink Mixer")

# connections
c85 = Connection(so_85, 'out1', vw, 'in1', label='85')
c86 = Connection(vw, 'out1', si_85, 'in1', label='86')
c33 = Connection(so_33, 'out1', vw, 'in2', label='33')
c34 = Connection(vw, 'out2', si_34, 'in1', label='34')


nw.add_conns(c85, c86, c33, c34)


# parameters
# hx
vw.set_attr(pr1=0.99, pr2=0.99, Q=-100000)
# hot
c85.set_attr(p=0.6948, T=68, fluid={'Water': 1}, m=77.25)
# cold
c33.set_attr(T=19.1, p=25, fluid={'Water': 1}, m=64.95)


# solve
nw.solve(mode='design')
nw.print_results()



