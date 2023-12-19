from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchanger)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d
from tespy.tools.helpers import mass_flow


fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]

# network
nw = Network(fluids=fluid_list, T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = HeatExchanger('Heat Exchanger')
so_h = Source("Source A")
si_h = Sink("Sink B")
so_fuel = Source("Source sfuel")
si_fuel = Sink("Sink fuel")

# connections
hot_in_2_hx = Connection(so_h, 'out1', hx, 'in1', label='88')
cold_in_2_hx = Connection(so_fuel, 'out1', hx, 'in2', label='9')
hot_hx_2_out = Connection(hx, 'out1', si_h, 'in1', label='89')
cold_hx_2_out = Connection(hx, 'out2', si_fuel, 'in1', label='10')

nw.add_conns(hot_in_2_hx, hot_hx_2_out)
nw.add_conns(cold_in_2_hx, cold_hx_2_out)

# parameters
# hx
hx.set_attr(pr1=0.99, pr2=0.998)
# hot
water_dict = air_0= {
        "CO2": 0, "ethane": 0, "N2": 0,
        "C3H8": 0, "CH4": 0,  "O2": 0, "H2O":1,
        "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0,
        "Ar":0, "H2": 0
    }
hot_in_2_hx.set_attr(T=238.18, p=36.442, fluid=water_dict, m=12.82)
hot_hx_2_out.set_attr(T=40)
# cold
fuel_n = {
        "CO2": 0.01800, "ethane": 0.03600, "N2": 0.10300,
        "C3H8": 0.00600, "CH4": 0.83380,  "O2": 0.000010, "H2O":0,
        "n-Butane": 0.00200, "n-Pentane": 0.00050, "n-Hexane": 0.00069,
        "Ar":0, "H2": 0
    }
fuel_methan = {
        "CO2": 0, "ethane": 0, "N2": 0,
        "C3H8": 0, "CH4": 1,  "O2": 0.000010, "H2O":0,
        "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0,
        "Ar":0, "H2": 0
    }
fuel_n = mass_flow(fuel_n)
cold_in_2_hx.set_attr(T=5, p=19.285, fluid=fuel_n, m = 26.31)
#cold_hx_2_out.set_attr(T=205)

# solve
nw.solve(mode='design')
nw.print_results()
