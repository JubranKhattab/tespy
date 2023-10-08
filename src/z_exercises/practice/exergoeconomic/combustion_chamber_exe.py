from tespy.networks import Network
from tespy.components import (Source, Sink, DiabaticCombustionChamber)
from tespy.connections import Connection, Bus, Ref
from tespy.tools import ExergyAnalysis
import plotly.graph_objects as go
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d


# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2"]
nw = Network(fluids=fluid_list, T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
chamber = DiabaticCombustionChamber('Combustion Chamber')
air_source = Source('Air Inlet')
exhaust_sink = Sink('Exhaust')
fuel_source = Source('Fuel')

# connections
so_to_cham = Connection(air_source, 'out1', chamber, 'in1', label='Air to Chamber')
fuel_to_chamber = Connection(fuel_source, 'out1', chamber, 'in2', label='Fuel to Chamber')
chamber_to_exhaust = Connection(chamber, 'out1', exhaust_sink, 'in1', label='to Exhaust')

nw.add_conns(so_to_cham, fuel_to_chamber, chamber_to_exhaust)


# parameters
# air source
so_to_cham.set_attr(
    p=1.0, T=20,
    fluid={
        "Ar": 0.0129, "N2": 0.7553, "H2O": 0,
        "CH4": 0, "CO2": 0.0004, "O2": 0.2314, "H2": 0
    }
)


# chamber
fuel_to_chamber.set_attr(
    p=Ref(so_to_cham, 1.0, 0), T=20,
    fluid={
        "CO2": 0.04, "Ar": 0, "N2": 0, "O2": 0,
        "H2O": 0, "CH4": 0.96, "H2": 0
    }
)
# fuel_to_chamber.set_attr(p=Ref(comp_to_chamber, 1.00, 0))
chamber.set_attr(pr=1, eta=0.99, ti=10e6)
chamber_to_exhaust.set_attr(T=1200)

# exergy analysis
# define busses
# +select placeS (components) of bus type+
heat_in = Bus('Fuel In')
heat_in.add_comps({'comp': fuel_source, 'base':'bus'})
air_in = Bus('Air In')
air_in.add_comps({'comp': air_source, 'base':'bus'})

exhaust_out = Bus('Hot unused Air')
exhaust_out.add_comps({'comp': exhaust_sink})


# ambient
pamb = 0.1
Tamb = 25

# add busses to nw
nw.add_busses( heat_in, air_in, exhaust_out)


# solve network with busses but without exergy analyses
nw.solve(mode='design')
nw.print_results()

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_P=[exhaust_out], E_F=[heat_in, air_in], E_L=[])

# do analysis
# define input for exe eco - later Read dict that is already filled.
# Component label + _Z for Z
comp_labels = nw.comps.index.tolist()
z_cost_streams = {key: None for key in comp_labels}
z_cost_streams = {key + '_Z': value for key, value in z_cost_streams.items()}
z_cost_streams['Combustion Chamber_Z'] = 120

# Source (component) label + _c for c_cost in Inlets
sources_labels = nw.comps[nw.comps['comp_type'] == 'Source'].index.tolist()
c_cost_source = {key: None for key in sources_labels}
c_cost_source = {key + '_c': value for key, value in c_cost_source.items()}
c_cost_source['Air Inlet_c'] = 20
c_cost_source['Fuel_c'] = 3000

exe_eco_input = {**z_cost_streams, **c_cost_source}
# source has no z --> only one dict is necessary

ean.analyse(pamb=pamb, Tamb=Tamb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.print_results()







