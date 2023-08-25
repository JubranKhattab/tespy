from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchangerSimple)
from tespy.connections import Connection, Bus
from tespy.tools import analyses, ExergyAnalysis
import CoolProp.CoolProp as CP
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d


# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = HeatExchangerSimple("Heat Exchanger")
so = Source("Source label")
si = Sink("Sink label")

# Connections
so_2_hx = Connection(so, 'out1', hx, 'in1', label="Inlet")
hx_2_si = Connection(hx, 'out1', si, 'in1', label="Outlet")

nw.add_conns(so_2_hx, hx_2_si)

# define parameters
hx.set_attr(pr=0.5, Q=+10000000)

so_2_hx.set_attr(fluid={'Water':1.0}, T=30, p=10, m=40)

# solve
nw.solve(mode='design')
nw.print_results()


""" +++ exergy analysis +++ """
# define ambient
T_amb = 5
p_amp = 1

# ++define busses types++

# power
# +select placeS (components) of bus type+


# heat
# +select placeS (components) of bus type+
heat_in_B = Bus('Heat In')
heat_in_B.add_comps({'comp': hx, 'char': 1})

# mass flow
# +select placeS (components) of bus type+
mass_flow_B = Bus('water flow')
mass_flow_B.add_comps({'comp': so, 'base': 'bus'}, {'comp': si})


# ++ add busses to network
nw.add_busses(heat_in_B, mass_flow_B)

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_F=[heat_in_B], E_P=[mass_flow_B], E_L=[])

# do analysis
# define input for exe eco

comp_labels = nw.comps.index.tolist()
z_cost_streams = {key: None for key in comp_labels}
z_cost_streams['Heat Exchanger'] = 120

sources_labels = nw.comps[nw.comps['comp_type'] == 'Source'].index.tolist()
c_cost_source = {key: None for key in sources_labels}
c_cost_source['Source label'] = 0

exe_eco_input = {**z_cost_streams, **c_cost_source}
# source has no z --> only one dict is necessary
ean.analyse(pamb=p_amp, Tamb=T_amb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.print_results()
