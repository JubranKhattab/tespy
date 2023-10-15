from tespy.networks import Network
from tespy.components import (Source, Sink, Merge)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d



# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = Merge('Mixer', num_in = 2)
## hx = Merge('Mixer', num_in = 3)
so_cold = Source("cold_stream")
si = Sink("out_mix")
so_hot = Source("hot_stream")
so_hot_2 = Source("hot_stream_2")


# connections
cold_in_mixer = Connection(so_cold, 'out1', hx, 'in1', label='cold_stream to Mixer')
hot_in_mixer = Connection(so_hot, 'out1', hx, 'in2', label='hot_stream to Mixer')
##hot2_in_mixer = Connection(so_hot_2, 'out1', hx, 'in3', label='hot_stream_2 to Mixer')
out_mix = Connection(hx, 'out1', si, 'in1', label='out as mix')


nw.add_conns(cold_in_mixer, out_mix)
nw.add_conns(hot_in_mixer)

# parameters
# mixer

# cold in
cold_in_mixer.set_attr(T=60, p=2, fluid={'Water': 1}, m=5)

# hot in
hot_in_mixer.set_attr(T=200, fluid={'Water': 1}, m=6)
##hot2_in_mixer.set_attr(T=230, fluid={'Water': 1}, m=4)


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
cold_in = Bus('cold')
cold_in.add_comps({'comp': so_cold, 'base': 'bus'})

hot_in = Bus('hot')
hot_in.add_comps({'comp': so_hot, 'base': 'bus'})

##hot2_in = Bus('hot2')
##hot2_in.add_comps({'comp': so_hot_2, 'base': 'bus'})

out_mix_B = Bus('out')
out_mix_B.add_comps({'comp': si})


# heat_in = Bus('Fuel In')
# heat_in.add_comps({'comp': fuel_source, 'base':'bus'})


# ++ add busses to network
nw.add_busses(cold_in, hot_in, out_mix_B)

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_F=[cold_in, hot_in], E_P=[out_mix_B], E_L=[])

# input costs
exe_eco_input = {'Mixer_Z': 0, 'cold_stream_c': 10, 'hot_stream_c': 20, 'hot_stream_2_c': 10}

# do analysis
#ean.analyse(pamb=p_amp, Tamb=T_amb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.analyse(pamb=p_amp, Tamb=T_amb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.print_results()


