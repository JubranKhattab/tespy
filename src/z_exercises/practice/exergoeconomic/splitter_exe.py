from tespy.networks import Network
from tespy.components import (Source, Sink, Splitter)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d



# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
sp = Splitter('Splitter', num_out = 2)
so = Source("source_stream")
si = Sink("out_1")
si_2 = Sink("out_2")

# connections
in_splitter = Connection(so, 'out1', sp, 'in1', label='stream in splitter')
out_splitter = Connection(sp, 'out1', si, 'in1', label='out 1')
out_splitter_2 = Connection(sp, 'out2', si_2, 'in1', label='out 2')


nw.add_conns(in_splitter, out_splitter)
nw.add_conns(out_splitter_2)

# parameters
# mixer

# cold in
in_splitter.set_attr(T=60, p=2, fluid={'Water': 1}, m=5)

# hot in
out_splitter.set_attr( m=1)
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
so_in_B = Bus('in')
so_in_B.add_comps({'comp': so, 'base': 'bus'})

si_out = Bus('out')
si_out.add_comps({'comp': si})

si_out2 = Bus('out2')
si_out2.add_comps({'comp': si_2})


# heat_in = Bus('Fuel In')
# heat_in.add_comps({'comp': fuel_source, 'base':'bus'})


# ++ add busses to network
nw.add_busses(so_in_B, si_out, si_out2)

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_F=[so_in_B], E_P=[si_out2, si_out], E_L=[])

# input costs
exe_eco_input = {'Splitter_Z': 5, 'source_stream_c': 10}

# do analysis
#ean.analyse(pamb=p_amp, Tamb=T_amb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.analyse(pamb=p_amp, Tamb=T_amb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.print_results()

print(5 + in_splitter.C_tot - out_splitter.C_tot - out_splitter_2.C_tot )
