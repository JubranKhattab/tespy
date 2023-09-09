from tespy.networks import Network
from tespy.components import (Source, Sink, Turbine)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
import plotly.graph_objects as go
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d


# network
turbine_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
turb = Turbine("Turbine")
so = Source("Source")
si = Sink("Sink")

# Connections
so_2_turb = Connection(so, 'out1', turb, 'in1', label="Inlet")
turb_2_si = Connection(turb, 'out1', si, 'in1', label="Outlet")

turbine_nw.add_conns(so_2_turb,
                     turb_2_si)

# define parameters
turb.set_attr(eta_s=0.8)

so_2_turb.set_attr(fluid={'Water': 1}, T=600, p=100,  m=20)
turb_2_si.set_attr(x=1)

# exergy analysis
# define busses
# product
power = Bus('power output')
power.add_comps(
    {'comp': turb, 'char': 0.5, 'base': 'component'})

# fuel
hot_steam = Bus('fresh steam dif')
hot_steam.add_comps(
    {'comp': so, 'base': 'bus'},
    {'comp': si})

# loss

# ambient
pamb = 0.1
Tamb = 25

# add busses to nw
# hot_steam is not necessary to add
turbine_nw.add_busses(power)


# solve network with busses but without exergy analyses
turbine_nw.solve(mode='design')
turbine_nw.print_results()

# define ena and assign as P, F, L
ean = ExergyAnalysis(turbine_nw, E_P=[power], E_F=[hot_steam], E_L=[])

# do analysis
# define input for exe eco - later Read dict that is already filled.
# Component label + _Z for Z
comp_labels = turbine_nw.comps.index.tolist()
z_cost_streams = {key: None for key in comp_labels}
z_cost_streams = {key + '_Z': value for key, value in z_cost_streams.items()}
z_cost_streams['Turbine_Z'] = 120

# Source (component) label + _c for c_cost in Inlets
sources_labels = turbine_nw.comps[turbine_nw.comps['comp_type'] == 'Source'].index.tolist()
c_cost_source = {key: None for key in sources_labels}
c_cost_source = {key + '_c': value for key, value in c_cost_source.items()}
c_cost_source['Source_c'] = 20

exe_eco_input = {**z_cost_streams, **c_cost_source}
# source has no z --> only one dict is necessary

ean.analyse(pamb=pamb, Tamb=Tamb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.print_results()







