from tespy.networks import Network
from tespy.components import (Source, Pump, Turbine, Sink, Valve, Merge, Splitter, HeatExchanger, Condenser, Compressor, DiabaticCombustionChamber)
from tespy.connections import Connection, Bus
from CCPP_exergoeconomic_analysis import help_func as h_f
from tespy.tools import ExergyAnalysis
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d

# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C", p_range=[0.01, 175], h_range=[1, 50000000])

exhaust_m = h_f.exhaust_m
air_n = h_f.air_n
fuel_n = h_f.fuel_n
water_m = h_f.water_m

# components
so_14 = Source('Source 14')
si_31 = Sink('Sink 31')
so_35 = Source('Source 35')
# high p - hx
eco1 = HeatExchanger('ECO1')
eco2 = HeatExchanger('ECO2')
eco3 = HeatExchanger('ECO3')
vd1 = HeatExchanger('VD1')
uh1 = HeatExchanger('UH1')
uh2 = HeatExchanger('UH2')
uh3 = HeatExchanger('UH3')
uh4 = HeatExchanger('UH4')
# medium p - hx
eco4 = HeatExchanger('ECO4')
vd2 = HeatExchanger('VD2')
uh5 = HeatExchanger('UH5')
zuh1 = HeatExchanger('ZUH1')
zuh2 = HeatExchanger('ZUH2')
zuh3 = HeatExchanger('ZUH3')
# low p - hx
vd3 = HeatExchanger('VD3')
uh6 = HeatExchanger('UH6')

kvw = HeatExchanger('kvw')
spl_kvw = Splitter('Splitter KVW')
# low p - other
dr_ue3 = Valve('DRue3')
dt3 = Turbine('DT3')
# medium p - other
p2 = Pump('P2')
dt2 = Turbine('DT2')
spl_p2 = Splitter('Splitter P2')
spl_bvw = Splitter('Splitter BVW')
# high p - other
p3 = Pump('P3')
dt1 = Turbine('DT1')
mix_zuh = Merge('Mix ZUH')
spl_fw3 = Splitter('Splitter FW3')
mix_dt3 = Merge('Mix DT3')

# B
dt4 = Turbine('DT4')
dt5 = Turbine('DT5')
spl_fw2 = Splitter('Splitter FW2')
spl_fw1 = Splitter('Splitter FW1')
dr_ue4 = Valve('DRue4')
dr_ue5 = Valve('DRue5')
dr_ue6 = Valve('DRue6')
mix_fw2 = Merge('Mix FW2')
mix_fw1 = Merge('Mix FW1')
dr_be2 = Valve('DRbe2')
dr_be3 = Valve('DRbe3')
hk1 = HeatExchanger('HK1')
hk2 = HeatExchanger('HK2')
hk3 = HeatExchanger('HK3')
so_71 = Source('Source 71')
si_74 = Sink('Sink 74')

# C
mix_kon = Merge('Mix KON')
kon = Condenser('KON')
p4 = Pump('P4')
dr_be4 = Valve('DRbe4')
p1 = Pump('P1')
vw = HeatExchanger('VW')
so_91 = Source('Source 91')
si_93 = Sink('Sink 93')
si_34 = Sink('Sink 34')
#si_85 = Sink('Sink 85')
#si_33 = Sink('Sink 33')
si_87 = Sink('Sink 87')
si_random_kon = Sink('Sink random kon')
si_random_fw = Sink('Sink random fw')

# Gas Turbine System
v = Compressor('V')
dr_ue1 = Valve('DRue1')
exp = Turbine('EXP')
mix_tit = Merge('MIX TIT')
spl_v = Splitter('Splitter V')
bk = DiabaticCombustionChamber('BK')
so_1 = Source('Source 1')
so_10 = Source('Source 10')
si_14_g = Sink('Sink 14 - Gas')

