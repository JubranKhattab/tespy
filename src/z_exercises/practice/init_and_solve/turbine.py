from tespy.networks import Network
from tespy.components import (Source, Sink, Turbine)
from tespy.connections import Connection

def main_func1():
        # network
        turbine_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

        # components
        turb = Turbine("Turbine")
        ausgang_hx = Source("ausgang_hx")
        eingang_condenser = Sink("eingang_condenser")

        # Connections
        dampf_conn = Connection(ausgang_hx, 'out1', turb, 'in1', label="Dampf Eintritt")
        condensate_conn = Connection(turb, 'out1', eingang_condenser, 'in1', label="Kondesat Austritt")

        turbine_nw.add_conns(dampf_conn,
                             condensate_conn)

        # define parameters
        turb.set_attr(eta_s=0.9)

        dampf_conn.set_attr(fluid={'Water': 1}, T=500, p=100,  m=5)
        condensate_conn.set_attr(x=0.8)

        # solve
        turbine_nw.solve(mode='design')
        turbine_nw.print_results()
        print(turb.get_variables()['P'].attr()['val'])


def main_func2():
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
        turb.set_attr(eta_s=0.9, P=-600000)#-6.74e+06

        so_2_turb.set_attr(fluid={'Water': 1}, T=500, p=100,  m=5)
        #turb_2_si.set_attr(x=0.8)

        # solve
        turbine_nw.solve(mode='design')
        turbine_nw.print_results()

if __name__ == '__main__':
    main_func1()
    # main_func2()
