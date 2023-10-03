# -*- coding: utf-8

"""Module of class Turbine.


This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location tespy/components/turbomachinery/turbine.py

SPDX-License-Identifier: MIT
"""


import numpy as np

from tespy.components.turbomachinery.base import Turbomachine
from tespy.tools import logger
from tespy.tools.data_containers import ComponentCharacteristics as dc_cc
from tespy.tools.data_containers import ComponentProperties as dc_cp
from tespy.tools.data_containers import DataContainerSimple as dc_simple
from tespy.tools.document_models import generate_latex_eq
from tespy.tools.fluid_properties import isentropic
from tespy.tools.fluid_properties import v_mix_ph


class Turbine(Turbomachine):
    r"""
    Class for gas or steam turbines.

    **Mandatory Equations**

    - :py:meth:`tespy.components.component.Component.fluid_func`
    - :py:meth:`tespy.components.component.Component.mass_flow_func`

    **Optional Equations**

    - :py:meth:`tespy.components.component.Component.pr_func`
    - :py:meth:`tespy.components.turbomachinery.base.Turbomachine.energy_balance_func`
    - :py:meth:`tespy.components.turbomachinery.turbine.Turbine.eta_s_func`
    - :py:meth:`tespy.components.turbomachinery.turbine.Turbine.eta_s_char_func`
    - :py:meth:`tespy.components.turbomachinery.turbine.Turbine.cone_func`

    Inlets/Outlets

    - in1
    - out1

    Image

    .. image:: /api/_images/Turbine.svg
       :alt: flowsheet of the turbine
       :align: center
       :class: only-light

    .. image:: /api/_images/Turbine_darkmode.svg
       :alt: flowsheet of the turbine
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

    P : float, dict
        Power, :math:`P/\text{W}`

    eta_s : float, dict
        Isentropic efficiency, :math:`\eta_s/1`

    pr : float, dict, :code:`"var"`
        Outlet to inlet pressure ratio, :math:`pr/1`

    eta_s_char : tespy.tools.characteristics.CharLine, dict
        Characteristic curve for isentropic efficiency, provide CharLine as
        function :code:`func`.

    cone : dict
        Apply Stodola's cone law (works in offdesign only).

    Example
    -------
    A steam turbine expands 10 kg/s of superheated steam at 550 °C and 110 bar
    to 0,5 bar at the outlet. For example, it is possible to calulate the power
    output and vapour content at the outlet for a given isentropic efficiency.

    >>> from tespy.components import Sink, Source, Turbine
    >>> from tespy.connections import Connection
    >>> from tespy.networks import Network
    >>> from tespy.tools import ComponentCharacteristics as dc_cc
    >>> import shutil
    >>> fluid_list = ['water']
    >>> nw = Network(fluids=fluid_list, p_unit='bar', T_unit='C',
    ... h_unit='kJ / kg', iterinfo=False)
    >>> si = Sink('sink')
    >>> so = Source('source')
    >>> t = Turbine('turbine')
    >>> t.component()
    'turbine'
    >>> inc = Connection(so, 'out1', t, 'in1')
    >>> outg = Connection(t, 'out1', si, 'in1')
    >>> nw.add_conns(inc, outg)

    In design conditions the isentropic efficiency is specified. For offdesign
    a characteristic function will be applied, together with Stodola's cone
    law coupling the turbine mass flow to inlet pressure.

    >>> t.set_attr(eta_s=0.9, design=['eta_s'],
    ... offdesign=['eta_s_char', 'cone'])
    >>> inc.set_attr(fluid={'water': 1}, m=10, T=550, p=110, design=['p'])
    >>> outg.set_attr(p=0.5)
    >>> nw.solve('design')
    >>> nw.save('tmp')
    >>> round(t.P.val, 0)
    -10452574.0
    >>> round(outg.x.val, 3)
    0.914
    >>> inc.set_attr(m=8)
    >>> nw.solve('offdesign', design_path='tmp')
    >>> round(t.eta_s.val, 3)
    0.898
    >>> round(inc.p.val, 1)
    88.6
    >>> shutil.rmtree('./tmp', ignore_errors=True)
    """

    @staticmethod
    def component():
        return 'turbine'

    def get_variables(self):
        return {
            'P': dc_cp(
                max_val=0, num_eq=1,
                deriv=self.energy_balance_deriv,
                func=self.energy_balance_func,
                latex=self.energy_balance_func_doc),
            'eta_s': dc_cp(
                min_val=0, max_val=1, num_eq=1,
                deriv=self.eta_s_deriv,
                func=self.eta_s_func, latex=self.eta_s_func_doc),
            'eta_s_char': dc_cc(
                param='m', num_eq=1,
                deriv=self.eta_s_char_deriv,
                func=self.eta_s_char_func, latex=self.eta_s_char_func_doc),
            'pr': dc_cp(
                min_val=0, max_val=1, num_eq=1,
                deriv=self.pr_deriv,
                func=self.pr_func, func_params={'pr': 'pr'},
                latex=self.pr_func_doc),
            'cone': dc_simple(
                deriv=self.cone_deriv, num_eq=1,
                func=self.cone_func, latex=self.cone_func_doc)
        }

    def eta_s_func(self):
        r"""
        Equation for given isentropic efficiency of a turbine.

        Returns
        -------
        residual : float
            Residual value of equation.

            .. math::

                0 = -\left( h_{out} - h_{in} \right) +
                \left( h_{out,s} - h_{in} \right) \cdot \eta_{s,e}
        """
        return (
            -(self.outl[0].h.val_SI - self.inl[0].h.val_SI) + (
                isentropic(
                    self.inl[0].get_flow(), self.outl[0].get_flow(),
                    T0=self.inl[0].T.val_SI) -
                self.inl[0].h.val_SI) * self.eta_s.val)

    def eta_s_func_doc(self, label):
        r"""
        Equation for given isentropic efficiency of a turbine.

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
            r'0=-\left(h_\mathrm{out}-h_\mathrm{in}\right)+\left('
            r'h_\mathrm{out,s}-h_\mathrm{in}\right)\cdot\eta_\mathrm{s}')
        return generate_latex_eq(self, latex, label)

    def eta_s_deriv(self, increment_filter, k):
        r"""
        Partial derivatives for isentropic efficiency function.

        Parameters
        ----------
        increment_filter : ndarray
            Matrix for filtering non-changing variables.

        k : int
            Position of derivatives in Jacobian matrix (k-th equation).
        """
        f = self.eta_s_func
        if not increment_filter[0, 1]:
            self.jacobian[k, 0, 1] = self.numeric_deriv(f, 'p', 0)
        if not increment_filter[1, 1]:
            self.jacobian[k, 1, 1] = self.numeric_deriv(f, 'p', 1)
        if not increment_filter[0, 2]:
            self.jacobian[k, 0, 2] = self.numeric_deriv(f, 'h', 0)
        self.jacobian[k, 1, 2] = -1

    def cone_func(self):
        r"""
        Equation for stodolas cone law.

        Returns
        -------
        residual : float
            Residual value of equation.

            .. math::

                0 = \frac{\dot{m}_{in,ref} \cdot p_{in}}{p_{in,ref}} \cdot
                \sqrt{\frac{p_{in,ref} \cdot v_{in}}{p_{in} \cdot v_{in,ref}}}
                \cdot \sqrt{\frac{1 - \left(\frac{p_{out}}{p_{in}} \right)^{2}}
                {1 - \left(\frac{p_{out,ref}}{p_{in,ref}} \right)^{2}}} -
                \dot{m}_{in}
        """
        n = 1
        i = self.inl[0]
        o = self.outl[0]
        vol = v_mix_ph(i.get_flow(), T0=self.inl[0].T.val_SI)
        return (
            - i.m.val_SI + i.m.design * i.p.val_SI / i.p.design *
            np.sqrt(i.p.design * i.vol.design / (i.p.val_SI * vol)) *
            np.sqrt(abs((1 - (o.p.val_SI / i.p.val_SI) ** ((n + 1) / n)) /
                        (1 - (self.pr.design) ** ((n + 1) / n)))))

    def cone_func_doc(self, label):
        r"""
        Equation for stodolas cone law.

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
            r'0 = \frac{\dot{m}_\mathrm{in,design}\cdot p_\mathrm{in}}'
            r'{p_\mathrm{in,design}}\cdot\sqrt{\frac{p_\mathrm{in,design}'
            r'\cdot v_\mathrm{in}}{p_\mathrm{in}\cdot '
            r'v_\mathrm{in,design}}\cdot\frac{1-\left('
            r'\frac{p_\mathrm{out}}{p_\mathrm{in}} \right)^{2}}'
            r'{1-\left(\frac{p_\mathrm{out,design}}{p_\mathrm{in,design}}'
            r'\right)^{2}}} -\dot{m}_\mathrm{in}')
        return generate_latex_eq(self, latex, label)

    def cone_deriv(self, increment_filter, k):
        r"""
        Partial derivatives for stodolas cone law.

        Parameters
        ----------
        increment_filter : ndarray
            Matrix for filtering non-changing variables.

        k : int
            Position of derivatives in Jacobian matrix (k-th equation).
        """
        f = self.cone_func
        self.jacobian[k, 0, 0] = -1
        if not increment_filter[0, 1]:
            self.jacobian[k, 0, 1] = self.numeric_deriv(f, 'p', 0)
        if not increment_filter[0, 2]:
            self.jacobian[k, 0, 2] = self.numeric_deriv(f, 'h', 0)
        if not increment_filter[1, 2]:
            self.jacobian[k, 1, 2] = self.numeric_deriv(f, 'p', 1)

    def eta_s_char_func(self):
        r"""
        Equation for given isentropic efficiency characteristic.

        Returns
        -------
        residual : float
            Residual value of equation.

            .. math::

                0 = - \left( h_\mathrm{out} - h_\mathrm{in} \right) +
                \eta_\mathrm{s,design} \cdot f\left( expr \right) \cdot
                \left(h_\mathrm{out,s}-h_\mathrm{in}\right)
        """
        p = self.eta_s_char.param
        expr = self.get_char_expr(p)
        if not expr:
            msg = ('Please choose a valid parameter, you want to link the '
                   'isentropic efficiency to at component ' + self.label + '.')
            logger.error(msg)
            raise ValueError(msg)

        i = self.inl[0]
        o = self.outl[0]
        return (
            -(o.h.val_SI - i.h.val_SI) + self.eta_s.design *
            self.eta_s_char.char_func.evaluate(expr) * (isentropic(
                i.get_flow(), o.get_flow(), T0=self.inl[0].T.val_SI) -
                i.h.val_SI))

    def eta_s_char_func_doc(self, label):
        r"""
        Equation for given isentropic efficiency characteristic.

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
            r'0=-\left(h_\mathrm{out}-h_\mathrm{in}\right)+'
            r'\eta_\mathrm{s,design}\cdot f \left(X\right)'
            r'\cdot\left(h_\mathrm{out,s}-h_\mathrm{in}\right)')
        return generate_latex_eq(self, latex, label)

    def eta_s_char_deriv(self, increment_filter, k):
        r"""
        Partial derivatives for isentropic efficiency characteristic.

        Parameters
        ----------
        increment_filter : ndarray
            Matrix for filtering non-changing variables.

        k : int
            Position of derivatives in Jacobian matrix (k-th equation).
        """
        f = self.eta_s_char_func
        if not increment_filter[0, 0]:
            self.jacobian[k, 0, 0] = self.numeric_deriv(f, 'm', 0)
        if not increment_filter[0, 1]:
            self.jacobian[k, 0, 1] = self.numeric_deriv(f, 'p', 0)
        if not increment_filter[0, 2]:
            self.jacobian[k, 0, 2] = self.numeric_deriv(f, 'h', 0)
        if not increment_filter[1, 1]:
            self.jacobian[k, 1, 1] = self.numeric_deriv(f, 'p', 1)
        if not increment_filter[1, 2]:
            self.jacobian[k, 1, 2] = self.numeric_deriv(f, 'h', 1)

    def convergence_check(self):
        r"""
        Perform a convergence check.

        Note
        ----
        Manipulate enthalpies/pressure at inlet and outlet if not specified by
        user to match physically feasible constraints.
        """
        i, o = self.inl[0], self.outl[0]

        if not i.good_starting_values:
            if i.p.val_SI <= 1e5 and not i.p.val_set:
                i.p.val_SI = 1e5

            if i.h.val_SI < 10e5 and not i.h.val_set:
                i.h.val_SI = 10e5

            if o.h.val_SI < 5e5 and not o.h.val_set:
                o.h.val_SI = 5e5

        if i.h.val_SI <= o.h.val_SI and not o.h.val_set:
            o.h.val_SI = i.h.val_SI * 0.9

        if i.p.val_SI <= o.p.val_SI and not o.p.val_set:
            o.p.val_SI = i.p.val_SI * 0.9

    @staticmethod
    def initialise_Source(c, key):
        r"""
        Return a starting value for pressure and enthalpy at outlet.

        Parameters
        ----------
        c : tespy.connections.connection.Connection
            Connection to perform initialisation on.

        key : str
            Fluid property to retrieve.

        Returns
        -------
        val : float
            Starting value for pressure/enthalpy in SI units.

            .. math::

                val = \begin{cases}
                5 \cdot 10^4 & \text{key = 'p'}\\
                1.5 \cdot 10^6 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 0.5e5
        elif key == 'h':
            return 1.5e6

    @staticmethod
    def initialise_target(c, key):
        r"""
        Return a starting value for pressure and enthalpy at inlet.

        Parameters
        ----------
        c : tespy.connections.connection.Connection
            Connection to perform initialisation on.

        key : str
            Fluid property to retrieve.

        Returns
        -------
        val : float
            Starting value for pressure/enthalpy in SI units.

            .. math::

                val = \begin{cases}
                2.5 \cdot 10^6 & \text{key = 'p'}\\
                2 \cdot 10^6 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 2.5e6
        elif key == 'h':
            return 2e6

    def calc_parameters(self):
        r"""Postprocessing parameter calculation."""
        super().calc_parameters()

        self.eta_s.val = (
            (self.outl[0].h.val_SI - self.inl[0].h.val_SI) / (
                isentropic(
                    self.inl[0].get_flow(), self.outl[0].get_flow(),
                    T0=self.inl[0].T.val_SI) - self.inl[0].h.val_SI))

    def exergy_balance(self, T0):
        r"""
        Calculate exergy balance of a turbine.

        Parameters
        ----------
        T0 : float
            Ambient temperature T0 / K.

        Note
        ----
        .. math::

            \dot{E}_\mathrm{P} =
            \begin{cases}
            -P & T_\mathrm{in}, T_\mathrm{out} \geq T_0\\
            -P + \dot{E}_\mathrm{out}^\mathrm{T}
            & T_\mathrm{in} > T_0 \geq T_\mathrm{out}\\
            -P +\dot{E}_\mathrm{out}^\mathrm{T}- \dot{E}_\mathrm{in}^\mathrm{T}
            & T_0 \geq T_\mathrm{in}, T_\mathrm{out}\\
            \end{cases}

           \dot{E}_\mathrm{F} =
           \begin{cases}
           \dot{E}_\mathrm{in}^\mathrm{PH} - \dot{E}_\mathrm{out}^\mathrm{PH}
           & T_\mathrm{in}, T_\mathrm{out} \geq T_0\\
           \dot{E}_\mathrm{in}^\mathrm{T} + \dot{E}_\mathrm{in}^\mathrm{M} -
           \dot{E}_\mathrm{out}^\mathrm{M}
           & T_\mathrm{in} > T_0 \geq T_\mathrm{out}\\
           \dot{E}_\mathrm{in}^\mathrm{M} - \dot{E}_\mathrm{out}^\mathrm{M}
           & T_0 \geq T_\mathrm{in}, T_\mathrm{out}\\
           \end{cases}

           \dot{E}_\mathrm{bus} = -P
        """
        if self.inl[0].T.val_SI >= T0 and self.outl[0].T.val_SI >= T0:
            self.E_P = -self.P.val
            self.E_F = self.inl[0].Ex_physical - self.outl[0].Ex_physical
        elif self.inl[0].T.val_SI > T0 and self.outl[0].T.val_SI <= T0:
            self.E_P = -self.P.val + self.outl[0].Ex_therm
            self.E_F = self.inl[0].Ex_therm + (
                self.inl[0].Ex_mech - self.outl[0].Ex_mech)
        elif self.inl[0].T.val_SI <= T0 and self.outl[0].T.val_SI <= T0:
            self.E_P = -self.P.val + (
                self.outl[0].Ex_therm - self.inl[0].Ex_therm)
            self.E_F = self.inl[0].Ex_mech - self.outl[0].Ex_mech
        else:
            msg = ('Exergy balance of a turbine, where outlet temperature is '
                   'larger than inlet temperature is not implmented.')
            logger.warning(msg)
            self.E_P = np.nan
            self.E_F = np.nan

        self.E_bus = {"chemical": 0, "physical": 0, "massless": -self.P.val}
        self.E_D = self.E_F - self.E_P
        self.epsilon = self.E_P / self.E_F

    def assign_eco_values_bus(self):
        r"""
        Write the costs related to massless exergy streams to the collection dict of exergy economic values.

        """
        #list = ['E_streams_tot', 'C_streams', 'c_per_unit']
        #self.exe_eco = {d: {} for d in list}
        self.exe_eco['E_streams_tot']['E_Power'] = self.E_Power
        self.exe_eco['C_streams']['C_Power'] = self.C_Power
        self.exe_eco['c_per_unit']['c_Power'] = self.c_Power

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

        # create attribute for the output power - massless exergy stream
        self.E_Power = self.E_bus['massless']

        # sum exergy streams of outlets
        self.outl[0].Ex_tot = self.outl[0].Ex_physical + self.outl[0].Ex_chemical

        "++cases++"
        if self.inl[0].T.val_SI >= T0 and self.outl[0].T.val_SI >= T0:
            self.case_one()
        elif self.inl[0].T.val_SI > T0 and self.outl[0].T.val_SI <= T0:
            self.case_two()
        elif self.inl[0].T.val_SI <= T0 and self.outl[0].T.val_SI <= T0:
            self.case_three()
        else:
            ...

        self.C_D = self.c_F * self.E_D * (3600 / 10 ** 9)
        self.r = 100 * (self.c_P - self.c_F) / self.c_F
        self.f = 100 * self.Z_costs / (self.Z_costs + self.C_D)

        # for assigning the costs related to massless exergy streams to the collection dict of exergy economic values. (for turbine, pump and compressor)
        self.eco_bus_value = True

        # conn calculated
        self.outl[0].eco_check = True

    def case_one(self):
        """ if self.inl[0].T.val_SI >= T0 and self.outl[0].T.val_SI >= T0"""
        # convert units
        unit_C = (3600 / 10 ** 9)
        unit_c = (10 ** 9 / 3600)

        # unaffected chemical exergy
        self.outl[0].c_chemical = self.inl[0].c_chemical
        self.outl[0].C_chemical = self.inl[0].C_chemical

        # F principle
        self.outl[0].c_therm = self.inl[0].c_therm
        self.outl[0].c_mech = self.inl[0].c_mech

        # costs streams associated with the fuel
        self.outl[0].C_therm = self.outl[0].c_therm * self.outl[0].Ex_therm * unit_C
        self.outl[0].C_mech = self.outl[0].c_mech * self.outl[0].Ex_mech * unit_C

        # fuel costs
        self.C_F = (self.inl[0].C_therm + self.inl[0].C_mech) - (self.outl[0].C_therm + self.outl[0].C_mech)
        self.c_F = self.C_F / self.E_F * unit_c

        # product costs
        self.C_P = self.C_F + self.Z_costs
        self.c_P = self.C_P / self.E_P * unit_c

        # costs streams associated with the product with P principle (power and [T, M, CH])
        self.C_Power = self.c_P * self.E_Power * unit_C

        # costs per exergy unit for outlets streams associated with the product (power and [T, M, CH])
        self.c_Power = self.C_Power / self.E_Power * unit_c

        # physical costs streams for all outlets
        self.outl[0].C_physical = self.outl[0].C_therm + self.outl[0].C_mech
        self.outl[0].c_physical = self.outl[0].C_physical / self.outl[0].Ex_physical * unit_c

        # average costs for outlets
        self.outl[0].C_tot = self.outl[0].C_physical + self.outl[0].C_chemical
        self.outl[0].c_tot = self.outl[0].C_tot / self.outl[0].Ex_tot * unit_c

    def case_two(self):
        """ if self.inl[0].T.val_SI > T0 and self.outl[0].T.val_SI <= T0 """
        # convert units
        unit_C = (3600 / 10 ** 9)
        unit_c = (10 ** 9 / 3600)

        # unaffected chemical exergy
        self.outl[0].c_chemical = self.inl[0].c_chemical
        self.outl[0].C_chemical = self.inl[0].C_chemical

        # F principle
        self.outl[0].c_mech = self.inl[0].c_mech

        # costs streams associated with the fuel
        self.outl[0].C_mech = self.outl[0].c_mech * self.outl[0].Ex_mech * unit_C

        # fuel costs
        self.C_F = (self.inl[0].C_therm + self.inl[0].C_mech) - (self.outl[0].C_mech)
        self.c_F = self.C_F / self.E_F * unit_c

        # product costs
        self.C_P = self.C_F + self.Z_costs
        self.c_P = self.C_P / self.E_P * unit_c

        # costs streams associated with the product with P principle (power and [T, M, CH])
        self.C_Power = self.c_P * self.E_Power * unit_C
        self.outl[0].C_therm = self.c_P * self.outl[0].Ex_therm * unit_C

        # costs per exergy unit for outlets streams associated with the product (power and [T, M, CH])
        self.c_Power = self.C_Power / self.E_Power * unit_c
        self.outl[0].c_therm = self.outl[0].C_therm / self.outl[0].Ex_therm * unit_c

        # physical costs streams for all outlets
        self.outl[0].C_physical = self.outl[0].C_therm + self.outl[0].C_mech
        self.outl[0].c_physical = self.outl[0].C_physical / self.outl[0].Ex_physical * unit_c

        # average costs for outlets
        self.outl[0].C_tot = self.outl[0].C_physical + self.outl[0].C_chemical
        self.outl[0].c_tot = self.outl[0].C_tot / self.outl[0].Ex_tot * unit_c

    def case_three(self):
        """ if self.inl[0].T.val_SI <= T0 and self.outl[0].T.val_SI <= T0 """
        # convert units
        unit_C = (3600 / 10 ** 9)
        unit_c = (10 ** 9 / 3600)

        # unaffected chemical exergy
        self.outl[0].c_chemical = self.inl[0].c_chemical
        self.outl[0].C_chemical = self.inl[0].C_chemical

        # F principle
        self.outl[0].c_mech = self.inl[0].c_mech

        # costs streams associated with the fuel
        self.outl[0].C_mech = self.outl[0].c_mech * self.outl[0].Ex_mech * unit_C

        # fuel costs
        self.C_F = (self.inl[0].C_mech) - (self.outl[0].C_mech)
        self.c_F = self.C_F / self.E_F * unit_c

        # product costs
        self.C_P = self.C_F + self.Z_costs
        self.c_P = self.C_P / self.E_P * unit_c

        # costs streams associated with the product with P principle (power and [T, M, CH])
        self.C_Power = self.c_P * self.E_Power * unit_C
        self.outl[0].C_therm = self.c_P * (self.outl[0].Ex_therm - self.inl[0].Ex_therm) * unit_C + self.inl[0].C_therm

        # costs per exergy unit for outlets streams associated with the product (power and [T, M, CH])
        self.c_Power = self.C_Power / self.E_Power * unit_c
        self.outl[0].c_therm = self.outl[0].C_therm / self.outl[0].Ex_therm * unit_c

        # physical costs streams for all outlets
        self.outl[0].C_physical = self.outl[0].C_therm + self.outl[0].C_mech
        self.outl[0].c_physical = self.outl[0].C_physical / self.outl[0].Ex_physical * unit_c

        # average costs for outlets
        self.outl[0].C_tot = self.outl[0].C_physical + self.outl[0].C_chemical
        self.outl[0].c_tot = self.outl[0].C_tot / self.outl[0].Ex_tot * unit_c
