from tespy.networks import Network
from tespy.components import (Source, Compressor, DiabaticCombustionChamber, Turbine, Sink, Valve, Merge, Splitter, HeatExchanger)
from tespy.connections import Connection, Ref, Bus
from CoolProp.CoolProp import PropsSI as PSI
from tespy.tools.helpers import mass_flow
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import pandas as pd

# network
fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2", "ethane", "C3H8", "n-Butane", "n-Pentane", "n-Hexane"]
nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

# components
hx_vw_br = HeatExchanger("Brennstoff Vorwärmer")
exp = Turbine('EXP')
ac = Compressor('AC')
spl = Splitter('Split')
tv1 = Valve('TV1')
# tv2 = Valve('TV2')
# m_lambda = Merge('lambda')
m_tit = Merge('TIT')
sc = DiabaticCombustionChamber('Stoichiometric combustion')
c1 = Source('Air')
c14 = Sink('Exaust')
c10 = Source('Fuel')
c9 = Source('cold Fuel')
sink_abgas = Sink("Sink Abgas")
sink_cooling = Sink("Sink Cooling")
sink_spliter = Sink("Sink Splitter")
sink_merge_tit = Sink("Sink Mix tit")
so_w = Source("A")
si_w = Sink("B")

# connections
so_to_comp = Connection(c1, 'out1', ac, 'in1', label='1')
comp_to_split = Connection(ac, 'out1', spl, 'in1', label='2')
split_to_sc = Connection(spl, 'out1', sc, 'in1', label='3')
split_to_tv1 = Connection(spl, 'out2', tv1, 'in1', label='7')

# later
sc_to_m_tit = Connection(sc, 'out1', m_tit, 'in1', label='12')
tv1_to_m_tit = Connection(tv1, 'out1', m_tit, 'in2', label='8')
#m_tit_to_sink = Connection(m_tit, 'out1', sink_merge_tit, 'in1', label='13')

# later 2
m_tit_to_exp = Connection(m_tit, 'out1', exp, 'in1', label='13')
exp_to_exit = Connection(exp, 'out1', c14, 'in1', label='14')

so_fuel_hx = Connection(c9, 'out1', hx_vw_br, 'in2', label='9')
fuel_to_sc = Connection(hx_vw_br, 'out2', sc, 'in2', label='10')
c_88 = Connection(so_w, 'out1', hx_vw_br, 'in1', label='88')
c_89 = Connection(hx_vw_br, 'out1', si_w, 'in1', label='89')



# nw.add_conns(so_to_comp,comp_to_split, split_to_sc, split_to_tv1, sc_to_m_tit, tv1_to_m_tit, m_tit_to_exp, exp_to_exit, fuel_to_sc)
nw.add_conns(so_to_comp,comp_to_split, split_to_sc, sc_to_m_tit, split_to_tv1, tv1_to_m_tit, fuel_to_sc, m_tit_to_exp, exp_to_exit, so_fuel_hx, c_88, c_89)

#
generator = Bus("generator")
generator.add_comps(
    {"comp": exp, "char": 0.995*0.995, "base": "component"},  # 99.5 % mech. ele. efficiency
    {"comp": ac, "char": 0.995*0.995, "base": "bus"},  # 99.5 % mech. ele. efficiency
)


generator_v = Bus("generator compressor")
generator_v.add_comps(
    {"comp": ac, "char": 0.995*0.995, "base": "bus"},  # 99.5 % mech. ele. efficiency
)

generator_t = Bus("generator turbine")
generator_t.add_comps(
    {"comp": exp, "char": 0.995*0.995, "base": "component"},)


#generator_v.set_attr(P=+3.48e8)
nw.add_busses(generator)
#nw.add_busses(generator_v, generator_t)
# total 400 instead of mass flow as input

# parameters
# air source
air_0= {
        "CO2": 0.00027, "ethane": 0, "N2": 0.78092,
        "C3H8": 0, "CH4": 0,  "O2": 0.20947, "H2O":0,
        "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0,
        "Ar":0.00934, "H2": 0
    }

psatH2O = PSI('P', 'Q', 0, 'T', 5+273.15, 'water') * 0.00001
rh = 75
pH2O = float(rh) / 100 * psatH2O

xH2O = PSI('M', 'water') * (pH2O / 1.013) / (
    pH2O/1.013 * PSI('M', 'water') + (1 - pH2O/1.013) * PSI('M', 'air'))

air_0 = {key: value * (1-xH2O) for key, value in air_0.items()}
air_0['H2O'] = xH2O
air_0 = mass_flow(air_0)

so_to_comp.set_attr(m=790,
    p=1.013, T=5,
    fluid=air_0
)

# Fuel
fuel_n = {
        "CO2": 0.01800, "ethane": 0.03600, "N2": 0.10300,
        "C3H8": 0.00600, "CH4": 0.83380,  "O2": 0.000010, "H2O":0,
        "n-Butane": 0.00200, "n-Pentane": 0.00050, "n-Hexane": 0.00069,
        "Ar":0, "H2": 0
    }
fuel = mass_flow(fuel_n)
fuel_to_sc.set_attr(p=19.247,
                    T=195,
    fluid=fuel
)

# vorwärmer
water = {
        "CO2": 0, "ethane": 0, "N2": 0,
        "C3H8": 0, "CH4": 0,  "O2": 0, "H2O":1,
        "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0,
        "Ar":0, "H2": 0
    }

