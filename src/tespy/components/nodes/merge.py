# -*- coding: utf-8

"""Module of class Merge.


This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location tespy/components/nodes/merge.py

SPDX-License-Identifier: MIT
"""

import numpy as np

from tespy.components.nodes.base import NodeBase
from tespy.tools.data_containers import DataContainerSimple as dc_simple
from tespy.tools.document_models import generate_latex_eq
from tespy.tools.fluid_properties import s_mix_pT
from tespy.tools.helpers import num_fluids


class Merge(NodeBase):
    r"""
    Class for merge points with multiple inflows and one outflow.

    **Mandatory Equations**

    - :py:meth:`tespy.components.nodes.base.NodeBase.mass_flow_func`
    - :py:meth:`tespy.components.nodes.base.NodeBase.pressure_equality_func`
    - :py:meth:`tespy.components.nodes.merge.Merge.fluid_func`
    - :py:meth:`tespy.components.nodes.merge.Merge.energy_balance_func`

    Inlets/Outlets

    - specify number of outlets with :code:`num_in` (default value: 2)
    - out1

    Image

    .. image:: /api/_images/Merge.svg
       :alt: flowsheet of the merge
       :align: center
       :class: only-light

    .. image:: /api/_images/Merge_darkmode.svg
       :alt: flowsheet of the merge
       :align: center
       :class: only-dark

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

    num_in : float, dict
        Number of inlets for this component, default value: 2.

    Example
    -------
    The merge mixes a specified number of mass flows and has a single outlet.
    At the outlet, fluid composition and enthalpy are calculated by mass
    weighted fluid composition and enthalpy of the inlets.

    >>> from tespy.components import Sink, Source, Merge
    >>> from tespy.connections import Connection
    >>> from tespy.networks import Network
    >>> import shutil
    >>> import numpy as np
    >>> fluid_list = ['O2', 'N2']
    >>> nw = Network(fluids=fluid_list, p_unit='bar', iterinfo=False)
    >>> so1 = Source('source1')
    >>> so2 = Source('source2')
    >>> so3 = Source('source3')
    >>> si1 = Sink('sink')
    >>> m = Merge('merge', num_in=3)
    >>> m.component()
    'merge'
    >>> inc1 = Connection(so1, 'out1', m, 'in1')
    >>> inc2 = Connection(so2, 'out1', m, 'in2')
    >>> inc3 = Connection(so3, 'out1', m, 'in3')
    >>> outg = Connection(m, 'out1', si1, 'in1')
    >>> nw.add_conns(inc1, inc2, inc3, outg)

    A merge with three inlets mixes air (simplified) with pure nitrogen and
    pure oxygen. All gases enter the component at the same temperature. As
    mixing effects are not considered, the outlet temperature should thus be
    similar to the three inlet temperatures (difference might occur due to
    rounding in fluid property functions, let's check it for two different
    temperatures). It is e.g. possible to find the required mass flow of pure
    nitrogen given the nitrogen mass fraction in the outlet.

    >>> T = 293.15
    >>> inc1.set_attr(fluid={'O2': 0.23, 'N2': 0.77}, p=1, T=T, m=5)
    >>> inc2.set_attr(fluid={'O2': 1, 'N2':0}, T=T, m=5)
    >>> inc3.set_attr(fluid={'O2': 0, 'N2': 1}, T=T)
    >>> outg.set_attr(fluid={'N2': 0.4})
    >>> nw.solve('design')
    >>> round(inc3.m.val_SI, 2)
    0.25
    >>> abs(round((outg.T.val_SI - T) / T, 5)) < 0.01
    True
    >>> T = 173.15
    >>> inc1.set_attr(T=T)
    >>> inc2.set_attr(T=T)
    >>> inc3.set_attr(T=T)
    >>> nw.solve('design')
    >>> abs(round((outg.T.val_SI - T) / T, 5)) < 0.01
    True
    """

    @staticmethod
    def component():
        return 'merge'

    @staticmethod
    def get_variables():
        return {'num_in': dc_simple()}

    def get_mandatory_constraints(self):
        return {
            'mass_flow_constraints': {
                'func': self.mass_flow_func, 'deriv': self.mass_flow_deriv,
                'constant_deriv': True, 'latex': self.mass_flow_func_doc,
                'num_eq': 1},
            'fluid_constraints': {
                'func': self.fluid_func, 'deriv': self.fluid_deriv,
                'constant_deriv': False, 'latex': self.fluid_func_doc,
                'num_eq': self.num_nw_fluids},
            'energy_balance_constraints': {
                'func': self.energy_balance_func,
                'deriv': self.energy_balance_deriv,
                'constant_deriv': False, 'latex': self.energy_balance_func_doc,
                'num_eq': 1},
            'pressure_constraints': {
                'func': self.pressure_equality_func,
                'deriv': self.pressure_equality_deriv,
                'constant_deriv': True,
                'latex': self.pressure_equality_func_doc,
                'num_eq': self.num_i + self.num_o - 1}
        }

    def inlets(self):
        if self.num_in.is_set:
            return ['in' + str(i + 1) for i in range(self.num_in.val)]
        else:
            self.set_attr(num_in=2)
            return self.inlets()

    @staticmethod
    def outlets():
        return ['out1']

    def fluid_func(self):
        r"""
        Calculate the vector of residual values for fluid balance equations.

        Returns
        -------
        residual : list
            Vector of residual values for component's fluid balance.

            .. math::

                0 = \sum_i \dot{m}_{in,i} \cdot x_{fl,in,i} -
                \dot {m}_{out} \cdot x_{fl,out}\\
                \forall fl \in \text{network fluids},
                \; \forall i \in \text{inlets}
        """
        residual = []
        for fluid, x in self.outl[0].fluid.val.items():
            res = -x * self.outl[0].m.val_SI
            for i in self.inl:
                res += i.fluid.val[fluid] * i.m.val_SI
            residual += [res]
        return residual

    def fluid_func_doc(self, label):
        r"""
        Calculate the vector of residual values for fluid balance equations.

        Parameters
        ----------
        label : str
            Label for equation.

        Returns
        -------
        latex : str
            LaTeX code of equations applied.
        """
        latex = (
            r'0=\sum_i \dot{m}_{\mathrm{in,}i} \cdot x_{fl\mathrm{,in,}i}'
            r'- \dot {m}_\mathrm{out} \cdot x_{fl\mathrm{,out}}'
            r'\; \forall fl \in \text{network fluids,} \; \forall i \in'
            r'\text{inlets}'
        )
        return generate_latex_eq(self, latex, label)

    def fluid_deriv(self, increment_filter, k):
        r"""
        Calculate partial derivatives of fluid balance.

        Parameters
        ----------
        increment_filter : ndarray
            Matrix for filtering non-changing variables.

        k : int
            Position of derivatives in Jacobian matrix (k-th equation).
        """
        i = 0
        for fluid, x in self.outl[0].fluid.val.items():
            j = 0
            for inl in self.inl:
                self.jacobian[k, j, 0] = inl.fluid.val[fluid]
                self.jacobian[k, j, i + 3] = inl.m.val_SI
                j += 1
            self.jacobian[k, j, 0] = -x
            self.jacobian[k, j, i + 3] = -self.outl[0].m.val_SI
            i += 1
            k += 1

    def energy_balance_func(self):
        r"""
        Calculate energy balance.

        Returns
        -------
        residual : float
            Residual value of energy balance.

            .. math::

                0 = \sum_i \left(\dot{m}_{in,i} \cdot h_{in,i} \right) -
                \dot{m}_{out} \cdot h_{out}\\
                \forall i \in \text{inlets}
        """
        res = -self.outl[0].m.val_SI * self.outl[0].h.val_SI
        for i in self.inl:
            res += i.m.val_SI * i.h.val_SI
        return res

    def energy_balance_func_doc(self, label):
        r"""
        Calculate energy balance.

        Parameters
        ----------
        label : str
            Label for equation.

        Returns
        -------
        latex : str
            LaTeX code of equations applied.
        """
        latex = (
            r'0=\sum_i\left(\dot{m}_{\mathrm{in,}i}\cdot h_{\mathrm{in,}i}'
            r'\right) - \dot{m}_\mathrm{out} \cdot h_\mathrm{out} '
            r'\; \forall i \in \text{inlets}'
        )
        return generate_latex_eq(self, latex, label)

    def energy_balance_deriv(self, increment_filter, k):
        r"""
        Calculate partial derivatives of energy balance.

        Parameters
        ----------
        increment_filter : ndarray
            Matrix for filtering non-changing variables.

        k : int
            Position of derivatives in Jacobian matrix (k-th equation).
        """
        self.jacobian[k, self.num_i, 0] = -self.outl[0].h.val_SI
        self.jacobian[k, self.num_i, 2] = -self.outl[0].m.val_SI
        j = 0
        for i in self.inl:
            self.jacobian[k, j, 0] = i.h.val_SI
            self.jacobian[k, j, 2] = i.m.val_SI
            j += 1

    def initialise_fluids(self):
        """Fluid initialisation for fluid mixture at outlet of the node."""
        num_fl = {}
        for o in self.outl:
            num_fl[o] = num_fluids(o.fluid.val)

        for i in self.inl:
            num_fl[i] = num_fluids(i.fluid.val)

        ls = []
        if any(num_fl.values()) and not all(num_fl.values()):
            for conn, num in num_fl.items():
                if num == 1:
                    ls += [conn]

            for c in ls:
                for fluid in self.nw_fluids:
                    for o in self.outl:
                        if not o.fluid.val_set[fluid]:
                            o.fluid.val[fluid] = c.fluid.val[fluid]
                    for i in self.inl:
                        if not i.fluid.val_set[fluid]:
                            i.fluid.val[fluid] = c.fluid.val[fluid]
            for o in self.outl:
                o.target.propagate_fluid_to_target(o, o.target)

    def propagate_fluid_to_target(self, inconn, start):
        r"""
        Fluid propagation stops here.

        Parameters
        ----------
        inconn : tespy.connections.connection.Connection
            Connection to initialise.

        start : tespy.components.component.Component
            This component is the fluid propagation starting point.
            The starting component is saved to prevent infinite looping.
        """
        return

    def propagate_fluid_to_source(self, outconn, start):
        r"""
        Propagate the fluids towards connection's source in recursion.

        Parameters
        ----------
        outconn : tespy.connections.connection.Connection
            Connection to initialise.

        start : tespy.components.component.Component
            This component is the fluid propagation starting point.
            The starting component is saved to prevent infinite looping.
        """
        for inconn in self.inl:
            for fluid, x in outconn.fluid.val.items():
                if (not inconn.fluid.val_set[fluid] and
                        not inconn.good_starting_values):
                    inconn.fluid.val[fluid] = x

            inconn.source.propagate_fluid_to_source(inconn, start)

    def entropy_balance(self):
        r"""
        Calculate entropy balance of a merge.

        Note
        ----
        A definition of reference points is included for compensation of
        differences in zero point definitions of different fluid compositions.

        - Reference temperature: 298.15 K.
        - Reference pressure: 1 bar.

        .. math::

            \dot{S}_\mathrm{irr}= \dot{m}_\mathrm{out} \cdot
            \left( s_\mathrm{out} - s_\mathrm{out,ref} \right)
            - \sum_{i} \dot{m}_{\mathrm{in,}i} \cdot
            \left( s_{\mathrm{in,}i} - s_{\mathrm{in,ref,}i} \right)\\
        """
        T_ref = 298.15
        p_ref = 1e5
        self.S_irr = self.outl[0].m.val_SI * (
            self.outl[0].s.val_SI -
            s_mix_pT([0, p_ref, 0, self.outl[0].fluid.val], T_ref))
        for i in self.inl:
            self.S_irr -= i.m.val_SI * (
                i.s.val_SI -
                s_mix_pT([0, p_ref, 0, i.fluid.val], T_ref))

    def exergy_balance(self, T0):
        r"""
        Calculate exergy balance of a merge.

        Parameters
        ----------
        T0 : float
            Ambient temperature T0 / K.

        Note
        ----
        Please note, that the exergy balance accounts for physical exergy only.

        .. math ::

            \dot{E}_\mathrm{P} =
            \begin{cases}
            \begin{cases}
            \sum_i \dot{m}_i \cdot \left(e_\mathrm{out}^\mathrm{PH} -
            e_{\mathrm{in,}i}^\mathrm{PH}\right)
            & T_{\mathrm{in,}i} < T_\mathrm{out} \text{ \& }
            T_{\mathrm{in,}i} \geq T_0 \\
            \sum_i \dot{m}_i \cdot e_\mathrm{out}^\mathrm{PH}
            & T_{\mathrm{in,}i} < T_\mathrm{out} \text{ \& }
            T_{\mathrm{in,}i} < T_0 \\
            \end{cases} & T_\mathrm{out} > T_0\\

            \text{not defined (nan)} & T_\mathrm{out} = T_0\\

            \begin{cases}
            \sum_i \dot{m}_i \cdot e_\mathrm{out}^\mathrm{PH}
            & T_{\mathrm{in,}i} > T_\mathrm{out} \text{ \& }
            T_{\mathrm{in,}i} \geq T_0 \\
            \sum_i \dot{m}_i \cdot \left(e_\mathrm{out}^\mathrm{PH} -
            e_{\mathrm{in,}i}^\mathrm{PH}\right)
            & T_{\mathrm{in,}i} > T_\mathrm{out} \text{ \& }
            T_{\mathrm{in,}i} < T_0 \\
            \end{cases} & T_\mathrm{out} < T_0\\
            \end{cases}

            \dot{E}_\mathrm{F} =
            \begin{cases}
            \begin{cases}
            \sum_i \dot{m}_i \cdot \left(e_{\mathrm{in,}i}^\mathrm{PH} -
            e_\mathrm{out}^\mathrm{PH}\right)
            & T_{\mathrm{in,}i} > T_\mathrm{out} \\
            \sum_i \dot{E}_{\mathrm{in,}i}^\mathrm{PH}
            & T_{\mathrm{in,}i} < T_\mathrm{out} \text{ \& }
            T_{\mathrm{in,}i} < T_0 \\
            \end{cases} & T_\mathrm{out} > T_0\\

            \sum_i \dot{E}_{\mathrm{in,}i}^\mathrm{PH} & T_\mathrm{out} = T_0\\

            \begin{cases}
            \sum_i \dot{E}_{\mathrm{in,}i}^\mathrm{PH}
            & T_{\mathrm{in,}i} > T_\mathrm{out} \text{ \& }
            T_{\mathrm{in,}i} \geq T_0 \\
            \sum_i \dot{m}_i \cdot \left(e_{\mathrm{in,}i}^\mathrm{PH} -
            e_\mathrm{out}^\mathrm{PH}\right)
            & T_{\mathrm{in,}i} < T_\mathrm{out} \\
            \end{cases} & T_\mathrm{out} < T_0\\
            \end{cases}

            \forall i \in \text{merge inlets}

            \dot{E}_\mathrm{bus} = \text{not defined (nan)}
        """
        self.E_P = 0
        self.E_F = 0
        if self.outl[0].T.val_SI > T0:
            for i in self.inl:
                if i.T.val_SI < self.outl[0].T.val_SI:
                    if i.T.val_SI >= T0:
                        self.E_P += i.m.val_SI * (
                            self.outl[0].ex_physical - i.ex_physical)
                    else:
                        self.E_P += i.m.val_SI * self.outl[0].ex_physical
                        self.E_F += i.Ex_physical
                else:
                    self.E_F += i.m.val_SI * (
                        i.ex_physical - self.outl[0].ex_physical)
        elif self.outl[0].T.val_SI == T0:
            self.E_P = np.nan
            for i in self.inl:
                self.E_F += i.Ex_physical
        else:
            for i in self.inl:
                if i.T.val_SI > self.outl[0].T.val_SI:
                    if i.T.val_SI >= T0:
                        self.E_P += i.m.val_SI * self.outl[0].ex_physical
                        self.E_F += i.Ex_physical
                    else:
                        self.E_P += i.m.val_SI * (
                            self.outl[0].ex_physical - i.ex_physical)
                else:
                    self.E_F += i.m.val_SI * (
                        i.ex_physical - self.outl[0].ex_physical)

        self.E_bus = {
            "chemical": np.nan, "physical": np.nan, "massless": np.nan
        }
        self.E_D = self.E_F - self.E_P
        self.epsilon = self.E_P / self.E_F

    def get_plotting_data(self):
        """Generate a dictionary containing FluProDia plotting information.

        Returns
        -------
        data : dict
            A nested dictionary containing the keywords required by the
            :code:`calc_individual_isoline` method of the
            :code:`FluidPropertyDiagram` class. First level keys are the
            connection index ('in1' -> 'out1', therefore :code:`1` etc.).
        """
        return {
            i + 1: {
                'isoline_property': 'p',
                'isoline_value': self.inl[i].p.val,
                'isoline_value_end': self.outl[0].p.val,
                'starting_point_property': 'v',
                'starting_point_value': self.inl[i].vol.val,
                'ending_point_property': 'v',
                'ending_point_value': self.outl[0].vol.val
            } for i in range(self.num_i)}

    def exergy_economic_balance(self, Exe_Eco, T0):
        r"""
        declare and prepare component's variables c, E, C and Z and calculate exergy economics balance of a component.

        c: cost per exergy unit to every connection.
        E: Sum of exergy streams to each inlet and outlet connection.
        C: Cost stream to every connection.
        Z: Sum of leveled capital investment costs 'CI' and operating and maintenance costs 'OM'.

        For inlets:
            c is known from previous components for thermal, mechanical, physical and chemical
            Z is given as input.
            E is calculated previously in connection functions for thermal, mechanical, physical and chemical
            C is calculated by Exergy-Costing principle for thermal, mechanical, physical and chemical

        For outlets:
            E is calculated previously in connection functions for thermal, mechanical, physical and chemical
            C is calculated by Exergy-Costing principle for thermal, mechanical, physical and chemical
            c is calculated by Exergy-Costing principle for thermal, mechanical, physical and chemical

        Units
            c [ / GJ]
            Z [ / h]
            E [ W ]
            C [ / h]

        Parameters
        ----------
        Exe_Eco: dict
            Contains c for all sources as well as all Z for every component or component group in the network.

        Note
        ----
        Requirement: all necessary input variables are known and calculated previously.
            input variables: Z, E, c and C for all inlets for thermal, mechanical, physical and chemical.

        The values of the connections (c, C) depend on the purpose for which the component under consideration is used and the ambient conditions.
        For each connection at the output, the costs per unit of exergy as well as the cost streams are calculated. This applies to the components (thermal, mechanical, physical and chemical).
        The total cost stream and the associated costs per exergy unit are then determined.
        The F and P principles are required for this.
        The cases are taken from the exergy balance function.

        """
        # assign Z to be an attribute for the component
        Z_id = f"{self.label}_Z"
        self.Z_costs = Exe_Eco[f"{Z_id}"]

        # sum exergy streams of outlets
        self.outl[0].Ex_tot = self.outl[0].Ex_physical + self.outl[0].Ex_chemical

        "++cases++"
        # for sum
        self.C_P = 0
        self.C_F = 0
        self.inl_hot = [c for c in self.inl if c.T.val >= self.outl[0].T.val]
        self.inl_cold = [c for c in self.inl if c.T.val < self.outl[0].T.val]
        if self.outl[0].T.val_SI > T0:
            self.case_one(T0)

        elif self.outl[0].T.val_SI == T0:
            self.case_two()

        elif self.outl[0].T.val_SI <= T0:
            self.case_three(T0)

        self.C_D = self.c_F * self.E_D * (3600 / 10 ** 9)
        self.r = 100 * (self.c_P - self.c_F) / self.c_F
        self.f = 100 * self.Z_costs / (self.Z_costs + self.C_D)

        # conn calculated
        self.outl[0].eco_check = True

    def case_one(self, T0):
        """
        if self.outl[0].T.val_SI > T0

        cold stream: T <= T_out
        hot stream: T > T_out
        """
        unit_C = (3600 / 10 ** 9)
        unit_c = (10 ** 9 / 3600)

        # chemical exergy
        self.outl[0].c_chemical = sum(conn.c_chemical * conn.m.val_SI for conn in self.inl) / self.outl[0].m.val_SI
        self.outl[0].C_chemical = self.outl[0].c_chemical * self.outl[0].Ex_chemical * unit_C

        # unaffected mech exergy, all inlets have same p. Same as chemical, same result also.
        self.outl[0].c_mech = sum(conn.c_mech * conn.m.val_SI for conn in self.inl) / self.outl[0].m.val_SI
        self.outl[0].C_mech = self.outl[0].c_mech * self.outl[0].Ex_mech * unit_C

        # Fuel from hot streams
        for i in self.inl_hot:
            self.C_F += i.m.val_SI * i.c_therm * (
                i.ex_therm - self.outl[0].ex_therm) * unit_C
        self.c_F = self.C_F / self.E_F * unit_c

        # product costs
        self.C_P = self.C_F + self.Z_costs
        self.c_P = self.C_P / self.E_P * unit_c

        # [outlets] costs streams associated with the product with P principle (power and [T, M, CH])
        # self.outl[0].C_therm = self.c_P * self.outl[0].Ex_therm * unit_C
        self.inl_cold[0].c_therm_help = self.c_P + (self.inl_hot[0].m.val_SI/self.inl_cold[0].m.val_SI) * (self.c_P - self.inl_hot[0].c_therm)
        #self.outl[0].C_therm = (self.inl_cold[0].c_therm_help * self.inl_cold[0].Ex_therm * unit_C) + (self.inl_hot[0].c_therm * self.inl_hot[0].Ex_therm) * unit_C
        self.outl[0].C_therm_help = self.inl_cold[0].m.val_SI * (self.inl_cold[0].c_therm_help * self.outl[0].ex_therm * unit_C)
        self.outl[0].C_therm = self.inl_cold[0].m.val_SI * (self.inl_cold[0].c_therm_help * self.outl[0].ex_therm * unit_C) - self.inl_cold[0].m.val_SI * (self.inl_cold[0].c_therm * self.inl_cold[0].ex_therm * unit_C)

        # costs per exergy unit for outlets streams associated with the product (power and [T, M, CH])
        self.outl[0].c_therm = self.outl[0].C_therm / self.outl[0].Ex_therm * unit_c

        # physical costs streams for all outlets
        self.outl[0].C_physical = self.outl[0].C_therm + self.outl[0].C_mech
        self.outl[0].c_physical = self.outl[0].C_physical / self.outl[0].Ex_physical * unit_c

        # average costs for outlets
        self.outl[0].C_tot = self.outl[0].C_physical + self.outl[0].C_chemical
        self.outl[0].c_tot = self.outl[0].C_tot / self.outl[0].Ex_tot * unit_c

        # check
        check_in = self.inl[0].C_physical + self.inl[1].C_physical + self.inl[0].C_chemical + self.inl[0].C_chemical + self.Z_costs
        check_out = self.outl[0].C_chemical + self.outl[0].C_physical
        self.outl[0].C_physical_soll = self.inl[0].c_physical * self.inl[0].c_physical
        print('e')

        # # ----
        # for i in self.inl:
        #     # if cold stream:
        #     if i.T.val_SI < self.outl[0].T.val_SI:
        #         # cold over T0, out over T0
        #         if i.T.val_SI >= T0:
        #             self.E_P += i.m.val_SI * (
        #                 self.outl[0].ex_physical - i.ex_physical)
        #         # cold under T0, out over Tv
        #         else:
        #             self.E_P += i.m.val_SI * self.outl[0].ex_physical
        #             self.E_F += i.Ex_physical
        #     # if hot stream
        #     elif i.T.val_SI >= self.outl[0].T.val_SI:
        #         ...

    def case_two(self):
        """
        if self.outl[0].T.val_SI == T0

        cold stream: T <= T_out
        hot stream: T > T_out
        """
        # dissipative
        self.E_P = np.nan
        for i in self.inl:
            self.E_F += i.Ex_physical

    def case_three(self, T0):
        """
        if self.outl[0].T.val_SI <= T0

        cold stream: T <= T_out
        hot stream: T > T_out
        """
        for i in self.inl:
            if i.T.val_SI > self.outl[0].T.val_SI:
                if i.T.val_SI >= T0:
                    self.E_P += i.m.val_SI * self.outl[0].ex_physical
                    self.E_F += i.Ex_physical
                else:
                    self.E_P += i.m.val_SI * (
                        self.outl[0].ex_physical - i.ex_physical)
            else:
                self.E_F += i.m.val_SI * (
                    i.ex_physical - self.outl[0].ex_physical)
