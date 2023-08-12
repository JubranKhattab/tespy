from tespy.networks import Network
from tespy.components import (Source, Compressor, DiabaticCombustionChamber, Turbine, Sink)
from tespy.connections import Connection, Ref, Bus
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d


"""
here without entering chemical exergy. This means that epsilon is infinitely large.
Reason: E_fuel is zero because ambient air has no physical exergy.
Fuel stream also has no physical exergy (at p, T Ambient). Nevertheless, the physical exergy at the exit E_P is large because of the combustion.
 --> epsilon = E_P / E_F , E_F = 0 --> infinity
"""

# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

# components
chamber = DiabaticCombustionChamber('Combustion Chamber')
air_source = Source('Air Inlet')
exhaust_sink = Sink('Exhaust')
fuel_source = Source('Fuel')

# connections
so_to_cham = Connection(air_source, 'out1', chamber, 'in1', label='1')
fuel_to_chamber = Connection(fuel_source, 'out1', chamber, 'in2', label='2')
chamber_to_exhaust = Connection(chamber, 'out1', exhaust_sink, 'in1', label='3')


nw.add_conns(so_to_cham, fuel_to_chamber, chamber_to_exhaust)
#nw.add_conns(fuel_to_chamber)


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




# solve
nw.solve(mode="design")
nw.print_results()

""" +++ Exergy analysis +++ """
# define ambient
T_amb = 20
p_amp = 1

# ++define busses types++

# power
# +select placeS (components) of bus type+



# heat
# +select placeS (components) of bus type+


# mass flow
# +select placeS (components) of bus type+
heat_in = Bus('Fuel In')
heat_in.add_comps({'comp': fuel_source, 'base':'bus'})

air_in = Bus('Air In')
air_in.add_comps({'comp': air_source,  'base':'bus'})

exhaust_out = Bus('Hot unused Air')
exhaust_out.add_comps({'comp': exhaust_sink})

# ++ add busses to network
nw.add_busses( heat_in, exhaust_out, air_in)

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_F=[heat_in, air_in], E_P=[exhaust_out], E_L=[])

# do analysis
ean.analyse(pamb=p_amp, Tamb=T_amb, Chem_Ex=ch_ex_d.stand_ch_exe_dict("Ahrendts"))
ean.print_results()


