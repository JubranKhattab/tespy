import numpy as np
from tespy.tools import logger
from tespy.tools.helpers import TESPyConnectionError
import math


def init_cost_per_exergy_unit(conn, Exe_Eco):
    r"""
    Declare the cost per exergy unit of every connection then initialize the costs
    per exergy unit of all sources, check if all source streams has values for c and raise error if not.

    Parameters
    ----------
    conn : class

    Exe_Eco : dict

    Note
    ----


    """
    if Exe_Eco is not None:
        # the variable c_tot is declared for every connection
        conn.c_tot = np.nan
        if conn.source.__class__.__name__ == "Source":
            so_label = conn.source.label + '_c'
            if so_label not in Exe_Eco or Exe_Eco[so_label] is None:
                msg = ('Error assigning cost per exergy unit to a source connection. No value found for ' +
                       conn.source.label + ' in the library Exe_Eco')
                logger.error(msg)
                raise TESPyConnectionError(msg)
            else:
                conn.c_tot = Exe_Eco[so_label]


def check_input_dict(self, Exe_Eco):
    """
    In this function the dict Exe_Eco is being checked to avoid errors in the simulation.
        1. Assign CI and OM costs to all sources and sinks as None. So every component has a value for Z and the user must not add Z costs for component like Source and Sink.
        2. Check if every other component has a value for c in the dict. If not an error is being raised with the name of the components that missing.
        3. Check if every power consumption turbomachinery (pumps and compressors) has a value c for the power cost.
            Either is a value defined or the component is assigned to a turbine, so that the product costs of the turbine "power" are the same as the input for the pump or compressor

    Parameters
    ----------
    self : Class
        object of ExergyAnalysis

    Exe_Eco : Dict
        costs of all Components Z and allocation for power consumers components.

    Returns
    -------
    Exe_Eco

    todo: Currently the costs of the supplied power (for pumps and compressor) must be entered as a value.
     The function needs to be expanded when the power generated in the process is used and no power is purchased from outside.
     To do this, the functions in Turbine must be able to override the costs of the associated component.
     Turbine should turn on "eco_check_bus" in the pump or compressor

    """
    # add Z for Source and Sink as None to avoid errors
    cp_df = self.nw.comps
    so_si_list = cp_df.index[cp_df['comp_type'].isin(["Source", "Sink"])].tolist()
    Exe_Eco.update({f"{item}_Z": np.nan for item in so_si_list})

    # check if every component has Z value: The sum of leveled capital investment costs 'CI' and operating and maintenance costs 'OM'.
    all_comps = cp_df.index[~cp_df['comp_type'].isin(["Source", "Sink"])].tolist()
    missing_comp = [element+'_Z' for element in all_comps if element+'_Z' not in Exe_Eco.keys()]
    if len(missing_comp) != 0:
        msg = ('Error assigning CI and OM costs to some components. No values found for ' +
               ",".join(missing_comp) + ' in the library Exe_Eco. The key in the dictionary Exe_Eco must match with the component label with \'_Z\' a suffix')
        logger.error(msg)
        raise TESPyConnectionError(msg)

    # for busses - not used
    values = [value for key, value in Exe_Eco.items() if isinstance(value, str)]
    all_comps_c = {item + "_c" for item in all_comps}
    missing_values = list(set(values) - all_comps_c)
    keys_for_missing_values = [key for key, value in Exe_Eco.items() if value in missing_values]

    if len(missing_values) != 0:
        msg = ('Error assigning internal power costs to some components. No values found for ' +
               ",".join(keys_for_missing_values) + ' in the library Exe_Eco. The key in the dictionary Exe_Eco must match with the wanted component label with \'_c\' a suffix')
        logger.error(msg)
        raise TESPyConnectionError(msg)

    return Exe_Eco


