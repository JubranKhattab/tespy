from tespy.networks import Network
from tespy.components import (Source, Sink, Compressor)
from tespy.connections import Connection, Bus
from tespy.tools import ExergyAnalysis
import plotly.graph_objects as go


# Network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# Components
compr = Compressor('Verdichter')
so = Source('Inlet')
si = Sink('Outlet')

# Connections
c_in = Connection(so, 'out1', compr, 'in1', 'c1')
c_out = Connection( compr, 'out1', si, 'in1', 'c2')

nw.add_conns(c_in, c_out)

# define parameters
c_in.set_attr(fluid={'Water': 1}, m=5, p=1.1, T=25)
c_out.set_attr(p=22)
compr.set_attr(eta_s=1)

nw.solve(mode='design')
nw.print_results()

""" +++ exergy analysis +++ """
# define ambient
T_amb = 20
p_amp = 1

# ++define busses types++

# power
# +select placeS (components) of bus type+
power = Bus('Power in')
power.add_comps({'comp': compr, 'char': 0.8, 'base': 'bus'})

# heat
# +select placeS (components) of bus type+

# mass flow
# +select placeS (components) of bus type+
mass_flow = Bus('water flow')
mass_flow.add_comps({'comp': so, 'base': 'bus'}, {'comp': si})


# ++ add busses to network
nw.add_busses(power)

# define ena and assign as P, F, L
ean = ExergyAnalysis(nw, E_F=[power], E_P=[mass_flow], E_L=[])

# do analysis
ean.analyse(pamb=p_amp, Tamb=T_amb)
ean.print_results()

# generate Grassmann diagram
# change display_thresold free
links, nodes = ean.generate_plotly_sankey_input(display_thresold=100)

# norm values to to E_F
links['value'] = [val / links['value'][0] for val in links['value']]

fig = go.Figure(go.Sankey(
    arrangement="snap",
    textfont={"family": "Linux Libertine O"},
    node={
        "label": nodes,
        'pad': 0,
        'color': 'orange'},
    link=links))
fig.show()