hx_vw_br.set_attr(pr1=0.99, pr2=0.998)
so_fuel_hx.set_attr(T=5)
c_88.set_attr(p=36.442, T=238.18, fluid=water)
c_89.set_attr( T=40)

# Chamber
sc.set_attr(pr=0.95, eta=0.98, lamb=1.9)
#sc_to_sink.set_attr(T=1700)

# # TIT
# m_tit_to_exp.set_attr(T=1340)

# compressor
ac.set_attr(eta_s=0.90, pr=19)

# # expander
exp.set_attr(eta_s=0.90)
exp_to_exit.set_attr(p=1.051)

# splitter
split_to_tv1.set_attr(m=132)
#m_tit_to_exp.set_attr(T=1340)


# valve
#tv1.set_attr(pr=1)

# starting values for out
m_tit_to_exp.set_attr(fluid0={"O2": 0.001})

# solve
nw.solve(mode="design")
nw.print_results()

"""
print("m Luft: ",round(so_to_comp.m.val ,2))
print("m Mischung: ",round(split_to_tv1.m.val, 2))
print("m brennstoff: ",round(fuel_to_sc.m.val,2))
print("m T13: ",round(m_tit_to_exp.T.val,2))
print("m P-Netto: ",round(-generator.P.val/100000000,2))


plt.rc('font', **{'size': 18})
data = {
    'm_luft': np.linspace(750, 850, 11),
    'm_mischung': np.linspace(150, 150, 1)
}

T_13 = {
    'm_luft': [],
    'm_mischung': []
}
net_power = {
    'm_luft': [],
    'm_mischung': []
}

x_aches = []

for m_m in data['m_mischung']:
    for m_l in data['m_luft']:
        so_to_comp.set_attr(m=m_l)
        split_to_tv1.set_attr(m=m_m)
        nw.solve('design')
        x_aches.append(str(round(m_l)) )
        T_13['m_luft'] += [round(m_tit_to_exp.T.val,2)]
        net_power['m_luft'] += [round(-generator.P.val/1000000,2)]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Plot on the first subplot (x, y1)
x_aches = [s.replace('.', ',') for s in x_aches]
ax1.plot(x_aches, T_13['m_luft'], 'b-', label='T13',marker='x', linewidth=2)
ax1.axhline(y=1340, color='green', linestyle='--')
ax1.set_xlabel('kg/s')
ax1.set_ylabel('°C')
ax1.legend()

# Plot on the second subplot (x, y2)
ax2.plot(x_aches, net_power['m_luft'], 'r-', label='Netto-P',marker='o', linewidth=2)
ax2.axhline(y=400, color='purple', linestyle='--')
ax2.set_xlabel('kg/s')
ax2.set_ylabel('MW')
ax2.legend()
ax1.set_xticks(x_aches[::2])
ax2.set_xticks(x_aches[::2])


fig.text(0.5, 0.02, 'Angesaugter Luftstrom (1) ', ha='center', fontsize=12)
fig.suptitle('Konstanter Teilluftstrom (7) = 150 kg/s')

plt.savefig('C:/TU-Berlin/01_Masterarbeit/Bilder_tespy/hauptmassenstrom_T_P.png')
plt.close()

"""

#
# # Create a figure and axis
# fig, ax1 = plt.subplots()
#
# # Plot data on the left y-axis
# ax1.plot(x_aches, T_13['m_mischung'], color='blue', marker='o', label='T13')
# ax1.axhline(y=1340, color='green', linestyle='--', label='1340')
# ax1.set_xlabel('X-axis')
# ax1.set_ylabel('Left Y-axis', color='blue')
# ax1.tick_params('y', colors='blue')
#
# # Create a twin axis for the right y-axis
# ax2 = ax1.twinx()
#
# # Plot data on the right y-axis
# ax2.plot(x_aches, net_power['m_mischung'], color='red', marker='x', label='Power')
# ax2.axhline(y=4, color='purple', linestyle='--', label='4')  # Add line at y=4
# ax2.set_ylabel('Right Y-axis', color='red')
# ax2.tick_params('y', colors='red')

#
# plt.savefig('C:/TU-Berlin/01_Masterarbeit/Bilder_tespy/T_P_one.png')
# plt.close()

# Find indices where y_values equal to 4
# indices = [i for i, y in enumerate(net_power['m_mischung']) if y == 4]
#
# # Get corresponding x_values
# result_x_values = [x_aches[i] for i in indices]
#
# print(result_x_values)
#
# print('end')

# for m in data['m_luft']:
#     so_to_comp.set_attr(m=m)
#     nw.solve('design')
#     T_13['m_luft'] += [round(m_tit_to_exp.T.val,2)]
#     net_power['m_luft'] += [round(-generator.P.val/100000000,2)]

#
# fig, ax = plt.subplots(2, 2, figsize=(16, 8), sharex='col', sharey='row')
# ax = ax.flatten()
# [a.grid() for a in ax]
#
# i = 0
# for key in data:
#     ax[i].scatter(data[key], T_13[key], s=100, color="#1f567d")
#     ax[i + 2].scatter(data[key], net_power[key], s=100, color="#18a999")
#     i += 1
#
# ax[0].set_ylabel('TIT ISO - T13')
# ax[2].set_ylabel('Power ')
# ax[2].set_xlabel('m Luft')
# ax[3].set_xlabel('m Mischung')
#
# plt.tight_layout()
# fig.savefig("""C:/TU-Berlin/01_Masterarbeit/Bilder_tespy/tit_iso.png""")
# plt.close()
