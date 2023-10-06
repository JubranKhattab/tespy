# -*- coding: utf-8

"""Module of class Valve.


This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location tespy/components/piping.py

SPDX-License-Identifier: MIT
"""

import numpy as np

from tespy.components.component import Component
from tespy.tools import logger
from tespy.tools.data_containers import ComponentCharacteristics as dc_cc
from tespy.tools.data_containers import ComponentProperties as dc_cp
from tespy.tools.document_models import generate_latex_eq


class Valve(Component):
    r"""
    The Valve throttles a fluid without changing enthalpy.

    **Mandatory Equations**

    - :py:meth:`tespy.components.component.Component.fluid_func`
    - :py:meth:`tespy.components.component.Component.mass_flow_func`

    **Optional Equations**

    - :py:meth:`tespy.components.component.Component.pr_func`
    - :py:meth:`tespy.components.component.Component.zeta_func`
    - :py:meth:`tespy.components.piping.valve.Valve.dp_char_func`

    Inlets/Outlets

    - in1
    - out1

    Image

    .. image:: /api/_images/Valve.svg
       :alt: flowsheet of the valve
       :align: center
       :class: only-light

    .. image:: /api/_images/Valve_darkmode.svg
       :alt: flowsheet of the valve
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

    pr : float, dict, :code:`"var"`
        Outlet to inlet pressure ratio, :math:`pr/1`

    zeta : float, dict, :code:`"var"`
        Geometry independent friction coefficient,
        :math:`\frac{\zeta}{D^4}/\frac{1}{\text{m}^4}`.

    dp_char : tespy.tools.characteristics.CharLine, dict
        Characteristic line for difference pressure to mass flow.

    Example
    -------
    A mass flow of 1 kg/s methane is throttled from 80 bar to 15 bar in a
    valve. The inlet temperature is at 50 °C. It is possible to determine the
    outlet temperature as the throttling does not change enthalpy.

    >>> from tespy.components import Sink, Source, Valve
    >>> from tespy.connections import Connection
    >>> from tespy.networks import Network
    >>> import shutil
    >>> fluid_list = ['CH4']
    >>> nw = Network(fluids=fluid_list, p_unit='bar', T_unit='C',
    ... iterinfo=False)
    >>> so = Source('source')
    >>> si = Sink('sink')
    >>> v = Valve('valve')
    >>> v.component()
    'valve'
    >>> so_v = Connection(so, 'out1', v, 'in1')
    >>> v_si = Connection(v, 'out1', si, 'in1')
    >>> nw.add_conns(so_v, v_si)
    >>> v.set_attr(offdesign=['zeta'])
    >>> so_v.set_attr(fluid={'CH4': 1}, m=1, T=50, p=80, design=['m'])
    >>> v_si.set_attr(p=15)
    >>> nw.solve('design')
    >>> nw.save('tmp')
    >>> round(v_si.T.val, 1)
    26.3
    >>> round(v.pr.val, 3)
    0.188

    The simulation determined the area independant zeta value
    :math:`\frac{\zeta}{D^4}`. This zeta remains constant if the cross
    sectional area of the valve opening does not change. Using the zeta value
    we can determine the pressure ratio at a different feed pressure.

    >>> so_v.set_attr(p=70)
    >>> nw.solve('offdesign', design_path='tmp')
    >>> round(so_v.m.val, 1)
    0.9
    >>> round(v_si.T.val, 1)
    30.0
    >>> shutil.rmtree('./tmp', ignore_errors=True)
    """

    @staticmethod
    def component():
        return 'valve'

    def get_variables(self):
        return {
            'pr': dc_cp(
                min_val=1e-4, max_val=1, num_eq=1,
                deriv=self.pr_deriv, func=self.pr_func,
                func_params={'pr': 'pr'}, latex=self.pr_func_doc),
            'zeta': dc_cp(
                min_val=0, max_val=1e15, num_eq=1,
                deriv=self.zeta_deriv, func=self.zeta_func,
                func_params={'zeta': 'zeta'}, latex=self.zeta_func_doc),
            'dp_char': dc_cc(
                param='m', num_eq=1,
                deriv=self.dp_char_deriv, func=self.dp_char_func,
                char_params={'type': 'abs'}, latex=self.dp_char_func_doc)
        }

    def get_mandatory_constraints(self):
        return {
            'mass_flow_constraints': {
                'func': self.mass_flow_func, 'deriv': self.mass_flow_deriv,
                'constant_deriv': True, 'latex': self.mass_flow_func_doc,
                'num_eq': 1},
            'fluid_constraints': {
                'func': self.fluid_func, 'deriv': self.fluid_deriv,
                'constant_deriv': True, 'latex': self.fluid_func_doc,
                'num_eq': self.num_nw_fluids},
            'enthalpy_equality_constraints': {
                'func': self.enthalpy_equality_func,
                'deriv': self.enthalpy_equality_deriv,
                'constant_deriv': True,
                'latex': self.enthalpy_equality_func_doc,
                'num_eq': 1}
        }

    @staticmethod
    def inlets():
        return ['in1']

    @staticmethod
    def outlets():
        return ['out1']

    def dp_char_func(self):
        r"""
        Equation for characteristic line of difference pressure to mass flow.

        Returns
        -------
        residual : ndarray
            Residual value of equation.

            .. math::

                0=p_\mathrm{in}-p_\mathrm{out}-f\left( expr \right)
        """
        p = self.dp_char.param
        expr = self.get_char_expr(p, **self.dp_char.char_params)
        if not expr:
            msg = ('Please choose a valid parameter, you want to link the '
                   'pressure drop to at component ' + self.label + '.')
            logger.error(msg)
            raise ValueError(msg)

        return (
            self.inl[0].p.val_SI - self.outl[0].p.val_SI -
            self.dp_char.char_func.evaluate(expr))

    def dp_char_func_doc(self, label):
        r"""
        Equation for characteristic line of difference pressure to mass flow.

        Parameters
        ----------
        label : str
            Label for equation.

        Returns
        -------
        latex : str
            LaTeX code of equations applied.
        """
        p = self.dp_char.param
        expr = self.get_char_expr_doc(p, **self.dp_char.char_params)
        if not expr:
            msg = ('Please choose a valid parameter, you want to link the '
                   'pressure drop to at component ' + self.label + '.')
            logger.error(msg)
            raise ValueError(msg)

        latex = (
            r'0=p_\mathrm{in}-p_\mathrm{out}-f\left(' + expr +
            r'\right)')
        return generate_latex_eq(self, latex, label)

    def dp_char_deriv(self, increment_filter, k):
        r"""
        Calculate partial derivatives of difference pressure characteristic.

        Parameters
        ----------
        increment_filter : ndarray
            Matrix for filtering non-changing variables.

        k : int
            Position of derivatives in Jacobian matrix (k-th equation).
        """
        if not increment_filter[0, 0]:
            self.jacobian[k, 0, 0] = self.numeric_deriv(
                self.dp_char_func, 'm', 0)
        if self.dp_char.param == 'v':
            self.jacobian[k, 0, 1] = self.numeric_deriv(
                self.dp_char_func, 'p', 0)
            self.jacobian[k, 0, 2] = self.numeric_deriv(
                self.dp_char_func, 'h', 0)
        else:
            self.jacobian[k, 0, 1] = 1

        self.jacobian[k, 1, 1] = -1

    def initialise_source(self, c, key):
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
                4 \cdot 10^5 & \text{key = 'p'}\\
                5 \cdot 10^5 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 4e5
        elif key == 'h':
            return 5e5

    def initialise_target(self, c, key):
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
                5 \cdot 10^5 & \text{key = 'p'}\\
                5 \cdot 10^5 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 5e5
        elif key == 'h':
            return 5e5

    def calc_parameters(self):
        r"""Postprocessing parameter calculation."""
        i = self.inl[0].get_flow()
        o = self.outl[0].get_flow()
        self.pr.val = o[1] / i[1]
        self.zeta.val = ((i[1] - o[1]) * np.pi ** 2 / (
            4 * i[0] ** 2 * (self.inl[0].vol.val_SI + self.outl[0].vol.val_SI)
            ))

    def entropy_balance(self):
        r"""
        Calculate entropy balance of a valve.

        Note
        ----
        The entropy balance makes the follwing parameter available:

        .. math::

            \text{S\_irr}=\dot{m} \cdot \left(s_\mathrm{out}-s_\mathrm{in}
            \right)\\
        """
        self.S_irr = self.inl[0].m.val_SI * (
            self.outl[0].s.val_SI - self.inl[0].s.val_SI)

    def exergy_balance(self, T0):
        r"""
        Calculate exergy balance of a valve.

        Parameters
        ----------
        T0 : float
            Ambient temperature T0 / K.

        Note
        ----
        .. math::

            \dot{E}_\mathrm{P} =
            \begin{cases}
            \text{not defined (nan)} & T_\mathrm{in}, T_\mathrm{out} \geq T_0\\
            \dot{E}_\mathrm{out}^\mathrm{T}
            & T_\mathrm{in} > T_0 \geq T_\mathrm{out}\\
            \dot{E}_\mathrm{out}^\mathrm{T} - \dot{E}_\mathrm{in}^\mathrm{T}
            & T_0 \geq T_\mathrm{in}, T_\mathrm{out}\\
            \end{cases}

            \dot{E}_\mathrm{F} =
            \begin{cases}
            \dot{E}_\mathrm{in}^\mathrm{PH} - \dot{E}_\mathrm{out}^\mathrm{PH}
            & T_\mathrm{in}, T_\mathrm{out} \geq T_0\\
            \dot{E}_\mathrm{in}^\mathrm{T} + \dot{E}_\mathrm{in}^\mathrm{M}-
            \dot{E}_\mathrm{out}^\mathrm{M}
            & T_\mathrm{in} > T_0 \geq T_\mathrm{out}\\
            \dot{E}_\mathrm{in}^\mathrm{M} - \dot{E}_\mathrm{out}^\mathrm{M}
            & T_0 \geq T_\mathrm{in}, T_\mathrm{out}\\
            \end{cases}
        """
        if self.inl[0].T.val_SI > T0 and self.outl[0].T.val_SI > T0:
            self.E_P = np.nan
            self.E_F = self.inl[0].Ex_physical - self.outl[0].Ex_physical
        elif self.outl[0].T.val_SI <= T0 and self.inl[0].T.val_SI > T0:
            self.E_P = self.outl[0].Ex_therm
            self.E_F = self.inl[0].Ex_therm + (
                self.inl[0].Ex_mech - self.outl[0].Ex_mech)
        elif self.inl[0].T.val_SI <= T0 and self.outl[0].T.val_SI <= T0:
            self.E_P = self.outl[0].Ex_therm - self.inl[0].Ex_therm
            self.E_F = self.inl[0].Ex_mech - self.outl[0].Ex_mech
        else:
            msg = ('Exergy balance of a valve, where outlet temperature is '
                   'larger than inlet temperature is not implmented.')
            logger.warning(msg)
            self.E_P = np.nan
            self.E_F = np.nan

        self.E_bus = {
            "chemical": np.nan, "physical": np.nan, "massless": np.nan
        }
        if np.isnan(self.E_P):
            self.E_D = self.E_F
        else:
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
            1: {
                'isoline_property': 'h',
                'isoline_value': self.inl[0].h.val,
                'isoline_value_end': self.outl[0].h.val,
                'starting_point_property': 'v',
                'starting_point_value': self.inl[0].vol.val,
                'ending_point_property': 'v',
                'ending_point_value': self.outl[0].vol.val
            }
        }

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
        if self.inl[0].T.val_SI > T0 and self.outl[0].T.val_SI > T0:
            self.case_one()
        elif self.inl[0].T.val_SI <= T0 and self.outl[0].T.val_SI > T0:
            self.case_two()
        elif self.inl[0].T.val_SI <= T0 and self.outl[0].T.val_SI <= T0:
            self.case_three()
        else:
            ...

        self.C_D = self.c_F * self.E_D * (3600 / 10 ** 9)
        self.r = 100 * (self.c_P - self.c_F) / self.c_F
        self.f = 100 * self.Z_costs / (self.Z_costs + self.C_D)

        # conn calculated
        self.outl[0].eco_check = True

    def case_one(self):
        """if self.inl[0].T.val_SI > T0 and self.outl[0].T.val_SI > T0"""
        """ self.E_P = np.nan
            self.E_F = self.inl[0].Ex_physical - self.outl[0].Ex_physical"""
        # convert units
        unit_C = (3600 / 10 ** 9)
        unit_c = (10 ** 9 / 3600)

        # unaffected chemical exergy
        self.outl[0].c_chemical = self.inl[0].c_chemical
        self.outl[0].C_chemical = self.inl[0].C_chemical

        # F principle
        self.outl[0].c_therm = self.inl[0].c_therm
        self.outl[0].c_mech = self.inl[0].c_mech

        # [outlets] costs streams associated with the fuel (power and [T, M, CH])
        self.outl[0].C_therm = self.outl[0].c_therm * self.outl[0].Ex_therm * unit_C
        self.outl[0].C_mech = self.outl[0].c_mech * self.outl[0].Ex_mech * unit_C

        # fuel costs
        self.C_F = self.inl[0].C_therm - self.outl[0].C_therm + self.inl[0].C_mech - self.outl[0].C_mech
        self.c_F = self.C_F / self.E_F * unit_c

        # product costs
        self.C_P = np.nan
        self.c_P = self.C_P / self.E_P * unit_c

        # [outlets] costs streams associated with the product with P principle (power and [T, M, CH])

        # costs per exergy unit for outlets streams associated with the product (power and [T, M, CH])

        # physical costs streams for all outlets
        self.outl[0].C_physical = self.outl[0].C_therm + self.outl[0].C_mech
        self.outl[0].c_physical = self.outl[0].C_physical / self.outl[0].Ex_physical * unit_c

        # average costs for outlets
        self.outl[0].C_tot = self.outl[0].C_physical + self.outl[0].C_chemical
        self.outl[0].c_tot = self.outl[0].C_tot / self.outl[0].Ex_tot * unit_c

        # dissapative
        self.C_dif = (self.inl[0].C_therm - self.outl[0].C_therm) + (self.inl[0].C_mech - self.outl[0].C_mech) + self.Z_costs
        self.eco_dissipative = True

    def case_two(self):
        """if self.outl[0].T.val_SI <= T0 and self.inl[0].T.val_SI > T0"""
        """ self.E_P = self.outl[0].Ex_therm
            self.E_F = self.inl[0].Ex_therm + (self.inl[0].Ex_mech - self.outl[0].Ex_mech)
        """

        # convert units
        unit_C = (3600 / 10 ** 9)
        unit_c = (10 ** 9 / 3600)

        # unaffected chemical exergy
        self.outl[0].c_chemical = self.inl[0].c_chemical
        self.outl[0].C_chemical = self.inl[0].C_chemical

        # F principle
        self.outl[0].c_mech = self.inl[0].c_mech

        # [outlets] costs streams associated with the fuel (power and [T, M, CH])
        self.outl[0].C_mech = self.outl[0].c_mech * self.outl[0].Ex_mech * unit_C

        # fuel costs
        self.C_F = self.inl[0].C_therm + (self.inl[0].C_mech - self.outl[0].C_mech)
        self.c_F = self.C_F / self.E_F * unit_c

        # product costs
        self.C_P = self.C_F + self.Z_costs
        self.c_P = self.C_P / self.E_P * unit_c

        # [outlets] costs streams associated with the product with P principle (power and [T, M, CH])
        self.outl[0].C_therm = self.c_P * self.outl[0].Ex_therm * unit_C

        # costs per exergy unit for outlets streams associated with the product (power and [T, M, CH])
        self.outl[0].c_therm = self.outl[0].C_therm / self.outl[0].Ex_therm * unit_c

        # physical costs streams for all outlets
        self.outl[0].C_physical = self.outl[0].C_therm + self.outl[0].C_mech
        self.outl[0].c_physical = self.outl[0].C_physical / self.outl[0].Ex_physical * unit_c

        # average costs for outlets
        self.outl[0].C_tot = self.outl[0].C_physical + self.outl[0].C_chemical
        self.outl[0].c_tot = self.outl[0].C_tot / self.outl[0].Ex_tot * unit_c

    def case_three(self):
        """if self.inl[0].T.val_SI <= T0 and self.outl[0].T.val_SI <= T0"""
        """ self.E_P = self.outl[0].Ex_therm - self.inl[0].Ex_therm
            self.E_F = self.inl[0].Ex_mech - self.outl[0].Ex_mech"""

        # convert units
        unit_C = (3600 / 10 ** 9)
        unit_c = (10 ** 9 / 3600)

        # unaffected chemical exergy
        self.outl[0].c_chemical = self.inl[0].c_chemical
        self.outl[0].C_chemical = self.inl[0].C_chemical

        # F principle
        self.outl[0].c_mech = self.inl[0].c_mech

        # [outlets] costs streams associated with the fuel (power and [T, M, CH])
        self.outl[0].C_mech = self.outl[0].c_mech * self.outl[0].Ex_mech * unit_C

        # fuel costs
        self.C_F = (self.inl[0].C_mech - self.outl[0].C_mech)
        self.c_F = self.C_F / self.E_F * unit_c

        # product costs
        self.C_P = self.C_F + self.Z_costs
        self.c_P = self.C_P / self.E_P * unit_c

        # [outlets] costs streams associated with the product with P principle (power and [T, M, CH])
        self.outl[0].C_therm = self.c_P * (self.outl[0].Ex_therm - self.inl[0].Ex_therm) * unit_C + self.inl[0].C_therm

        # costs per exergy unit for outlets streams associated with the product (power and [T, M, CH])
        self.outl[0].c_therm = self.outl[0].C_therm / self.outl[0].Ex_therm * unit_c

        # physical costs streams for all outlets
        self.outl[0].C_physical = self.outl[0].C_therm + self.outl[0].C_mech
        self.outl[0].c_physical = self.outl[0].C_physical / self.outl[0].Ex_physical * unit_c

        # average costs for outlets
        self.outl[0].C_tot = self.outl[0].C_physical + self.outl[0].C_chemical
        self.outl[0].c_tot = self.outl[0].C_tot / self.outl[0].Ex_tot * unit_c
