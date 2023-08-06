from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchangerSimple)
from tespy.connections import Connection, Bus
from tespy.tools import analyses
import CoolProp.CoolProp as CP


"""
this heat exchanger takes cold water at the inlet 20 C und heat it up to 50 C.
I can define the heat amount in the component heat exchanger, because there is a parameter for this.
I can also add this heat with a bus. I this case I must delete the Q-Input in the component so that the system converges.
"""

def main_func():
        # network
        hx_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

        # components
        hx = HeatExchangerSimple("Heat Exchanger")
        so = Source("Source")
        si = Sink("Sink")

        # Connections
        so_2_hx = Connection(so, 'out1', hx, 'in1', label="Inlet")
        hx_2_si = Connection(hx, 'out1', si, 'in1', label="Outlet")

        hx_nw.add_conns(so_2_hx, hx_2_si)

        # define parameters
        #hx.set_attr(pr=1,  Q=+5000000)
        hx.set_attr(pr=1)

        heat_in_bus = Bus('heating')
        heat_in_bus.add_comps({'comp': hx})
        heat_in_bus.set_attr(P=+5000000)
        hx_nw.add_busses(heat_in_bus)

        so_2_hx.set_attr(fluid={'Water':1.0}, T=20, p=1)
        hx_2_si.set_attr(T=50)

        # solve
        hx_nw.solve(mode='design')
        hx_nw.print_results()


if __name__ == '__main__':
    main_func()
