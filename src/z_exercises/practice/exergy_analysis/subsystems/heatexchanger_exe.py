from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchangerSimple)
from tespy.connections import Connection, Bus
from tespy.tools import analyses, ExergyAnalysis
import CoolProp.CoolProp as CP


# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
hx = HeatExchangerSimple("Heat Exchanger")
so = Source("Source")
si = Sink("Sink")

# Connections
so_2_hx = Connection(so, 'out1', hx, 'in1', label="Inlet")
hx_2_si = Connection(hx, 'out1', si, 'in1', label="Outlet")

nw.add_conns(so_2_hx, hx_2_si)

# define parameters
hx.set_attr(pr=0.5, Q=+1000000)

so_2_hx.set_attr(fluid={'Water':1.0}, T=30, p=10, m=40)

# solve
nw.solve(mode='design')
nw.print_results()


""" +++ exergy analysis +++ """
# define ambient
T_amb = 5
p_amp = 1

# ++define busses types++

# power
# +select placeS (components) of bus type+


# heat
# +select placeS (components) of bus type+
heat_in_B = Bus('Heat In')
heat_in_B.add_comps({'comp': hx, 'char': 1})

# mass flow
# +select placeS (components) of bus type+
mass_flow_B = Bus('water flow')
mass_flow_B.add_comps({'comp': so, 'base': 'bus'}, {'comp': si})


# ++ add busses to network
nw.add_busses(heat_in_B, mass_flow_B)

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_F=[heat_in_B], E_P=[mass_flow_B], E_L=[])

# do analysis
ean.analyse(pamb=p_amp, Tamb=T_amb)
ean.print_results()
