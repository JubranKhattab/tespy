# -*- coding: utf-8

"""Module for class Source.


This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location tespy/components/basics/source.py

SPDX-License-Identifier: MIT
"""

import numpy as np

from tespy.components.component import Component


class Source(Component):
    r"""
    A flow originates from a Source.

    Parameters
    ----------
    label : str
        The label of the component.

    design : list
        List containing design parameters (stated as String).

    offdesign : list
        List containing offdesign parameters (stated as String).

    design_path : str
        Path to the components design case.

    local_offdesign : boolean
        Treat this component in offdesign mode in a design calculation.

    local_design : boolean
        Treat this component in design mode in an offdesign calculation.

    char_warnings : boolean
        Ignore warnings on default characteristics usage for this component.

    printout : boolean
        Include this component in the network's results printout.

    Example
    -------
    Create a source and specify a label.

    >>> from tespy.components import Source
    >>> so = Source('a labeled source')
    >>> so.component()
    'source'
    >>> so.label
    'a labeled source'
    """

    @staticmethod
    def component():
        return 'source'

    @staticmethod
    def outlets():
        return ['out1']

    @staticmethod
    def get_mandatory_constraints():
        return {}

    def propagate_fluid_to_source(self, outconn, start):
        r"""
        Fluid propagation to source stops here.

        Parameters
        ----------
        outconn : tespy.connections.connection.Connection
            Connection to initialise.

        start : tespy.components.component.Component
            This component is the fluid propagation starting point.
            The starting component is saved to prevent infinite looping.
        """
        return

    def exergy_balance(self, T0):
        r"""Exergy balance calculation method of a source.

        A source does not destroy or produce exergy. The value of
        :math:`\dot{E}_\mathrm{bus}` is set to the exergy of the mass flow to
        make exergy balancing methods more simple as in general a mass flow can
        be fuel, product or loss.

        Parameters
        ----------
        T0 : float
            Ambient temperature T0 / K.

        Note
        ----
        .. math::

            \dot{E}_\mathrm{bus} = \dot{E}_\mathrm{out}^\mathrm{PH}
        """
        self.E_P = np.nan
        self.E_F = np.nan
        self.E_bus = {
            "chemical": self.outl[0].Ex_chemical,
            "physical": self.outl[0].Ex_physical,
            "massless": 0
        }
        self.E_D = np.nan
        self.epsilon = np.nan

    def assign_eco_values_conn_to_comp(self):
        r"""
        Write all the calculated values from the exergy economic balance to be attributes of the components.
        That will be used at the end to check that values match.

        Parameters
        ----------

        """
        # declare variables to the component
        c_per_unit, E_streams_tot, C_streams = {}, {}, {}
        self.exe_eco = {'C_streams': {}, 'c_per_unit': {}, 'E_streams_tot': {}}

        # help Dictionary
        dict_dicts = {'c_per_unit': c_per_unit, 'E_streams_tot': E_streams_tot, 'C_streams': C_streams}

        # read input values an assign them to the component.
        for conn in self.inl:
            # read c from inlet
            cost_id = f"c_cost_{conn.target_id}"
            c_per_unit[cost_id] = conn.c_cost

            # read and calculate E from inlet
            E_id = f"E_TOT_{conn.target_id}"
            E_streams_tot[E_id] = conn.Ex_physical + conn.Ex_chemical

            # calculate C
            C_id = f"C_{conn.target_id}"
            C_streams[C_id] = c_per_unit[cost_id]*E_streams_tot[E_id]

        for conn in self.outl:
            # declare c for outlet
            cost_id = f"c_cost_{conn.source_id}"
            c_per_unit[cost_id] = conn.c_cost

            # read and calculate E from outlet
            E_id = f"E_TOT_{conn.source_id}"
            E_streams_tot[E_id] = conn.Ex_physical + conn.Ex_chemical

            # declare C for outlet
            C_id = f"C_{conn.source_id}"
            C_streams[C_id] = c_per_unit[cost_id] * E_streams_tot[E_id]

        # add all variables {c, C, E} as attributes for the components.
        for d in list(dict_dicts.values()):
            dict_name = list(dict_dicts.keys())[list(dict_dicts.values()).index(d)]
            for key, value in d.items():
                self.exe_eco[f"{dict_name}"][f"{key}"] = value

    def exergy_economic_balance(self,Exe_Eco):
        r"""
        declare and prepare component's variables c, E, C and Z and calculate exergy economics balance of a component.
        A Source does not destroy or produce exergy. No exergy economic balance is necessary.
        All exergy economic outputs of the Source are inputs for the network and should be known und defined

        c: cost per exergy unit to every connection.
        E: Sum of exergy streams to each inlet and outlet connection.
        C: Cost stream to every connection.

        For inlets:
            no inlets

        For outlets:
            E is calculated previously in connection functions
            C is calculated by Exergy-Costing principle
            c is entered in the network.

        Units
            c [ / GJ]
            E [ W ]
            C [ / h]

        Parameters
        ----------
        Exe_Eco: dict
            Contains c for all sources as well as all Z for every component or component group in the network.

        Note
        ----
        Requirement: all necessary input variables are known and calculated previously.
            input variables: Z, E, c and C for all inlets


        """
        "++Input++"
        # assign Z to be an attribute for the component
        Z_id = f"{self.label}_Z"
        self.Z_costs = Exe_Eco[f"{Z_id}"]

        "++Output++"
        # calculate outlet
        self.outl[0].Ex_tot = self.outl[0].Ex_physical + self.outl[0].Ex_chemical
        self.outl[0].C_stream = self.outl[0].c_cost * self.outl[0].Ex_tot * (3600/10**9)

        # conn calculated
        self.outl[0].eco_check = True

    def calculate_comp_variables(self, T0):
        # C_F, C_P
        self.C_F = np.nan
        self.C_P = np.nan

        # add c_F c_P, C_D, r and f
        self.c_F = self.C_F / self.E_F
        self.c_P = self.C_P / self.E_P
        self.C_D = self.c_F * self.E_D
        self.r = (self.c_P - self.c_F) / self.c_F
        self.f = self.Z_costs / (self.Z_costs + self.C_D)