# connections
c35 = Connection(so_35, 'out1', kvw, 'in2', label='35')
c36 = Connection(kvw, 'out2', spl_kvw, 'in1', label='36')
c55 = Connection(spl_kvw, 'out1', dr_ue3, 'in1', label='55')
c37 = Connection(spl_kvw, 'out2', p2, 'in1', label='37')
# low p - conn
c56 = Connection(dr_ue3, 'out1', vd3, 'in2', label='56')
c57 = Connection(vd3, 'out2', uh6, 'in2', label='57')
c58 = Connection(uh6, 'out2', mix_dt3, 'in1', label='58')
c63 = Connection(dt2, 'out1', spl_fw3, 'in1', label='63')
c64 = Connection(spl_fw3, 'out2', mix_dt3, 'in2', label='64')
c65 = Connection(mix_dt3, 'out1', dt3, 'in1', label='65')
c75 = Connection(spl_fw3, 'out1', dr_ue4, 'in1', label='75')
c79 = Connection(spl_fw2, 'out1', dr_ue5, 'in1', label='79')  # b
c67 = Connection(spl_fw2, 'out2', dt4, 'in1', label='67')  # b
c68 = Connection(dt4, 'out1', spl_fw1, 'in1', label='68')  # b
c83 = Connection(spl_fw1, 'out1', dr_ue6, 'in1', label='83')  # b
c69 = Connection(spl_fw1, 'out2', dt5, 'in1', label='69')  # b
c70 = Connection(dt5, 'out1', kon, 'in1', label='70')  # b
#c70m = Connection(mix_kon, 'out1', kon, 'in1', label='70m')  # c
c32 = Connection(kon, 'out1', p1, 'in1', label='32')  # c
c33 = Connection(p1, 'out1', vw, 'in2', label='33')  # c
c34 = Connection(vw, 'out2', si_34, 'in1', label='34')  # c
c76 = Connection(dr_ue4, 'out1', hk3, 'in1', label='76')  # b
c77 = Connection(hk3, 'out1', dr_be2, 'in1', label='77')  # b
c78 = Connection(dr_be2, 'out1', mix_fw2, 'in1', label='78')  # b
c80 = Connection(dr_ue5, 'out1', mix_fw2, 'in2', label='80')  # b
c80m = Connection(mix_fw2, 'out1', hk2, 'in1', label='80m')  # b
c81 = Connection(hk2, 'out1', dr_be3, 'in1', label='81')  # b
c82 = Connection(dr_be3, 'out1', mix_fw1, 'in1', label='82')  # b
c84 = Connection(dr_ue6, 'out1', mix_fw1, 'in2', label='84')  # b
c84m = Connection(mix_fw1, 'out1', hk1, 'in1', label='84m')  # b
c85 = Connection(hk1, 'out1', vw, 'in1', label='85')  # b
c86 = Connection(vw, 'out1', dr_be4, 'in1', label='86')  # c
c87 = Connection(dr_be4, 'out1', si_87, 'in1', label='87')  # c
c91 = Connection(so_91, 'out1', p4, 'in1', label='91')  # c
c92 = Connection(p4, 'out1', kon, 'in2', label='92')  # c
c93 = Connection(kon, 'out2', si_93, 'in1', label='93')  # c
c66 = Connection(dt3, 'out1', spl_fw2, 'in1', label='66')
# medium p - conn
c39 = Connection(spl_p2, 'out2', p3, 'in1', label='39')
c38 = Connection(p2, 'out1', spl_p2, 'in1', label='38')
c50 = Connection(spl_p2, 'out1', eco4, 'in2', label='50')
# c51 = Connection(eco4, 'out2', spl_bvw, 'in1', label='51')
# c88 = Connection(spl_bvw, 'out1', si_88, 'in1', label='88')
# c52 = Connection(spl_bvw, 'out2', vd2, 'in2', label='52')
c51 = Connection(eco4, 'out2', vd2, 'in2', label='51')
c53 = Connection(vd2, 'out2', uh5, 'in2', label='53')
c54 = Connection(uh5, 'out2', mix_zuh, 'in1', label='54')
c59 = Connection(mix_zuh, 'out1', zuh1, 'in2', label='59')
c60 = Connection(zuh1, 'out2', zuh2, 'in2', label='60')
c61 = Connection(zuh2, 'out2', zuh3, 'in2', label='61')
c62 = Connection(zuh3, 'out2', dt2, 'in1', label='62')
c49 = Connection(dt1, 'out1', mix_zuh, 'in2', label='49')
# high p - conn
c40 = Connection(p3, 'out1', eco1, 'in2', label='40')
c41 = Connection(eco1, 'out2', eco2, 'in2', label='41')
c42 = Connection(eco2, 'out2', eco3, 'in2', label='42')
c43 = Connection(eco3, 'out2', vd1, 'in2', label='43')
c44 = Connection(vd1, 'out2', uh1, 'in2', label='44')
c45 = Connection(uh1, 'out2', uh2, 'in2', label='45')
c46 = Connection(uh2, 'out2', uh3, 'in2', label='46')
c47 = Connection(uh3, 'out2', uh4, 'in2', label='47')
c48 = Connection(uh4, 'out2', dt1, 'in1', label='48')
# exhaust gas
c14 = Connection(so_14, 'out1', uh4, 'in1', label='14')
c15 = Connection(uh4, 'out1', zuh3, 'in1', label='15')
c16 = Connection(zuh3, 'out1', uh3, 'in1', label='16')
c17 = Connection(uh3, 'out1', zuh2, 'in1', label='17')
c18 = Connection(zuh2, 'out1', uh2, 'in1', label='18')
c19 = Connection(uh2, 'out1', zuh1, 'in1', label='19')
c20 = Connection(zuh1, 'out1', uh1, 'in1', label='20')
c21 = Connection(uh1, 'out1', vd1, 'in1', label='21')
c22 = Connection(vd1, 'out1', eco3, 'in1', label='22')
c23 = Connection(eco3, 'out1', uh5, 'in1', label='23')
c24 = Connection(uh5, 'out1', eco2, 'in1', label='24')
c25 = Connection(eco2, 'out1', vd2, 'in1', label='25')
c26 = Connection(vd2, 'out1', uh6, 'in1', label='26')
c27 = Connection(uh6, 'out1', eco4, 'in1', label='27')
c28 = Connection(eco4, 'out1', eco1, 'in1', label='28')
c29 = Connection(eco1, 'out1', vd3, 'in1', label='29')
c30 = Connection(vd3, 'out1', kvw, 'in1', label='30')
c31 = Connection(kvw, 'out1', si_31, 'in1', label='31')
# district heating
c71 = Connection(so_71, 'out1', hk1, 'in2', label='71')  # b
c72 = Connection(hk1, 'out2', hk2, 'in2', label='72')  # b
c73 = Connection(hk2, 'out2', hk3, 'in2', label='73')  # b
c74 = Connection(hk3, 'out2', si_74, 'in1', label='74')  # b
# gas turbine system
c1 = Connection(so_1, 'out1', v, 'in1', label='1')
c2 = Connection(v, 'out1', spl_v, 'in1', label='2')
c3 = Connection(spl_v, 'out1', bk, 'in1', label='3')
c7 = Connection(spl_v, 'out2', dr_ue1, 'in1', label='7')
c8 = Connection(dr_ue1, 'out1', mix_tit, 'in2', label='8')
c10 = Connection(so_10, 'out1', bk, 'in2', label='10')
c12 = Connection(bk, 'out1', mix_tit, 'in1', label='12')
c13 = Connection(mix_tit, 'out1', exp, 'in1', label='13')
c14_gas = Connection(exp, 'out1', si_14_g, 'in1', label='14 new')
#c14 = Connection(exp, 'out1', si_14, 'in1', label='14')

