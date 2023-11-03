from tespy.networks import Network
from tespy.components import (Source, Compressor, DiabaticCombustionChamber, Turbine, Sink, Valve, Merge, Splitter)
from tespy.connections import Connection, Ref, Bus
from CoolProp.CoolProp import PropsSI as PSI
from tespy.tools.helpers import mass_flow, molar_mass_flow

# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

# components
tv1 = Valve('TV1')
m_lambda = Merge('lambda')
sc = DiabaticCombustionChamber('Stoichiometric combustion')
so_air = Source('air')
so_fuel = Source('fuel')
sink = Sink('exit')
spl = Splitter("Splitter")


# connections
#so_to_cc = Connection(so_air, 'out1', sc, 'in1', label='3')
so_to_spl = Connection(so_air, 'out1', spl, 'in1', label='3')
spl_to_sc = Connection(spl, 'out1', sc, 'in1', label='4')
spl_to_valve = Connection(spl, 'out2', tv1, 'in1', label='5')
valve_to_merge = Connection(tv1, 'out1', m_lambda, 'in2', label='6')
fuel_to_chamber = Connection(so_fuel, 'out1', sc, 'in2', label='10')
#sc_to_sink = Connection(sc, 'out1', sink, 'in1', label='12')
sc_to_merge = Connection(sc, 'out1', m_lambda, 'in1', label='11')
merge_to_sink = Connection(m_lambda, 'out1', sink, 'in1', label='12')

#nw.add_conns(so_to_cc, fuel_to_chamber, cc_to_sink)
nw.add_conns(so_to_spl, spl_to_sc, spl_to_valve, valve_to_merge, fuel_to_chamber, sc_to_merge, merge_to_sink)
#nw.add_conns(fuel_to_chamber)

# parameters
# air source
air_0= {
        "CO2": 0.00027, "ethane": 0, "N2": 0.78092,
        "C3H8": 0, "CH4": 0,  "O2": 0.20947, "H2O":0,
        "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0,
        "Ar":0.00934, "H2": 0
    }

psatH2O = PSI('P', 'Q', 0, 'T', 12+273.15, 'water') * 0.00001
rh = 75
pH2O = float(rh) / 100 * psatH2O

xH2O = PSI('M', 'water') * (pH2O / 19.247) / (
    pH2O/19.247 * PSI('M', 'water') + (1 - pH2O/19.247) * PSI('M', 'air'))

air_0 = {key: value * (1-xH2O) for key, value in air_0.items()}
air_0['H2O'] = xH2O

air_0 = mass_flow(air_0)

so_to_spl.set_attr(
    p=19.247, T=412.38,
    fluid=air_0
)


# chamber
fuel_n = {
        "CO2": 0.01800, "ethane": 0.03600, "N2": 0.10300,
        "C3H8": 0.00600, "CH4": 0.83380,  "O2": 0.000010, "H2O":0,
        "n-Butane": 0.00200, "n-Pentane": 0.00050, "n-Hexane": 0.00069,
        "Ar":0, "H2": 0
    }

fuel = mass_flow(fuel_n)

fuel_to_chamber.set_attr(
    p=Ref(so_to_spl, 1.00, 0), T=195,
    fluid=fuel
)
# fuel_to_chamber.set_attr(p=Ref(comp_to_chamber, 1.00, 0))
sc.set_attr(pr=0.95, eta=0.98, lamb=1)
#cc_to_sink.set_attr(T=1506)

# splitter
spl_to_valve.set_attr(m=330.46)

# T instead of m
merge_to_sink.set_attr(T=1357)

# starting value
merge_to_sink.set_attr(fluid0={"N2": 0.1})

# solve
nw.solve(mode="design")
nw.print_results()
