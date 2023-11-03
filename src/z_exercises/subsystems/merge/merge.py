from tespy.components import Sink, Source, Merge
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI as PSI
from tespy.tools.helpers import mass_flow

# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
#fluid_list = ["H2O", "CO2"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

# components
so1 = Source('air')
so2 = Source('fuel')
m = Merge('Mixer')
si1 = Sink('sink')

inc1 = Connection(so1, 'out1', m, 'in1', label='Air')
inc2 = Connection(so2, 'out1', m, 'in2', label='Fuel')
outg = Connection(m, 'out1', si1, 'in1', label='Abgas')

nw.add_conns(inc1, inc2, outg)

#air
air_0= {
        "CO2": 0.00027, "ethane": 0, "N2": 0.78092,
        "C3H8": 0, "CH4": 0,  "O2": 0.20947, "H2O":0,
        "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0,
        "Ar":0.00934, "H2": 0
    }

# psatH2O = PSI('P', 'Q', 0, 'T', 12+273.15, 'water') * 0.00001
# rh = 75
# pH2O = float(rh) / 100 * psatH2O
#
# xH2O = PSI('M', 'water') * (pH2O / 19.247) / (
#     pH2O/19.247 * PSI('M', 'water') + (1 - pH2O/19.247) * PSI('M', 'air'))
#
# air_0 = {key: value * (1-xH2O) for key, value in air_0.items()}
# air_0['H2O'] = xH2O
air_0 = mass_flow(air_0)

#air_0 = {"H2O": 0.5, "CO2":0.5}
inc1.set_attr(m=148.83,
    p=18.285, T=412.39,
    fluid=air_0
)

#fuel
fuel_n = {
        "CO2": 0.01800, "ethane": 0.03600, "N2": 0.10300,
        "C3H8": 0.00600, "CH4": 0.83380,  "O2": 0.000010, "H2O":0,
        "n-Butane": 0.00200, "n-Pentane": 0.00050, "n-Hexane": 0.00069,
        "Ar":0, "H2": 0
    }
fuel = mass_flow(fuel_n)
# fuel= {"H2O": 0.9, "CO2": 0.1}
inc2.set_attr(
     T=1500,
    fluid=fuel
)

# starting value
outg.set_attr(fluid0={"O2": 0.01}, T=600)

nw.solve('design')
nw.print_results()
