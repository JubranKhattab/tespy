from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchanger)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d



# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = HeatExchanger('Heat Exchanger')
so_h = Source("Source Hot")
si_h = Sink("Sink Hot")
so_c = Source("Source Cold")
si_c = Sink("Sink Cold")

# connections
hot_in_2_hx = Connection(so_h, 'out1', hx, 'in1', label='Hot In')
cold_in_2_hx = Connection(so_c, 'out1', hx, 'in2', label='Cold In')
hot_hx_2_out = Connection(hx, 'out1', si_h, 'in1', label='Hot Out')
cold_hx_2_out = Connection(hx, 'out2', si_c, 'in1', label='Cold Out')

nw.add_conns(hot_in_2_hx, hot_hx_2_out)
nw.add_conns(cold_in_2_hx, cold_hx_2_out)

# parameters
# hx
hx.set_attr(pr1=1, pr2=1)
# hot
hot_in_2_hx.set_attr(T=90, p=1, fluid={'Water': 1}, m=5)
hot_hx_2_out.set_attr(T=70)
# cold
cold_in_2_hx.set_attr(T=20, p=1, fluid={'Water': 1})
cold_hx_2_out.set_attr(T=50)

# solve
nw.solve(mode='design')
nw.print_results()


""" +++ exergy analysis +++ """
# define ambient
T_amb = 10
p_amp = 1

# ++define busses types++

# power
# +select placeS (components) of bus type+


# heat
# +select placeS (components) of bus type+


# mass flow
# +select placeS (components) of bus type+
heat_in_B = Bus('Heat In')
heat_in_B.add_comps({'comp': so_h, 'base':'bus'}, {'comp':si_h})
heated_B = Bus('Heated fluid')
heated_B.add_comps({'comp':so_c, 'base':'bus'}, {'comp': si_c})


# ++ add busses to network
nw.add_busses(heat_in_B, heated_B)

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_F=[heat_in_B], E_P=[heated_B], E_L=[])

# input costs
exe_eco_input = {'Heat Exchanger_Z': 50, 'Source Hot_c': 10, 'Source Cold_c': 10}

# do analysis
ean.analyse(pamb=p_amp, Tamb=T_amb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.print_results()

# print(50 + hot_in_2_hx.C_tot + cold_in_2_hx.C_tot - hot_hx_2_out.C_tot - cold_hx_2_out.C_tot)
