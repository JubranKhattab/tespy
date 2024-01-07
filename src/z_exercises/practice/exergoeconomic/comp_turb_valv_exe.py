from tespy.networks import Network
from tespy.components import (Source, Sink, Turbine, Compressor, Valve)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
import plotly.graph_objects as go
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d


# network
turbine_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
turb = Turbine("Turbine")
compr = Compressor("Compressor")
valv = Valve("Valve")
so = Source("Source")
si = Sink("Sink")

# Connections
so_2_compr = Connection(so, 'out1', compr, 'in1', label="Inlet")
compr_2_turb = Connection(compr, 'out1', turb, 'in1', label="Compr-Turbine")
turb_2_valv = Connection(turb, 'out1', valv, 'in1', label="Turbine-Valve")
valv_2_si = Connection(valv, 'out1', si, 'in1', label="Outlet")

turbine_nw.add_conns(so_2_compr, compr_2_turb,
                     turb_2_valv, valv_2_si)

# define parameters
turb.set_attr(eta_s=0.8)
compr.set_attr(pr=2, eta_s=1)
valv.set_attr(pr=0.5)

so_2_compr.set_attr(fluid={'Water': 1}, T=600, p=100,  m=20)
turb_2_valv.set_attr(x=1)

# exergy analysis
# define busses
# product
power = Bus('power output')
power.add_comps(
    {'comp': turb, 'char': 0.6, 'base': 'component'}, {'comp': compr, 'char': 1, 'base': 'bus'})


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
turbine_nw.add_busses(power, hot_steam)

# solve
turbine_nw.solve(mode='design')
turbine_nw.print_results()

exe_eco_input = {'Compressor_c': 500,'Source_c': 10, 'Turbine_Z': 500, 'Compressor_Z': 40, 'Valve_Z': 10}
# define ena and assign as P, F, L
ean = ExergyAnalysis(turbine_nw, E_P=[power], E_F=[hot_steam], E_L=[], internal_busses=[])
ean.analyse(pamb=pamb, Tamb=Tamb, Chem_Ex= ch_ex_d.stand_ch_exe_dict('Ahrendts'), Exe_Eco=exe_eco_input)
ean.print_results()


print(500 + compr_2_turb.C_tot - turb_2_valv.C_tot - turb.exe_eco['C_streams']['C_Power'])






