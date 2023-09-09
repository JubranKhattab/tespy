from tespy.networks import Network
from tespy.components import (Source, Sink, Turbine)
from tespy.connections import Connection, Bus

# network
nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

# components
turb = Turbine("Turbine")
so = Source("Source")
si = Sink("Sink")

# Connections
so_2_turb = Connection(so, 'out1', turb, 'in1', label="Inlet")
turb_2_si = Connection(turb, 'out1', si, 'in1', label="Outlet")

nw.add_conns(so_2_turb, turb_2_si)

# define parameters
turb.set_attr(eta_s=0.9)
so_2_turb.set_attr(fluid={'Water': 1}, T=500, p=100,  m=5)
turb_2_si.set_attr(x=0.8)

# bus - generator
turb_bus = Bus('turbine to bus (generator)')
turb_bus.add_comps({'comp': turb, "char": 1, "base": "component"})
nw.add_busses(turb_bus)


# solve
nw.solve(mode='design')
nw.print_results()
print(turb.get_variables()['P'])
