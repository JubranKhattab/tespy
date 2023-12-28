from tespy.networks import Network
from tespy.components import (Source, Sink, Condenser)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d



# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = Condenser('Condenser')
so_h_t = Source("Source Hot turbine")
so_h_v = Source("Source Hot valve")
so_h_mix = Source("Source Hot mix")
si_h = Sink("Sink condenser")
so_c = Source("Source Cold")
si_c = Sink("Sink Cold")
si_mix = Sink("Sink Mixer")

# connections
hot_in_2_hx = Connection(so_h_mix, 'out1', hx, 'in1', label='Hot In after mix - H')
hot_hx_2_out = Connection(hx, 'out1', si_h, 'in1', label='32')
cold_in_2_hx = Connection(so_c, 'out1', hx, 'in2', label='92')
cold_hx_2_out = Connection(hx, 'out2', si_c, 'in1', label='93')


nw.add_conns(hot_in_2_hx, hot_hx_2_out, cold_in_2_hx, cold_hx_2_out)


# parameters
# hx
hx.set_attr(pr1=1, pr2=0.675)
# hot
hot_in_2_hx.set_attr( p=0.022, x=0.98, fluid={'Water': 1}, m=64.94)
# cold
cold_in_2_hx.set_attr(T=8, p=1.5, fluid={'Water': 1})
cold_hx_2_out.set_attr(T=14)

# solve
nw.solve(mode='design')
nw.print_results()



