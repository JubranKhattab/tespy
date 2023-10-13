from tespy.networks import Network
from tespy.components import (Source, Sink, DropletSeparator)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d



# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = DropletSeparator('Drum')
so_eco = Source("from eco")
si_sat_l = Sink("sat liquid")
si_sat_g = Sink("sat gas")

# connections
liq_in_2_hx = Connection(so_eco, 'out1', hx, 'in1', label='from economiser to drum')
sat_liq_out = Connection(hx, 'out1', si_sat_l, 'in1', label='out as saturated liquid')
sat_gas_out = Connection(hx, 'out2', si_sat_g, 'in1', label='out as saturated gas')

nw.add_conns(liq_in_2_hx, sat_liq_out)
nw.add_conns(sat_gas_out)

# parameters
# hx

# liquid in
liq_in_2_hx.set_attr(x=0.5, p=1, fluid={'Water': 1}, m=5)


# gas out
#sat_gas_out.set_attr(m=3)

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
eco_out = Bus('liquid in')
eco_out.add_comps({'comp': so_eco, 'base': 'bus'})

liq_out = Bus('liquid out')
liq_out.add_comps({'comp': si_sat_l})


gas_out = Bus('gas out')
gas_out.add_comps({'comp': si_sat_g})


# heat_in = Bus('Fuel In')
# heat_in.add_comps({'comp': fuel_source, 'base':'bus'})


# ++ add busses to network
nw.add_busses(eco_out, liq_out, gas_out)

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_F=[eco_out], E_P=[liq_out, gas_out], E_L=[])

# input costs
exe_eco_input = {'Drum_Z': 50, 'from eco_c': 10, 'from eva_c': 10}

# do analysis
ean.analyse(pamb=p_amp, Tamb=T_amb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
#ean.analyse(pamb=p_amp, Tamb=T_amb,  Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'))
ean.print_results()