# add connections
nw.add_conns(c1, c2, c3, c7, c8, c10, c12, c13, c14_gas)
nw.add_conns(c35, c36, c55, c56, c57, c58, c37, c38, c39, c50, c51, c53, c54, c59, c60, c61, c62, c49, c63, c75, c64, c65, c66,
             c40, c41, c42, c43, c44, c45, c46, c47, c48, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31
)
nw.add_conns(c79, c67, c68, c83, c69, c70, c76, c77, c78, c80, c80m, c81, c82, c84, c84m, c85, c71, c72, c73, c74)
nw.add_conns( c32, c33, c34, c86, c87, c91, c92, c93)
# nw.add_conns(c1, c2, c3, c7, c8, c10, c12, c13)


# busses
# pumps
g_p2 = Bus("generator P2 - 102")
g_p3 = Bus("generator P3 - 103")
g_p1 = Bus("generator P1 - 101")
g_p4 = Bus("generator P4 - 104")
g_p2.add_comps({"comp": p2, "char": 1.0, "base": "bus"})
g_p3.add_comps({"comp": p3, "char": 1.0, "base": "bus"})
g_p1.add_comps({"comp": p1, "char": 1.0, "base": "bus"})
g_p4.add_comps({"comp": p4, "char": 1.0, "base": "bus"})
# turbines
g_dt1 = Bus("generator DT1 - 96")
g_dt2 = Bus("generator DT2 - 97")
g_dt3 = Bus("generator DT3 - 98")
g_dt4 = Bus("generator DT4 - 99")
g_dt5 = Bus("generator DT5 - 100")
g_dt1.add_comps({"comp": dt1, "char": 0.995*0.995, "base": "component"})
g_dt2.add_comps({"comp": dt2, "char": 0.995*0.995, "base": "component"})
g_dt3.add_comps({"comp": dt3, "char": 0.995*0.995, "base": "component"})
g_dt4.add_comps({"comp": dt4, "char": 0.995*0.995, "base": "component"})
g_dt5.add_comps({"comp": dt5, "char": 0.995*0.995, "base": "component"})
# together?
nw.add_busses(g_p2, g_p3, g_dt1, g_dt2, g_dt3, g_dt4, g_dt5, g_p1, g_p4)
# gas expander and compressor
g_v = Bus("generator v - 95")
g_v.add_comps({"comp": v, "char": 0.995*0.995, "base": "bus"})
g_exp = Bus("generator turbine")
g_exp.add_comps({"comp": exp, "char": 0.995*0.995, "base": "component"})
nw.add_busses(g_v, g_exp)


