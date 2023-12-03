from tespy.networks import Network
from tespy.components import (Turbine, Pump, Condenser, HeatExchangerSimple, CycleCloser, Source, Sink)
from tespy.connections import Connection, Bus
import matplotlib.pyplot as plt
import numpy as np
from tespy.tools import ExergyAnalysis


def easy_process():
    # network
    fluid_list = ['Water']
    rankine_nw = Network(fluids=fluid_list)
    rankine_nw.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

    # components
    turb = Turbine('turbine')
    cond = Condenser('condenser')
    so = Source('source')
    si = Sink('sink')
    pump = Pump('pump')
    stm_gen = HeatExchangerSimple('steam generator')
    cc = CycleCloser('cycle closer')

    # define connections and add to network
    conn_cc_turb = Connection(cc, 'out1', turb, 'in1', label='1')
    conn_turb_cond = Connection(turb, 'out1', cond, 'in1', label='2')
    conn_cond_pump = Connection(cond, 'out1', pump, 'in1', label='3')
    conn_pump_stm_gen = Connection(pump, 'out1', stm_gen, 'in1', label='4')
    conn_stm_gen_cc = Connection(stm_gen, 'out1', cc, 'in1', label='0')

    rankine_nw.add_conns(conn_cc_turb,
                         conn_turb_cond,
                         conn_cond_pump,
                         conn_pump_stm_gen,
                         conn_stm_gen_cc)


    # define connections and add to network
    conn_so_cond = Connection(so, 'out1', cond, 'in2', label='11')
    conn_cond_si = Connection(cond, 'out2', si, 'in1', label='12')

    rankine_nw.add_conns(conn_so_cond,
                         conn_cond_si)

    # set the component and connection parameters.
    # turbine
    # m input, P output or the opposite
    turb.set_attr(eta_s=0.9)
    conn_cc_turb.set_attr(m=5, p=65, T=400, fluid={'Water': 1})
    conn_turb_cond.set_attr(x=0.95)

    # condenser
    cond.set_attr(pr1=1, pr2=1)
    conn_so_cond.set_attr(m=1000, p=1, T=20, fluid={'Water': 1})

    # pump
    conn_pump_stm_gen.set_attr(x=0)
    stm_gen.set_attr(pr=1)

    #ean =1
    rankine_nw, ean = exergy_ana(rankine_nw, turb, cond, pump, stm_gen, so, si)
    return rankine_nw, ean


def analyze_process():
    """
    we will analyze the power production and the efficiency of the cycle, given constant steam mass flow and with
    varying values for the

    live steam pressure,
    live steam temperature and
    cooling water temperature level.
    """

    # network
    fluid_list = ['Water']
    rankine_nw = Network(fluids=fluid_list)
    rankine_nw.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

    # components
    turb = Turbine('turbine')
    cond = Condenser('condenser')
    so = Source('source')
    si = Sink('sink')
    pump = Pump('pump')
    stm_gen = HeatExchangerSimple('steam generator')
    cc = CycleCloser('cycle closer')

    # define connections and add to network
    conn_cc_turb = Connection(cc, 'out1', turb, 'in1', label='1')
    conn_turb_cond = Connection(turb, 'out1', cond, 'in1', label='2')
    conn_cond_pump = Connection(cond, 'out1', pump, 'in1', label='3')
    conn_pump_stm_gen = Connection(pump, 'out1', stm_gen, 'in1', label='4')
    conn_stm_gen_cc = Connection(stm_gen, 'out1', cc, 'in1', label='0')

    rankine_nw.add_conns(conn_cc_turb,
                         conn_turb_cond,
                         conn_cond_pump,
                         conn_pump_stm_gen,
                         conn_stm_gen_cc)

    # define connections and add to network
    conn_so_cond = Connection(so, 'out1', cond, 'in2', label='11')
    conn_cond_si = Connection(cond, 'out2', si, 'in1', label='12')

    rankine_nw.add_conns(conn_so_cond,
                         conn_cond_si)

    # set the component and connection parameters.
    # turbine
    # m input, P output or the opposite
    turb.set_attr(eta_s=0.90) #
    conn_cc_turb.set_attr(m=10, p=150, T=600, fluid={'Water': 1}) #
    conn_turb_cond.set_attr(p=0.1) #
    # conn_turb_cond.set_attr(x=0.95)

    # condenser
    cond.set_attr(pr1=1, pr2=1, ttd_u = 10) #
    conn_so_cond.set_attr(p=1.2, T=20, fluid={'Water': 1})  #
    # conn_cond_si.set_attr(T=30) #

    # pump
    pump.set_attr(eta_s=0.75) #
    # conn_pump_stm_gen.set_attr(x=0)

    # steam generator
    stm_gen.set_attr(pr=1) #

    rankine_nw, powergen = exergy_ana(rankine_nw, turb, pump)

    """
     ### from here starts the analysis ###
     """

    data, eta, power = define_data()

    """ case 1:T steam is variable. p steam and T cooling constant """
    # for T in data['T_livesteam']:
    #     conn_cc_turb.set_attr(T=T)
    #     rankine_nw.solve('design')
    #     eta['T_livesteam'] += [abs(powergen.P.val) / stm_gen.Q.val * 100]
    #     power['T_livesteam'] += [abs(powergen.P.val) / 1e6]

    """ case 2:T cooling is variable. T steam and p steam constant """
    conn_cc_turb.set_attr(T=600)
    for T in data['T_cooling']:
        conn_so_cond.set_attr(T=T)
        rankine_nw.solve('design')
        eta['T_cooling'] += [abs(powergen.P.val) / stm_gen.Q.val * 100]
        power['T_cooling'] += [abs(powergen.P.val) / 1e6]

    return rankine_nw


def define_data():
    data = {
        'T_livesteam': np.linspace(450, 750, 7),
        'T_cooling': np.linspace(15, 45, 7),
        'p_livesteam': np.linspace(75, 225, 7)
    }
    eta = {
        'T_livesteam': [],
        'T_cooling': [],
        'p_livesteam': []
    }
    power = {
        'T_livesteam': [],
        'T_cooling': [],
        'p_livesteam': []
    }
    return data, eta, power


def exergy_ana(rankine_nw, turb, cond, pump, stm_gen,so, si):
    # define ambient
    T_amb = 20
    p_amp = 1

    # ++define busses types++

    # power
    # +select placeS (components) of bus type+
    power_net = Bus('Power netto')
    power_net.add_comps({'comp': turb, 'char':1, 'base': 'component'},
                    {'comp': pump, 'char':1, 'base': 'bus'})
    #### test differnet busses

    # heat
    # +select placeS (components) of bus type+
    heat_in = Bus('Heat in')
    heat_in.add_comps({'comp': stm_gen})

    cooling = Bus('Cooling water')
    cooling.add_comps({'comp': so, 'base': 'bus'}, {'comp': si})

    # mass flow
    # +select placeS (components) of bus type+

    # ++ add busses to network
    rankine_nw.add_busses(power_net, heat_in, cooling)

    # define ena and assign as P, F, L
    ean = ExergyAnalysis(rankine_nw, E_F=[heat_in], E_P=[power_net], E_L=[cooling])

    return rankine_nw, ean


def solve(rankine_nw, ean):
    # solve
    rankine_nw.set_attr(iterinfo=False)  # disable the printout of the convergence history
    rankine_nw.solve(mode='design')
    rankine_nw.print_results()

    ean.analyse(pamb=1, Tamb=15)
    ean.print_results()


if __name__ =='__main__':
    rankine_nw, ean = easy_process()
    # rankine_nw = analyze_process()
    solve(rankine_nw, ean)
