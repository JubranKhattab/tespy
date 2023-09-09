import numpy as np
from tespy.tools import logger
from tespy.tools.helpers import TESPyConnectionError


def init_cost_per_exergy_unit(conn, Exe_Eco):
    r"""
    Declare the cost per exergy unit of every connection then initialize the costs
    per exergy unit of all sources.

    Parameters
    ----------
    conn : class

    Exe_Eco : dict

    Note
    ----


    """
    if Exe_Eco is not None:
        # the variable c_cost is declared for every connection
        conn.c_cost = np.nan
        if conn.source.__class__.__name__ == "Source":
            so_label = conn.source.label + '_c'
            if so_label not in Exe_Eco or Exe_Eco[so_label] is None:
                msg = ('Error assigning cost per exergy unit to a source connection. No value found for ' +
                       conn.source.label + ' in the library Exe_Eco')
                logger.error(msg)
                raise TESPyConnectionError(msg)
            else:
                conn.c_cost = Exe_Eco[so_label]


def check_input_dict(self, Exe_Eco):
    # add Z for Source and Sink as None to avoid errors
    cp_df = self.nw.comps
    so_si_list = cp_df.index[cp_df['comp_type'].isin(["Source", "Sink"])].tolist()
    Exe_Eco.update({f"{item}_Z": None for item in so_si_list})

    # check if every component has Z value: The sum of leveled capital investment costs 'CI' and operating and maintenance costs 'OM'.
    all_comps = cp_df.index[~cp_df['comp_type'].isin(["Source", "Sink"])].tolist()
    missing_comp = [element+'_Z' for element in all_comps if element+'_Z' not in Exe_Eco.keys()]
    if len(missing_comp) != 0:
        msg = ('Error assigning CI and OM costs to some components. No values found for ' +
               ",".join(missing_comp) + ' in the library Exe_Eco. The key in the dictionary Exe_Eco must match with the component label with \'_Z\' a suffix')
        logger.error(msg)
        raise TESPyConnectionError(msg)

    # for busses
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


def find_next_component(cp_df):
    for index, row in cp_df.iterrows():
        cp = row["object"]
        for in_conn in cp.inl:
           if hasattr(in_conn, "eco_check"):
               cp_df.at[index, "num_set_c_i"] += 1
        if hasattr(cp, "eco_check_bus"):
            cp_df.at[index, "num_set_c_i"] += 1
    ready_cp = cp_df[cp_df['num_i'] == cp_df['num_set_c_i']]['object'].tolist()
    cp_df = cp_df[~cp_df['object'].isin(ready_cp)]
    # ToDos add the number of busses inlet for the components in the df. The busses are to find in the network by 'busses
    # the output power of the turbine should hold a c that is the inlet to the pump. -> Turbine should be handled before the pump
    return cp_df, ready_cp


# def assign_busses(self):
#     for b_id, b in self.nw.busses.items():
#         bus_only_for = ['Turbine', 'Compressor', 'Pump']
#         cp_list = b.comps.index.values.tolist()
#         cp_list_names = [type(obj).__name__ for obj in cp_list]
#         if any(c in cp_list_names for c in bus_only_for):
#             for cp in cp_list:
#                 cp.connected_bus = True
#         print("end")


def define_bus_cost(self, Exe_Eco):
    """
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