# set parameters
# in and out
# T and p for 35
# T and p and m for 14
# m for 88
# m for 75
# p for DT3 out

# hx
c36.set_attr(T=145, fluid=water_m)
# high p
c41.set_attr(T=220)
c42.set_attr(T=300)
c45.set_attr(T=470)
c46.set_attr(T=500)
c47.set_attr(T=540)
c48.set_attr(T=600, p=170)
# medium p
c54.set_attr(T=300)
c60.set_attr(T=450)
c61.set_attr(T=540)
c62.set_attr(T=600, p=34)
# low p
c58.set_attr(T=230)
c65.set_attr(p=4.5)
c66.set_attr(p=2)
# VD1 - high p
#c43.set_attr(x=0)
c43.set_attr(Td_bp=-5)
#c43.set_attr(Td_bp=-7.469)
c44.set_attr(Td_bp=8)
vd1.set_attr(ttd_l=15)
# VD2 - medium p (in 2 VD after splitter with no delta p for the new)
#c52.set_attr(x=0)
#c52.set_attr(Td_bp=-5)
c51.set_attr(Td_bp=-5)
#c52.set_attr(Td_bp=-6.708)
c53.set_attr(Td_bp=8)
vd2.set_attr(ttd_l=15)
# VD3
#c56.set_attr(x=0)
#c56.set_attr(Td_bp=-5)
c57.set_attr(Td_bp=8)
vd3.set_attr(ttd_l=15)
# pressure drop
vd_list = [vd1, vd2, vd3]
hx_list = [kvw, eco1, eco2, eco3, uh1, uh2, uh3, uh4, eco4, uh5, zuh1, zuh2, zuh3, uh6]
for vd in vd_list:
    vd.set_attr(pr1=0.997, pr2=0.97)
for hx in hx_list:
    hx.set_attr(pr1=0.998, pr2=0.99)
# turbines and pumps properties
dt1.set_attr(eta_s=0.9)
dt2.set_attr(eta_s=0.9)
dt3.set_attr(eta_s=0.9)
p2.set_attr(eta_s=0.9)
p3.set_attr(eta_s=0.9)


# fluids
c14.set_attr(m=829.55, p=1.051, T=636.4013, fluid=exhaust_m)
c35.set_attr(p=24.750, T=51.9423446094176)

