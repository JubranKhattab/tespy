from tespy.tools.helpers import mass_flow
from CoolProp.CoolProp import PropsSI as PSI
import pandas as pd
import plotly.graph_objects as go
import json


#exhaust_m = {'Ar': 0.012457896607378277, 'C3H8': 0, 'CH4': 0, 'CO2': 0.06886347922097558, 'H2': 0, 'H2O': 0.05583016579437184, 'N2': 0.7351524120278958,
#           'O2': 0.12753952306032723, 'ethane': 0, 'n-Butane': 0, 'n-Hexane': 9.739355621090751e-05, 'n-Pentane': 5.9087691508375354e-05}
exhaust_m = {'Ar': 0.01250537983922654, 'C3H8': 0, 'CH4': 0, 'CO2': 0.06983061549520793, 'H2': 0, 'H2O': 0.05645744063702813, 'N2': 0.7347999095200368,
             'O2': 0.1262482891545452, 'ethane': 0, 'n-Butane': 0, 'n-Hexane': 9.853974508085118e-05, 'n-Pentane': 5.9783072773752946e-05}



air_n = { "CO2": 0.00027, "ethane": 0, "N2": 0.78092, "C3H8": 0, "CH4": 0,  "O2": 0.20947, "H2O":0, "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0, "Ar":0.00934, "H2": 0 }

fuel_n = {"CO2": 0.01800, "ethane": 0.03600, "N2": 0.10300, "C3H8": 0.00600, "CH4": 0.83380,  "O2": 0.000010, "H2O":0, "n-Butane": 0.00200, "n-Pentane": 0.00050, "n-Hexane": 0.00069, "Ar":0, "H2": 0}

water_m = {"CO2": 0, "ethane": 0, "N2": 0, "C3H8": 0, "CH4": 0,  "O2": 0, "H2O":1, "n-Butane": 0, "n-Pentane": 0, "n-Hexane": 0, "Ar":0, "H2": 0 }


def humid_air(T, rh, air_n):
    psatH2O = PSI('P', 'Q', 0, 'T', T + 273.15, 'water') * 0.00001
    pH2O = float(rh) / 100 * psatH2O

    xH2O = PSI('M', 'water') * (pH2O / 1.013) / (
        pH2O / 1.013 * PSI('M', 'water') + (1 - pH2O / 1.013) * PSI('M', 'air'))

    air_0 = {key: value * (1 - xH2O) for key, value in air_n.items()}
    air_0['H2O'] = xH2O
    air_m = calc_mass_flow(air_0)
    return air_m


def calc_mass_flow(flow_n):
    flow_m = mass_flow(flow_n)
    return flow_m


def under_cool(conn, delta):
    p_sat = conn.p.val
    psatH2O = PSI('T', 'Q', 0, 'P', p_sat, 'water') - 273.15


def sat_p(T):
    psatH2O = PSI('P', 'Q', 0, 'T', T + 273.15, 'water') * 0.00001
    return psatH2O


# comp_list = nw.comps.index.tolist()
# for comp in comp_list:
#     print(comp.strip("'"))
costs_c= {
    "Source 1_c": 0,
    "Source 10_c": 15,
    # "Source 14_c": 112,
    "Source 35_c": 10,
    "Source 71_c": 1,
    "Source 91_c": 0,
    "temp_func": True,
}


costs_c_power ={
    "P1_c": 10,
    "P2_c": 10,
    "P3_c": 10,
    "P4_c": 10,
    "V_c": 10
}

costs_Z = {
    "BK_Z": 80,
    "DRbe2_Z": 5,
    "DRbe3_Z": 5,
    "DRbe4_Z": 5,
    "DRue1_Z": 5,
    "DRue3_Z": 5,
    "DRue4_Z": 5,
    "DRue5_Z": 5,
    "DRue6_Z": 5,
    "DT1_Z": 250,
    "DT2_Z": 250,
    "DT3_Z": 250,
    "DT4_Z": 250,
    "DT5_Z": 250,
    "EXP_Z": 700,
    "ECO1_Z": 100,
    "ECO2_Z": 100,
    "ECO3_Z": 100,
    "ECO4_Z": 100,
    "HK1_Z": 80,
    "HK2_Z": 80,
    "HK3_Z": 80,
    "KON_Z": 80,
    "kvw_Z": 100,
    "Mix DT3_Z": 5,
    "Mix FW1_Z": 5,
    "Mix FW2_Z": 5,
    "Mix KON_Z": 5,
    "MIX TIT_Z": 5,
    "Mix ZUH_Z": 5,
    "P1_Z": 10,
    "P2_Z": 10,
    "P3_Z": 10,
    "P4_Z": 10,
    "Sink 31_Z": 0,
    "Sink 33_Z": 0,
    "Sink 74_Z": 0,
    "Sink 85_Z": 0,
    "Sink 88_Z": 0,
    "Sink 93_Z": 0,
    "Source 1_Z": 0,
    "Source 10_Z": 0,
    # "Source 14_Z": 0,
    "Source 35_Z": 0,
    "Source 71_Z": 0,
    "Source 91_Z": 0,
    "Splitter BVW_Z": 5,
    "Splitter FW1_Z": 5,
    "Splitter FW2_Z": 5,
    "Splitter FW3_Z": 5,
    "Splitter KVW_Z": 5,
    "Splitter P2_Z": 5,
    "Splitter V_Z": 5,
    "UH1_Z": 160,
    "UH2_Z": 160,
    "UH3_Z": 160,
    "UH4_Z": 160,
    "UH5_Z": 160,
    "UH6_Z": 160,
    "V_Z": 700,
    "VD1_Z": 180,
    "VD2_Z": 180,
    "VD3_Z": 180,
    "VW_Z": 100,
    "ZUH1_Z": 160,
    "ZUH2_Z": 160,
    "ZUH3_Z": 160
}


def c_steam_gen(exp_comp, df):
    hx_list = ['ECO1', 'ECO2', 'ECO3', 'ECO4', 'kvw', 'UH1', 'UH2', 'UH3', 'UH4', 'UH5', 'UH6', 'VD1', 'VD2',
               'VD3', 'ZUH1', 'ZUH2', 'ZUH3']
    # hx_list_comp = [comp for comp in nw.comps.object if comp.label in hx_list]
    hx_list_comp = df[df.index.isin(hx_list)]['object'].tolist()
    conn_source = next((comp for comp in hx_list_comp if comp.label == 'UH4'), None).inl[0]

    c_therm = conn_source.c_therm
    c_mech = conn_source.c_mech
    c_physical = conn_source.c_physical
    c_chemical = conn_source.c_chemical

    for hx in hx_list_comp:
        hx.outl[0].c_therm = c_therm
        hx.outl[0].c_mech = c_mech
        hx.outl[0].c_physical = c_physical
        hx.outl[0].c_chemical = c_chemical
        fill_cost(hx)


def fill_cost(comp):
    unit_C = (3600 / 10 ** 9)
    comp.outl[0].C_therm = comp.outl[0].c_therm * comp.outl[0].Ex_therm * unit_C
    comp.outl[0].C_mech = comp.outl[0].c_mech * comp.outl[0].Ex_mech * unit_C
    comp.outl[0].C_physical = comp.outl[0].c_physical * comp.outl[0].Ex_physical * unit_C
    comp.outl[0].C_chemical = comp.outl[0].c_chemical * comp.outl[0].Ex_chemical * unit_C
    comp.outl[0].eco_check = True


def c_sp_vw(ready_list, df):
    hx_list = ['VW']
    # hx_list_comp = [comp for comp in nw.comps.object if comp.label in hx_list]
    hx_list_comp = df[df.index.isin(hx_list)]['object'].tolist()
    conn_source = next((comp for comp in ready_list if comp.label == 'HK1'), None).outl[0]

    c_therm = conn_source.c_therm
    c_mech = conn_source.c_mech
    c_physical = conn_source.c_physical
    c_chemical = conn_source.c_chemical

    for hx in hx_list_comp:
        hx.outl[0].c_therm = c_therm
        hx.outl[0].c_mech = c_mech
        hx.outl[0].c_physical = c_physical
        hx.outl[0].c_chemical = c_chemical
        fill_cost(hx)

# c35
# c_therm = 35.85
# c_mech = 19.26
# c_physical = 35.85
# c_chemical = 10 random


def sankey_diagram(ean):
    path = 'C:/TU-Berlin/01_Masterarbeit/excel_read/'
    links, nodes = ean.generate_plotly_sankey_input()
    with open(path+'links.json', 'w') as pickle_file:
        json.dump(links, pickle_file)

    with open(path+'nodes.json', 'w') as json_file:
        json.dump(nodes, json_file)

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node={
            "label": nodes,
            'pad': 11,
            'color': 'orange'},
        link=links))
    #plot(fig, filename=path+'sankey')
    fig.show()