def create_components_df(self):
    """
    In this function a dataframe is being created with all components except for sources. every row is for one component. The columns are component type, object,
    number of connections entering the components, number of connections entering the components with already calculated cost per exergy c.
    For pumps and compressors the number of input connections is increased by 1 because of the input power.
      If the input power costs is entered from the user as a value, the known number of connection cost is increased by 1 as well.
      If the input power costs is assign to a turbine, this cost should be calculated from the turbine first, before applying the exergy economic balance
      on the pumps and compressors - this case is not implemented to the end. every power cost should be entered from the user for pumps and compressors

    The function returns also a list of all sources to assign the source stream costs to the linked connection.
    Parameters
    ----------
    self

    Returns
    -------
    sources_list : List
        includes all source components.
     df : dataframe
        includes all components of the network except for sources.
    """
    df = self.nw.comps.copy()
    df['num_set_c_i'] = 0
    sources_list = []
    for index, row in df.iterrows():
        cp = row["object"]
        df.at[index, 'num_i'] = cp.num_i
        if hasattr(cp,'bus_costs'):
            if cp in cp.bus_costs.outl:
                df.at[index, 'num_i'] += 1
                if cp.bus_costs.c_cost_out[f"{cp.label+'_c'}"] is not None and not isinstance(cp.bus_costs.c_cost_out[f"{cp.label+'_c'}"], str):
                    df.at[index, 'num_set_c_i'] += 1
        if cp.__class__.__name__ == 'Source':
            sources_list.append(cp)
            df = df.drop(df[df['object'] == cp].index)
    return sources_list, df


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
        cost_id = f"c_tot_{conn.target_id}"
        c_per_unit[cost_id] = conn.c_tot

        # read and calculate E from inlet
        E_id = f"E_tot_{conn.target_id}"
        E_streams_tot[E_id] = conn.Ex_physical + conn.Ex_chemical

        # calculate C
        C_id = f"C_tot_{conn.target_id}"
        C_streams[C_id] = c_per_unit[cost_id]*E_streams_tot[E_id] * (3600 / 10 ** 9)

    for conn in self.outl:
        # declare c for outlet
        cost_id = f"c_tot_{conn.source_id}"
        c_per_unit[cost_id] = conn.c_tot

        # read and calculate E from outlet
        E_id = f"E_tot_{conn.source_id}"
        E_streams_tot[E_id] = conn.Ex_physical + conn.Ex_chemical

        # declare C for outlet
        C_id = f"C_tot_{conn.source_id}"
        C_streams[C_id] = c_per_unit[cost_id] * E_streams_tot[E_id] * (3600 / 10 ** 9)

    # add all variables {c, C, E} as attributes for the components.
    for d in list(dict_dicts.values()):
        dict_name = list(dict_dicts.keys())[list(dict_dicts.values()).index(d)]
        for key, value in d.items():
            self.exe_eco[f"{dict_name}"][f"{key}"] = value


def find_next_component(cp_df, checked_conn):
    """
    This function takes a dataframe with all components of the network to carry out the exergy economic balance.
    This function return the components, for which the exergy economic balance can be executed. That applies for the components with already known and calculated cost per exergy unit c
    for every entering connection as mass stream or power. After every round of applying the exergy economic balance this function is being carried out to find the next ready components.
    Parameters
    ----------
    cp_df : dataframe
        takes the dataframe with the components, for which the exergy economic balance has not been carried out yet because not all entering costs are known.
    checked_conn : list
        includes all already check connections, if any of them has 'eco_check' means that c is now known. No need to add 1 to the column 'num_set_c_i' every time
         while waiting for calculating c of  the other entering connection.
    Returns
    -------
    cp_df : dataframe
        Includes all components of the network, for which the exergy economic balance has not been carried out yet

    ready_cp : dataframe
        Includes all components of the network, for which the exergy economic balance can now be carried out.

    """
    for index, row in cp_df.iterrows():
        cp = row["object"]
        for in_conn in cp.inl:
            if hasattr(in_conn, "eco_check"):
                if in_conn not in checked_conn:
                    cp_df.at[index, "num_set_c_i"] += 1
                    checked_conn.append(in_conn)
        if hasattr(cp, "eco_check_bus"):
            cp_df.at[index, "num_set_c_i"] += 1
            del cp.eco_check_bus
    ready_cp = cp_df[cp_df['num_i'] == cp_df['num_set_c_i']]['object'].tolist()
    cp_df = cp_df[~cp_df['object'].isin(ready_cp)]
    return cp_df, ready_cp


