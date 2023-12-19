from tespy.networks import Network
from tespy.components import (Source, Sink, Turbine)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
import plotly.graph_objects as go
from z_exercises.practice.exergy_analysis import standard_chem_exergy as ch_ex_d


# network
turbine_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
turb = Turbine("Turbine")
so = Source("Source")
si = Sink("Sink")

# Connections
so_2_turb = Connection(so, 'out1', turb, 'in1', label="Inlet")
turb_2_si = Connection(turb, 'out1', si, 'in1', label="Outlet")

turbine_nw.add_conns(so_2_turb,
                     turb_2_si)

# define parameters
turb.set_attr(eta_s=0.9)

so_2_turb.set_attr(fluid={'Water': 1}, T=600, p=34,  m=20)
turb_2_si.set_attr(p=4.5)


# solve network with busses but without exergy analyses
turbine_nw.solve(mode='design')
turbine_nw.print_results()