fmt_dict = {
    'E_F': {
        'unit': ' [MW]',
        'float': '{:.2f}',
        'factor': 1e6,
    },
    'E_P': {
        'unit': '  [MW]',
        'float': '{:.2f}',
        'factor': 1e6,
    },
    'E_D': {
        'unit': '  [MW]',
        'float': '{:.2f}',
        'factor': 1e6,
    },
    'E_L': {
        'unit': '  [MW]',
        'float': '{:.2f}',
        'factor': 1e6,
    },
    'epsilon': {
        'unit': '  [%]',
        'float': '{:.1f}',
        'factor': 1 / 100,
        'markdown_header': 'ε'
    },
    'y_Dk': {
        'unit': '  [%]',
        'float': '{:.1f}',
        'factor': 1 / 100
    },
    'y*_Dk': {
        'unit': '  [%]',
        'float': '{:.1f}',
        'factor': 1 / 100
    },
    'group': {

    },
    'C_F': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'C_P': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'C_D': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'Z_costs': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'c_F': {
        'unit': '  [€/GJ]',
        'float': '{:.2f}',
        'factor': 1
    },
    'c_P': {
        'unit': '  [€/GJ]',
        'float': '{:.2f}',
        'factor': 1
    },
    'r': {
        'unit': '  [%]',
        'float': '{:.2f}',
        'factor': 1
    },
    'f': {
        'unit': '  [%]',
        'float': '{:.2f}',
        'factor': 1
    },
    'e_T': {
        'unit': '  [kJ/kg]',
        'float': '{:.1f}',
        'factor': 1000
    },
    'e_M': {
        'unit': '  [kJ/kg]',
        'float': '{:.1f}',
        'factor': 1000
    },
    'e_PH': {
        'unit': '  [kJ/kg]',
        'float': '{:.1f}',
        'factor': 1000
    },
    'e_CH': {
        'unit': '  [kJ/kg]',
        'float': '{:.1f}',
        'factor': 1000
    },
    'E_T': {
        'unit': '  [MW]',
        'float': '{:.2f}',
        'factor': 1e6
    },
    'E_M': {
        'unit': '  [MW]',
        'float': '{:.2f}',
        'factor': 1e6
    },
    'E_PH': {
        'unit': '  [MW]',
        'float': '{:.2f}',
        'factor': 1e6
    },
    'E_CH': {
        'unit': '  [MW]',
        'float': '{:.2f}',
        'factor': 1e6
    },
    'c_PH': {
        'unit': '  [€/GJ]',
        'float': '{:.2f}',
        'factor': 1
    },
    'c_T': {
        'unit': '  [€/GJ]',
        'float': '{:.2f}',
        'factor': 1
    },
    'c_M': {
        'unit': '  [€/GJ]',
        'float': '{:.2f}',
        'factor': 1
    },
    'c_CH': {
        'unit': '  €/GJ',
        'float': '{:.2f}',
        'factor': 1
    },
    'c_tot': {
        'unit': '  [€/GJ]',
        'float': '{:.2f}',
        'factor': 1
    },
    'C_PH': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'C_T': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'C_M': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'C_CH': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'C_tot': {
        'unit': '  [€/h]',
        'float': '{:.2f}',
        'factor': 1
    },
    'T': {
        'unit': '  [°C]',
        'float': '{:.1f}',
        'factor': 1
    },
    'p': {
        'unit': '  [bar]',
        'float': '{:.2f}',
        'factor': 1
    },
    'h': {
        'unit': '  [kJ/kg]',
        'float': '{:.1f}',
        'factor': 1
    }
}


