from tespy.networks import Network
from tespy.components import (Source, Sink, Valve)
from tespy.connections import Connection, Ref, Bus
from CoolProp import CoolProp as CP
from CoolProp.CoolProp import PropsSI as PSI
from tespy.tools.helpers import mass_flow

# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
air_0= {
        "CO2": 0.00027, "ethane": 0, "N2": 0.78092,
        "C3H8": 0, "CH4": 0,  "O2": 0.20947, "H2O":0,
        "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0,
        "Ar":0.00934, "H2": 0
    }


#fluid_list = ["Air"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

# components
valv = Valve("Valve")
so = Source("Source")
si = Sink("Sink")

# Connections
so_2_valv = Connection(so, 'out1', valv, 'in1', label="7")
valv_2_si = Connection(valv, 'out1', si, 'in1', label="8")

nw.add_conns(so_2_valv, valv_2_si)

# define parameters
so_2_valv.set_attr(fluid=air_0, T=412.38, p=19.247,  m=148.83)
valv.set_attr(pr=0.95)

# solve
nw.solve(mode='design')
nw.print_results()


enthalpy_air = PSI('H', 'T', 412.38+273.15, 'P', 19.247*10000, 'Air')
entropy_air = PSI('S', 'T', 412.38+273.15, 'P', 19.247*10000, 'Air')

print('h: ', round(enthalpy_air*0.001,2) , ' kJ/kg')
print('s: ', round(entropy_air*0.001, 4), ' kJ/kgK')
