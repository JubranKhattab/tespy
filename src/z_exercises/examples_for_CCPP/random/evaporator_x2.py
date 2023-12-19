from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchanger)
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as PSI
from tespy.tools.helpers import mass_flow


# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
nw = Network(fluids=fluid_list, T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = HeatExchanger('evaporatorA')
hx_b = HeatExchanger('evaporatorB')
so_eco = Source("from eco")
si_overheater = Sink("to over heater")
so_hot_gas = Source("from eva")
si_hot_gas = Sink("sat liquid")



# connections
c_56 = Connection(so_eco, 'out1', hx, 'in2', label='56')
c_56_57 = Connection(hx, 'out2', hx_b, 'in2', label='56_57')
c_57 = Connection(hx_b, 'out2', si_overheater, 'in1', label='57')
c_29 = Connection(so_hot_gas, 'out1', hx_b, 'in1', label='29')
c_29_30 = Connection(hx_b, 'out1', hx, 'in1', label='29_30')
c_30 = Connection(hx, 'out1', si_hot_gas, 'in1', label='30')


nw.add_conns(c_56, c_56_57, c_57, c_29, c_29_30, c_30 )


# fluids
fuel_n = {
        "CO2": 0.01800, "ethane": 0.03600, "N2": 0.10300,
        "C3H8": 0.00600, "CH4": 0.83380,  "O2": 0.000010, "H2O":0,
        "n-Butane": 0.00200, "n-Pentane": 0.00050, "n-Hexane": 0.00069,
        "Ar":0, "H2": 0
    }
fuel_n = mass_flow(fuel_n)

water = {
        "CO2": 0, "ethane": 0, "N2": 0,
        "C3H8": 0, "CH4": 0,  "O2": 0, "H2O":1,
        "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0,
        "Ar":0, "H2": 0
    }



# parameters
# hx
# hx.set_attr(pr1=0.997, pr2=0.97, ttd_l= 15)
hx.set_attr(pr1=0.997, pr2=0.97)
undercooling = 5
overheating = 8

# water in
psatH2= 4.681
t_correct = 0.8962
tsatH2O = PSI('T', 'Q', 0, 'P', psatH2 * 100000 , 'H2O') - 273.15
c_eco_eva.set_attr(T=tsatH2O - undercooling , p=psatH2, fluid=water)

# hot gas in
c_hot_gas_in.set_attr(fluid=fuel_n, m=392.92, T=208.47, p=1.015)  # h_in_gas

# hot gas out
c_hot_gas_out.set_attr(T=164)  # h_out_gas

# water out
#c_eva_overheat.set_attr(T=tsatH2O+overheating)
c_eva_overheat.set_attr(m = 20)

# solve
nw.solve(mode='design')
nw.print_results()


H_water = PSI('H', 'T', 144.4+273.15, 'P', psatH2 * 100000 , 'H2O') - 273.15
print(H_water)
