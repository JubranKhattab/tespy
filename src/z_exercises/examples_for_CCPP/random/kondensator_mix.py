from tespy.networks import Network
from tespy.components import (Source, Sink, Condenser, Merge)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d



# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = Condenser('Condenser')
mx = Merge('Mixer')
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

hot_valve = Connection(so_h_v, 'out1', mx, 'in1', label='87')
hot_turbine = Connection(so_h_t, 'out1', mx, 'in2', label='70')
hot_h = Connection(mx, 'out1', si_mix, 'in1', label='70-87')

nw.add_conns(hot_valve, hot_turbine, hot_h)


# parameters
# hx
hx.set_attr(pr1=0.98, pr2=0.97)
# hot
hot_hx_2_out.set_attr(T=67.90, p=0.697, fluid={'Water': 1}, m=76.94)
# cold
cold_in_2_hx.set_attr(T=65.00, p=14.065, fluid={'Water': 1}, m=864.32)
cold_hx_2_out.set_attr(T=87.09)
# mixer
hot_turbine.set_attr(m=64.94, h=2270.43, p=0.022, fluid={'Water': 1})
hot_valve.set_attr(m=76.94,  h=122.04, fluid={'Water': 1})

# solve
nw.solve(mode='design')
nw.print_results()



