from tespy.networks import Network
from tespy.components import (Source, Pump, Turbine, Sink, Valve, Merge, Splitter, HeatExchanger)
from tespy.connections import Connection, Bus
import help_func as h_f

# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

exhaust_m = h_f.exhaust_m
air_n = h_f.air_n
fuel_n = h_f.fuel_n
water_m = h_f.water_m

# components
so_14 = Source('Source 14')
si_31 = Sink('Sink 31')
so_35 = Source('Source 35')
si_75 = Sink('Sink 75')
si_66 = Sink('Sink 66')
si_88 = Sink('Sink 88')
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

c35 = Connection(so_35, 'out1', kvw, 'in2', label='35')
c36 = Connection(kvw, 'out2', spl_kvw, 'in1', label='36')
c55 = Connection(spl_kvw, 'out1', dr_ue3, 'in1', label='55')
c37 = Connection(spl_kvw, 'out2', p2, 'in1', label='37')
# low p - conn
c56 = Connection(dr_ue3, 'out1', vd3, 'in2', label='56')
c57 = Connection(vd3, 'out2', uh6, 'in2', label='57')
c58 = Connection(uh6, 'out2', mix_dt3, 'in1', label='58')
c63 = Connection(dt2, 'out1', spl_fw3, 'in1', '63')
c64 = Connection(spl_fw3, 'out2', mix_dt3, 'in2', '64')
c65 = Connection(mix_dt3, 'out1', dt3, 'in1', '65')
c75 = Connection(spl_fw3, 'out1', si_75, 'in1', '75')
c66 = Connection(dt3, 'out1', si_66, 'in1', label='66')
# medium p - conn
c39 = Connection(spl_p2, 'out2', p3, 'in1', label='39')
c38 = Connection(p2, 'out1', spl_p2, 'in1', label='38')
c50 = Connection(spl_p2, 'out1', eco4, 'in2', label='50')
c51 = Connection(eco4, 'out2', spl_bvw, 'in1', label='51')
c88 = Connection(spl_bvw, 'out1', si_88, 'in1', label='88')
c52 = Connection(spl_bvw, 'out2', vd2, 'in2', label='52')
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

# add connections
nw.add_conns(c35, c36, c55, c56, c57, c58, c37, c38, c39, c50, c51, c88, c52, c53, c54, c59, c60, c61, c62, c49, c63, c75, c64, c65, c66,
             c40, c41, c42, c43, c44, c45, c46, c47, c48, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31
)

# busses
# pumps
g_p2 = Bus("generator P2 - 102")
g_p2.add_comps({"comp": p2, "char": 1.0, "base": "bus"})
g_p3 = Bus("generator P3 - 103")
g_p3.add_comps({"comp": p2, "char": 1.0, "base": "bus"})
# turbines
g_dt1 = Bus("generator DT1 - 96")
g_dt2 = Bus("generator DT2 - 97")
g_dt3 = Bus("generator DT3 - 98")
g_dt1.add_comps({"comp": dt1, "char": 0.995*0.995, "base": "component"})
g_dt2.add_comps({"comp": dt2, "char": 0.995*0.995, "base": "component"})
g_dt3.add_comps({"comp": dt3, "char": 0.995*0.995, "base": "component"})
# together?
nw.add_busses(g_p2, g_p3, g_dt1, g_dt2, g_dt3)


# set parameters
# in and out
# T and p for 35
# T and p and m for 14
# m for 88
# m for 75
# p for DT3 out

# hx
c36.set_attr(T=145)
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
#c43.set_attr(Td_bp=-7.24)
c44.set_attr(Td_bp=8)
vd1.set_attr(ttd_l=15)
# VD2 - medium p (in 2 VD after splitter with no delta p for the new)
#c52.set_attr(x=0)
c52.set_attr(Td_bp=-5)
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
# splitter
c88.set_attr(m=12.82)
c75.set_attr(m=15.23)
# fluids
c14.set_attr(m=868.06, p=1.051, T=644.51, fluid=exhaust_m)
c35.set_attr(p=24.750, T=40.19, fluid=water_m)

nw.solve(mode="design")
nw.print_results()


