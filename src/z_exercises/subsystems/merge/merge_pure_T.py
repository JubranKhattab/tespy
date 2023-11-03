from tespy.components import Sink, Source, Merge
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI as PSI
from tespy.tools.helpers import mass_flow

# network
#fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
fluid_list = ["CO2", "H2O"]
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

##air
air_0 = {"CO2": 0.1, "H2O": 0.9}


inc1.set_attr(m=5,
    p=9, T=400,
    fluid=air_0
)

##fuel
fuel= { "CO2": 0, "H2O": 1}

inc2.set_attr(
     T=200,
    fluid=fuel
)

# starting values for out
outg.set_attr(fluid0={ "CO2":0.3, "H2O": 0.7}, h=900000)

nw.solve('design')
nw.print_results()

# Falls pure --> T am Ausgang als Eingabe möglich, sonst residual un gleich Null