def result_to_markdown(df, filename,  df_type, prefix=''):
    if df_type == 'connections':
        df['numeric_part'] = df.index.str.extract('(\d+)', expand=False)
        df['numeric_part'] = pd.to_numeric(df['numeric_part'], errors='coerce')
        df = df.sort_values(by='numeric_part')
        df = df.drop(columns='numeric_part')
    df.drop(columns='group', errors='ignore', inplace=True)
    for col in df.columns:
        fmt = fmt_dict[col]['float']
        if prefix == 'δ ':
            unit = ' in %'
            df[col] *= 100
        else:
            unit = fmt_dict[col]['unit']
            df[col] /= fmt_dict[col]['factor']
        for row in df.index:
            df.loc[row, col] = str(fmt.format(df.loc[row, col]))
        if 'markdown_header' not in fmt_dict[col]:
            fmt_dict[col]['markdown_header'] = col

        df = df.rename(columns={
            col: prefix + fmt_dict[col]['markdown_header'] + unit
        })
    df.to_markdown(
        filename, disable_numparse=True,
        colalign=['left'] + ['right' for _ in df.columns]
    )
    path = 'C:/TU-Berlin/01_Masterarbeit/excel_read/results_df/'
    df.to_excel(path+df_type+'.xlsx')


def power_costs(nw):
    wanted_id = ['P1', 'P2', 'P3', 'P4', 'DT1', 'DT2', 'DT3', 'DT4', 'DT5', 'V', 'EXP']
    comps_df = nw.comps
    comp_bus = comps_df[comps_df.index.isin(wanted_id)]['object'].tolist()
    columns = ['power', 'c', 'C']
    df = pd.DataFrame(columns=columns)
    for c in comp_bus:
        row = {'power': c.exe_eco['E_streams_tot']['E_Power'],
               'c':c.exe_eco['c_per_unit']['c_Power'] ,
               'C':c.exe_eco['C_streams']['C_Power'] }
        index_value = c.label
        df = df.append(pd.Series(row, name=index_value))

    path = 'C:/TU-Berlin/01_Masterarbeit/excel_read/'
    df.to_excel(path + 'results_df/power_costs' + '.xlsx')
    print('end')
