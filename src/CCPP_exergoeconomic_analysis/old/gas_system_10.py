from tespy.networks import Network
from tespy.components import (Source, Compressor, DiabaticCombustionChamber, Turbine, Sink, Valve, Merge, Splitter, HeatExchanger)
from tespy.connections import Connection, Bus
import help_func as h_f

# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

exhaust_m = h_f.exhaust_m
air_n = h_f.air_n
fuel_n = h_f.fuel_n

# components
v = Compressor('V')
dr_ue1 = Valve('DRue1')
exp = Turbine('EXP')
mix_tit = Merge('MIX TIT')
spl_v = Splitter('Splitter V')
bk = DiabaticCombustionChamber('BK')
so_1 = Source('Source 1')
so_10 = Source('Source 10')
si_14 = Sink('Sink 14')

# connections
c1 = Connection(so_1, 'out1', v, 'in1', label='1')
c2 = Connection(v, 'out1', spl_v, 'in1', label='2')
c3 = Connection(spl_v, 'out1', bk, 'in1', label='3')
c7 = Connection(spl_v, 'out2', dr_ue1, 'in1', label='7')
c8 = Connection(dr_ue1, 'out1', mix_tit, 'in2', label='8')
c10 = Connection(so_10, 'out1', bk, 'in2', label='10')
c12 = Connection(bk, 'out1', mix_tit, 'in1', label='12')
c13 = Connection(mix_tit, 'out1', exp, 'in1', label='13')
c14 = Connection(exp, 'out1', si_14, 'in1', label='14')

# busses
g_v = Bus("generator v - 95")
g_v.add_comps({"comp": v, "char": 0.995*0.995, "base": "bus"})
g_exp = Bus("generator turbine")
g_exp.add_comps({"comp": exp, "char": 0.995*0.995, "base": "component"})
nw.add_busses(g_v, g_exp)

# add connections
nw.add_conns(c1, c2, c3, c7, c8, c10, c12, c13, c14)

# set parameters
# V
v.set_attr(eta_s=0.90, pr=19)
air_m = h_f.humid_air(T=5, rh=75, air_n=air_n)
c1.set_attr(m=803.961, p=1.013, T=5,fluid=air_m)

# Splitter V
c7.set_attr(m=138.743)


# BK
bk.set_attr(pr=0.95, eta=0.98, lamb=1.9)
fuel_m = h_f.calc_mass_flow(fuel_n)
c10.set_attr(p=19.258, T=5, fluid=fuel_m)

# EXP
exp.set_attr(eta_s=0.90)
c14.set_attr(p=1.051)

# starting values for c13
c13.set_attr(fluid0={"O2": 0.001})

# solve
nw.solve(mode="design")
nw.print_results()