def define_bus_cost(self, Exe_Eco):
    """
    --- **** not used **** ---
    declare a class for every added bus that helps to assign the associated costs with the bus. The attributes of this class are:
        inl: list of all components that generate power and feed it in the bus like turbines. These are named here input components

        num_i: number of these components (input components) that generate power

        c_cost_in: dictionary of input components. The keys are components labels and values are declared as nan and to be calculated as out put in exergy economic balance

        outl: list of all components that consume power out of the bus like compressors und pumps. These are named here output components

        num_o: number of these components (output components) that consume power

        c_cost_out: dictionary of output components. The keys are output components labels and values are read from the Exe_Eco dict.
            Either are the values the labels of Input components, from which the power comes. The costs are calculated previously
            or the user enter the real cost /GJ in the Exe_Eco for the output components

    Parameters
    ----------
    self : Class
        object of ExergyAnalysis

    Exe_Eco : dict


    """
    for b_id, b in self.nw.busses.items():
        bus_only_for = ['Turbine', 'Compressor', 'Pump']
        cp_list = b.comps.index.values.tolist()
        cp_list_names = [type(obj).__name__ for obj in cp_list]
        if any(c in cp_list_names for c in bus_only_for):
            bus_costs = Bus_cost(b, Exe_Eco)
            for c in bus_costs.inl + bus_costs.outl:
                c.bus_costs = bus_costs
            for c in bus_costs.c_cost_out:
                if c not in Exe_Eco:
                    msg = ('Error assigning internal power costs to some components. No values found for ' +
                           c + ' in the library Exe_Eco. The key in the dictionary Exe_Eco must match with the wanted component label with \'_c\' a suffix')
                    logger.error(msg)
                    raise TESPyConnectionError(msg)



class Bus_cost:
    def __init__(self, bus, Exe_Eco):
        self.label = bus.label
        self.inl = self.inlet_comp(bus)
        self.num_i = len(self.inl)
        self.outl = self.outlet_comp(bus)
        self.num_o = len(self.outl)
        self.c_cost_in = self.costs_in(self.inl)
        self.c_cost_out = self.costs_out(Exe_Eco, self.outl)

    def inlet_comp(self, bus):
        inl = [index for index, value in bus.comps[bus.comps['P_ref'] < 0].iterrows()]
        return inl

    def outlet_comp(self, bus):
        outl = [index for index, value in bus.comps[bus.comps['P_ref'] > 0].iterrows()]
        return outl

    def costs_in(self, inl):
        return {comp.label+'_c': None for comp in inl}

    def costs_out(self, Exe_Eco, outl):
        return {comp.label+'_c': Exe_Eco.get(comp.label + "_c") for comp in outl}


def conn_print_exe_eco(self):
    for conn in self.nw.conns['object']:
        conn_exergy_eco_data = [conn.c_physical,conn.c_therm, conn.c_mech,conn.c_chemical,
                                conn.C_physical,conn.C_therm, conn.C_mech,conn.C_chemical,
                                conn.c_tot, conn.C_tot]
        self.connection_data.loc[conn.label, ['c_PH', 'c_T', 'c_M', 'c_CH',
                                              'C_PH', 'C_T', 'C_M', 'C_CH',
                                              'c_tot', 'C_tot']] = conn_exergy_eco_data


def comp_print_exe_eco(self):
    # todo: add c_f c_p, C_D, r and f
    var_list = ['C_F', 'C_P', 'c_F', 'c_P', 'C_D', 'Z_costs', 'r', 'f']

    for comp in self.nw.comps['object']:
        comp_exergy_eco_data = [getattr(comp, var) for var in var_list]
        self.component_data.loc[comp.label, var_list] = comp_exergy_eco_data
def nan_to_zero(self):
    # when the mechanical or chemical exergy is zero.
    c_list = ["c_therm", "c_mech", "c_physical", "c_chemical"]
    for conn in self.outl:
        for c in c_list:
            if hasattr(conn, c):
                attr_value = getattr(conn, c)
                if math.isnan(attr_value):
                    setattr(conn, c, 0)

#  todos: exergy economic balance of the overall system
