from tespy.networks import Network
from tespy.components import (Turbine, Pump, Condenser, HeatExchanger, CycleCloser, Source, Sink)
from tespy.connections import Connection, Bus
import matplotlib.pyplot as plt
import numpy as np
from tespy.tools import ExergyAnalysis



# network
fluid_list = ['Water']
rankine_nw = Network(fluids=fluid_list)
rankine_nw.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

# components
turb = Turbine('turbine')
cond = Condenser('condenser')
so = Source('source')
so_hx = Source('source hot')
si = Sink('sink')
si_hx = Sink('sink hot')
pump = Pump('pump')
stm_gen = HeatExchanger('steam generator')
cc = CycleCloser('cycle closer')
cc_so = Source('source cycle closer')
cc_si = Sink('sink cycle closer')


# define connections and add to network
#conn_cc_turb = Connection(cc, 'out1', turb, 'in1', label='1')
conn_cc_so_turb = Connection(cc_so, 'out1', turb, 'in1', label='1')
conn_turb_cond = Connection(turb, 'out1', cond, 'in1', label='2')
conn_cond_pump = Connection(cond, 'out1', pump, 'in1', label='3')
conn_pump_stm_gen = Connection(pump, 'out1', stm_gen, 'in2', label='4')
#conn_stm_gen_cc = Connection(stm_gen, 'out2', cc, 'in1', label='0')
conn_stm_gen_cc_si = Connection(stm_gen, 'out2', cc_si, 'in1', label='0')

conn_so_hx = Connection(so_hx, 'out1', stm_gen, 'in1', label='13')
conn_si_hx = Connection(stm_gen, 'out1', si_hx, 'in1', label='14')

rankine_nw.add_conns(conn_cc_so_turb,
                     conn_turb_cond,
                     conn_cond_pump,
                     conn_pump_stm_gen,
                     conn_stm_gen_cc_si,
                     conn_so_hx,
                     conn_si_hx)


# define connections and add to network
conn_so_cond = Connection(so, 'out1', cond, 'in2', label='11')
conn_cond_si = Connection(cond, 'out2', si, 'in1', label='12')

rankine_nw.add_conns(conn_so_cond,
                     conn_cond_si)

# set the component and connection parameters.
# turbine
# m input, P output or the opposite
turb.set_attr(eta_s=0.95)
conn_cc_so_turb.set_attr(m=5, p=100, T=650, fluid={'Water': 1})
conn_turb_cond.set_attr(x=0.95)

# condenser
cond.set_attr(pr1=1, pr2=1)
conn_so_cond.set_attr(m=1000, p=1, T=20, fluid={'Water': 1})

# pump
conn_pump_stm_gen.set_attr(x=0)

# stm gen
stm_gen.set_attr(pr1=1, pr2=1)
conn_so_hx.set_attr(m=1000, p=50, T=800, fluid={'Water': 1})

conn_stm_gen_cc_si.set_attr( p=100, T=650)

# define ambient
T_amb = 20
p_amp = 1

# ++define busses types++

# power
# +select placeS (components) of bus type+
power_out = Bus('Power out turbine')
power_out.add_comps({'comp': turb, 'char':1, 'base': 'component'})

power_in= Bus('Power in pump')
power_in.add_comps({'comp': pump, 'char':1, 'base': 'bus'})

# heat
# +select placeS (components) of bus type+
heat_in = Bus('Heat in/out')
heat_in.add_comps({'comp': so_hx, 'base': 'bus'}, {'comp': si_hx})

cooling = Bus('Cooling water')
cooling.add_comps({'comp': so, 'base': 'bus'}, {'comp': si})

# mass flow
# +select placeS (components) of bus type+

# ++ add busses to network
rankine_nw.add_busses(power_out, heat_in, power_in, cooling)

# define ena and assign as P, F, L
ean = ExergyAnalysis(rankine_nw, E_F=[heat_in, power_in], E_P=[power_out], E_L=[cooling])



# solve
#rankine_nw.set_attr(iterinfo=False)  # disable the printout of the convergence history
rankine_nw.solve(mode='design')
rankine_nw.print_results()

ean.analyse(pamb=1, Tamb=15)
ean.print_results()