# B
# T71, p71, T72, T73, T74
# p76, p80, p84
# p drop in hk
# ttd_l hk
# p69, p70, eta for dt4, dt5
c71.set_attr(T=65, p=14.5, fluid=water_m)
c72.set_attr(T=c71.T.val+22)
c73.set_attr(T=c72.T.val+22)
c74.set_attr(T=c73.T.val+11)
c76.set_attr(p=h_f.sat_p(c74.T.val+3))
c80.set_attr(p=h_f.sat_p(c73.T.val+3))
c84.set_attr(p=h_f.sat_p(c72.T.val+3))
hk1.set_attr(pr1=0.99, pr2=0.97)
hk2.set_attr(pr1=0.99, pr2=0.97)
hk3.set_attr(pr1=0.99, pr2=0.97)


#hk1.set_attr(Q=-80000000)
hk1.set_attr( ttd_l=3, Q=-80000000)
#hk1.set_attr( ttd_l=3)
hk2.set_attr(ttd_l=3)
hk3.set_attr(ttd_l=3)
#c77.set_attr(Td_bp=-5)
#c81.set_attr(Td_bp=-5)
#c85.set_attr(Td_bp=-5)
#c71.set_attr(m=864)

c69.set_attr(p=1)
# del c70.set_attr(p=0.022)
dt4.set_attr(eta_s=0.9)
dt5.set_attr(eta_s=0.9)

# C
# p91, T91, p92, T93
# p70=sat(T93+5) -> x=0 for c32 automatically
# p drop KON and VW
# p70
# 933
p1.set_attr(eta_s=0.9)
p4.set_attr(eta_s=0.9)
c91.set_attr(T=8, p=1.013, fluid=water_m)
c92.set_attr(p=1.5)
c93.set_attr(T=14)
kon.set_attr(pr1=1, pr2=0.6)
c33.set_attr(p=25)
vw.set_attr(pr1=0.99, pr2=0.99, ttd_l=10)



"""
-----
mixer for district heat - new structure
"""
nw.del_conns(c84,c82, c84m, c80, c78, c80m, c85, c81)
c84 = Connection(dr_ue6, 'out1', hk1, 'in1', label='84')
c85m = Connection( hk1, 'out1', mix_fw1, 'in2', label='85m')
c82 = Connection(dr_be3, 'out1', mix_fw1, 'in1', label='82')
c80 = Connection(dr_ue5, 'out1', hk2, 'in1', label='80')
c81m = Connection( hk2, 'out1', mix_fw2, 'in2', label='81m')
c78 = Connection(dr_be2, 'out1', mix_fw2, 'in1', label='78')
c81 = Connection(mix_fw2, 'out1', dr_be3, 'in1', label= '81')
c85 = Connection(mix_fw1, 'out1', vw, 'in1', label='85')
c80.set_attr(p=h_f.sat_p(c73.T.val+3))
c84.set_attr(p=h_f.sat_p(c72.T.val+3))
nw.add_conns(c84, c85m, c82, c80, c81m, c78, c81, c85)
"""
-----
"""

# with merge - before condenser
nw.del_conns(c70, c87, c86)
c86 = Connection(vw, 'out1', dr_be4, 'in1', label='86')
c87 = Connection(dr_be4, 'out1', mix_kon, 'in1', label='87')
c70 = Connection(dt5, 'out1', mix_kon, 'in2', label='70')
c70m = Connection(mix_kon, 'out1', kon, 'in1', label='70m')
c70.set_attr(p=h_f.sat_p(c93.T.val+5))
c70m.set_attr(fluid0=water_m)
nw.add_conns(c87, c70, c70m, c86)

# without brennstoffvorwärmung bvw
# nw.del_conns(c51, c88, c52)
# c51 = Connection(eco4, 'out2', vd2, 'in2', label='51')
# c51.set_attr(Td_bp=-5)
# nw.add_conns(c51)


"""
-----
gas turbine system
"""
air_m = h_f.humid_air(T=5, rh=75, air_n=air_n)
fuel_m = h_f.calc_mass_flow(fuel_n)
# V
v.set_attr(eta_s=0.90, pr=19)
c1.set_attr(m=803.961, p=1.013, T=5, fluid=air_m)
# Splitter V
c7.set_attr(m=138.743)
# BK
bk.set_attr(pr=0.95, eta=0.98, lamb=1.9)
c10.set_attr(p=19.258, T=5, fluid=fuel_m)
c13.set_attr(fluid0={"O2": 0.001})
# EXP
exp.set_attr(eta_s=0.90)
c14_gas.set_attr(p=1.051)

