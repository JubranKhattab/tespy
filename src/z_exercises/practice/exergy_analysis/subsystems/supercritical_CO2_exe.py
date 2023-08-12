from tespy.networks import Network
from tespy.components import (
    Sink, Source, Turbine, Condenser, HeatExchangerSimple, Merge, Splitter,
    Valve, HeatExchanger, CycleCloser, Compressor)
from tespy.connections import Connection, Bus, Ref
from tespy.tools import CharLine
from tespy.tools import document_model
import pandas as pd
import numpy as np
from tespy.tools import ExergyAnalysis

import plotly.graph_objects as go

fmt_dict = {
    'E_F': {
        'unit': ' in MW',
        'float': '{:.2f}',
        'factor': 1e6,
    },
    'E_P': {
        'unit': ' in MW',
        'float': '{:.2f}',
        'factor': 1e6,
    },
    'E_D': {
        'unit': ' in MW',
        'float': '{:.2f}',
        'factor': 1e6,
    },
    'E_L': {
        'unit': ' in MW',
        'float': '{:.2f}',
        'factor': 1e6,
    },
    'epsilon': {
        'unit': ' in %',
        'float': '{:.1f}',
        'factor': 1 / 100,
        'markdown_header': 'ε'
    },
    'y_Dk': {
        'unit': ' in %',
        'float': '{:.1f}',
        'factor': 1 / 100
    },
    'y*_Dk': {
        'unit': ' in %',
        'float': '{:.1f}',
        'factor': 1 / 100
    },
    'e_T': {
        'unit': ' in kJ/kg',
        'float': '{:.1f}',
        'factor': 1000
    },
    'e_M': {
        'unit': ' in kJ/kg',
        'float': '{:.1f}',
        'factor': 1000
    },
    'e_PH': {
        'unit': ' in kJ/kg',
        'float': '{:.1f}',
        'factor': 1000
    },
    'E_T': {
        'unit': ' in MW',
        'float': '{:.2f}',
        'factor': 1e6
    },
    'E_M': {
        'unit': ' in MW',
        'float': '{:.2f}',
        'factor': 1e6
    },
    'E_PH': {
        'unit': ' in MW',
        'float': '{:.2f}',
        'factor': 1e6
    },
    'T': {
        'unit': ' in °C',
        'float': '{:.1f}',
        'factor': 1
    },
    'p': {
        'unit': ' in bar',
        'float': '{:.2f}',
        'factor': 1
    },
    'h': {
        'unit': ' in kJ/kg',
        'float': '{:.1f}',
        'factor': 1
    }
}

# specification of ambient state
pamb = 1.01325
Tamb = 15


# setting up network
nw = Network(fluids=['CO2'])
nw.set_attr(
    T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s',
    s_unit="kJ / kgK")

# components definition
water_in = Source('Water source')
water_out = Sink('Water sink')

closer = CycleCloser('Cycle closer')

cp1 = Compressor('Compressor 1', fkt_group='CMP')
cp2 = Compressor('Compressor 2', fkt_group='CMP')

rec1 = HeatExchanger('Recuperator 1', fkt_group='REC')
rec2 = HeatExchanger('Recuperator 2', fkt_group='REC')

cooler = HeatExchangerSimple('Water cooler')
heater = HeatExchangerSimple('Heater')

turb = Turbine('Turbine')

sp1 = Splitter('Splitter 1', fkt_group='REC')
m1 = Merge('Merge 1', fkt_group='REC')

# connections definition
# power cycle
c1 = Connection(cooler, 'out1', cp1, 'in1', label='1')
c2 = Connection(cp1, 'out1', rec1, 'in2', label='2')
c3 = Connection(rec2, 'out2', heater, 'in1', label='3')

c0 = Connection(heater, 'out1', closer, 'in1', label='0')
c4 = Connection(closer, 'out1', turb, 'in1', label='4')
c5 = Connection(turb, 'out1', rec2, 'in1', label='5')
c6 = Connection(sp1, 'out1', cooler, 'in1', label='6')

c10 = Connection(sp1, 'out2', cp2, 'in1', label='10')
c11 = Connection(cp2, 'out1', m1, 'in2', label='11')
c12 = Connection(rec1, 'out2', m1, 'in1', label='12')
c13 = Connection(m1, 'out1', rec2, 'in2', label='13')

c14 = Connection(rec2, 'out1', rec1, 'in1', label='14')
c15 = Connection(rec1, 'out1', sp1, 'in1', label='15')

# add connections to network
nw.add_conns(c0, c1, c2, c3, c4, c5, c6, c10, c11, c12, c13, c14, c15)

# power bus
power = Bus('total output power')
power.add_comps({'comp': turb, 'char': 0.99 * 0.99, 'base': 'component'},
                {'comp': cp1, 'char': 0.98 * 0.97, 'base': 'bus'},
                {'comp': cp2, 'char': 0.98 * 0.97, 'base': 'bus'})

heat_input_bus = Bus('heat input')
heat_input_bus.add_comps({'comp': heater, 'base': 'bus'})

nw.add_busses(power, heat_input_bus)

# connection parameters
c1.set_attr(T=35, p=75, fluid={'CO2': 1}, m=10)
c2.set_attr(p=258.4)
c3.set_attr(p=257, T=433.63)
c4.set_attr(T=600, p=250)
c5.set_attr(p=77.95)
c6.set_attr(p=75.15, T=128.26)
c11.set_attr(p=257.51)
c14.set_attr(p=76.94, T=269.11)

# component parameters
turb.set_attr(eta_s=0.9)
cp1.set_attr(eta_s=0.85)
cp2.set_attr(eta_s=0.85)
# rec1.set_attr(ttd_u=5)

# solve final state
nw.solve(mode='design')
rec2.set_attr(ttd_l=5)
rec1.set_attr(ttd_l=5)
c11.set_attr(T=Ref(c12, 1, 0))
c3.set_attr(T=None)
c6.set_attr(T=None)
c14.set_attr(T=None)
c1.set_attr(m=None)
power.set_attr(P=-100e6)
nw.solve(mode='design')
# print results to prompt and generate model documentation
nw.print_results()

# carry out exergy analysis
ean = ExergyAnalysis(nw, E_P=[power], E_F=[heat_input_bus])
ean.analyse(pamb=pamb, Tamb=Tamb)

# print exergy analysis results to prompt
ean.print_results()