nw.del_conns(c14, c14_gas)
c14 = Connection(exp, 'out1', uh4, 'in1', label='14')
c14.set_attr(p=1.051)
nw.add_conns(c14)


# init_only= True for debugging
nw.check_network()
nw.check_conns()
# #nw.solve(mode="design")
# nw.solve(mode="design", init_path='C:/TU-Berlin/01_Masterarbeit/tespy_forked/saved_nw')
# nw.print_results()
"""
# nw.save_network('C:/TU-Berlin/01_Masterarbeit/tespy_forked/saved_nw/ccpp_export_nw')
# nw.save_connections('C:/TU-Berlin/01_Masterarbeit/tespy_forked/saved_nw/connections')
# nw.save_components('C:/TU-Berlin/01_Masterarbeit/tespy_forked/saved_nw/components')
# nw.save_busses('C:/TU-Berlin/01_Masterarbeit/tespy_forked/saved_nw/busses')
"""


""" +++ exergy analysis +++ """
# define ambient
Tamb = 4
pamb = 1.013

# ++define busses ++

# power
# already

# heat loss
heat_loss_bus = Bus('Heat loss BK')
heat_loss_bus.add_comps({'comp': bk, 'base':'bus', 'param': 'Qloss'})


# mass flow - difference
condenser_bus = Bus('Heated fluid')
condenser_bus.add_comps({'comp':so_91, 'base':'bus'}, {'comp': si_93})
district_heat_bus = Bus('Fernwärme')
district_heat_bus.add_comps({'comp':so_71, 'base':'bus'}, {'comp': si_74})
# mass flow - single
start_bus = Bus('Bus 35')
start_bus.add_comps({'comp': so_35, 'base': 'bus'})
end_bus = Bus('Bus 34')
end_bus.add_comps({'comp': si_34})
air_bus = Bus('Bus 1')
air_bus.add_comps({'comp': so_1, 'base': 'bus'})
heat_in_bus = Bus('Heat in')
heat_in_bus.add_comps({'comp': so_10, 'base':'bus'})
heat_out_bus = Bus('Heat out')
heat_out_bus.add_comps({'comp': si_31})

nw.add_busses(heat_in_bus, condenser_bus, district_heat_bus,
              start_bus,  end_bus, heat_loss_bus)

product = [g_dt1, g_dt2, g_dt3, g_dt4, g_dt5, district_heat_bus, g_exp]
fuel = [g_p1, g_p2, g_p3, g_p4,air_bus, heat_in_bus, start_bus, end_bus, g_v]
loss = [condenser_bus, heat_out_bus]


#nw.solve(mode="design")
nw.solve(mode="design", init_path='C:/TU-Berlin/01_Masterarbeit/tespy_forked/saved_nw')
nw.print_results()


ean = ExergyAnalysis(nw, E_P=product, E_F=fuel, E_L=loss)
exe_eco_input = {**h_f.costs_c, **h_f.costs_c_power, **h_f.costs_Z}
costs_iteration = {
'iterate': {'repeat':True, 'cycle_closer_start': so_35, 'cycle_closer_end': si_34, 'initial_c':{'c_therm': 10, 'c_mech': 10, 'c_chemical': 10} }
}
exe_eco_input = {**exe_eco_input, **costs_iteration}

ean.analyse(pamb=pamb, Tamb=Tamb,  Chem_Ex= ch_ex_d.stand_ch_exe_dict('Szargut1988'), Exe_Eco=exe_eco_input)
ean.print_results()
#h_f.export_tables(ean)
h_f.sankey_diagram(ean)



# h_f.power_costs(nw)
# network_result = ean.network_data.to_frame().transpose()
# ean.aggregation_data.drop(columns=['group'], inplace=True)
# path = 'C:/TU-Berlin/01_Masterarbeit/excel_read/'
# nw.results['Connection'].to_excel(path+'results_df/thermodynamics_conn'+'.xlsx')
# h_f.result_to_markdown(ean.component_data, path+'components_result', 'components')
# h_f.result_to_markdown(ean.connection_data, path+'connections_result', 'connections')
# h_f.result_to_markdown(ean.aggregation_data, path+'components_bus_result_agg', 'components_bus_agg')
# h_f.result_to_markdown(network_result, path+'network_result', 'network')

