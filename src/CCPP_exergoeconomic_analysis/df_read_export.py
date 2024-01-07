import pandas as pd
import json
import plotly.graph_objects as go

def conn_col():
    conn_col = ['e_PH  [kJ/kg]', 'e_T  [kJ/kg]', 'e_M  [kJ/kg]', 'E_PH  [MW]', 'E_T  [MW]', 'E_M  [MW]', 'e_CH  [kJ/kg]', 'E_CH  [MW]', 'c_PH  [€/GJ]', 'c_T  [€/GJ]', 'c_M  [€/GJ]', 'c_CH  €/GJ',
     'C_PH  [€/h]', 'C_T  [€/h]', 'C_M  [€/h]', 'C_CH  [€/h]', 'c_tot  [€/GJ]', 'C_tot  [€/h]']
    return conn_col


def modify_general(df):
    df.set_index('Unnamed: 0', inplace=True)
    df.fillna('-', inplace=True)
    return df


def connections_gas(df_thermo, df_exe_eco):
    all_cols = list(df_thermo.columns.values)
    unwanted = ['v', 'vol', 'x', 'Td_bp']
    wanted_id = ['1', '2', '3', '7', '8', '10', '12', '13', '14']
    therm_list = ['m', 'p', 'h', 'T', 's']
    df_thermo = df_thermo.drop(unwanted, axis=1)
    df_thermo = df_thermo[df_thermo.index.isin(wanted_id)]
    df_thermo['h'] = df_thermo['h'] / 1000
    df_thermo['s'] = df_thermo['s'] / 1000
    for col in df_thermo.columns:
        if col not in therm_list:
            df_thermo[col] = df_thermo[col] * 100
            df_thermo[col] = df_thermo[col].round(4).astype(str)
        else:
            df_thermo[col] = df_thermo[col].round(2).astype(str)
    # print latex thermodynamics table with mass fraction
    # print(df_thermo.to_latex())

    # take exergy values for gas turbine system
    df_exe_eco = df_exe_eco[df_exe_eco.index.isin(wanted_id)]
    df_exe = df_exe_eco.filter(regex='^(?!c_|C_)')
    df_thermo['H'] = df_thermo['m'].astype(float) * df_thermo['h'].astype(float)/1000
    df_thermo_2 = df_thermo[['m','p','h', 'T', 'H']]
    df_therm_exe = pd.merge(df_thermo_2, df_exe, left_index=True, right_index=True)
    df_therm_exe = df_therm_exe.astype(float)
    df_therm_exe['e_tot'] = 1000*(df_therm_exe['E_CH  [MW]'] + df_therm_exe['E_PH  [MW]']) / df_therm_exe['m']
    df_therm_exe['E_tot'] = (df_therm_exe['E_CH  [MW]'] + df_therm_exe['E_PH  [MW]'])
    for col in df_therm_exe.columns:
        df_therm_exe[col] = df_therm_exe[col].round(2).astype(str)
    # print latex exergy table with m, T, p and H
    # print(df_therm_exe.to_latex())

    # take economic values
    df_econ = df_exe_eco.filter(regex='^(c_|C_)')
    for col in df_econ.columns:
        df_econ[col] = df_econ[col].round(1).astype(str)
    # print latex exergy table with m, T, p and H
    print(df_econ.to_latex())



    not_frac = ['m', 'p', 'h', 'T', 's']


def connections_dampf(df_thermo, df_exe_eco):
    wanted = ['m', 'p', 'h', 'T', 's', 'x']
    wanted_id = ['1', '2', '3', '7', '8', '10', '12', '13']
    therm_list = ['m', 'p', 'h', 'T', 's']
    df_thermo = df_thermo[wanted]
    df_thermo = df_thermo[~df_thermo.index.isin(wanted_id)]
    df_thermo['h'] = df_thermo['h'] / 1000
    df_thermo['s'] = df_thermo['s'] / 1000
    for col in df_thermo.columns:
            df_thermo[col] = df_thermo[col].round(2).astype(str)
    df_thermo['x'] = df_thermo['x'].astype(float).apply(lambda x: '-' if x <= 0 else x)
    df_thermo.at['32', 'x'] = 0
    df_thermo['numeric_part'] = df_thermo.index.str.extract('(\d+)', expand=False)
    df_thermo['numeric_part'] = pd.to_numeric(df_thermo['numeric_part'], errors='coerce')
    df_thermo = df_thermo.sort_values(by='numeric_part')
    df_thermo = df_thermo.drop(columns='numeric_part')
    # print latex thermodynamics table with mass fraction
    # print(df_thermo.to_latex())

    # take exergy values for gas turbine system
    df_exe_eco = df_exe_eco[~df_exe_eco.index.isin(wanted_id)]
    df_exe = df_exe_eco.filter(regex='^(?!c_|C_)')
    df_thermo['H'] = df_thermo['m'].astype(float) * df_thermo['h'].astype(float)/1000
    df_thermo_2 = df_thermo[['m','p','h', 'T', 'H']]
    df_therm_exe = pd.merge(df_thermo_2, df_exe, left_index=True, right_index=True)
    df_therm_exe = df_therm_exe.astype(float)
    df_therm_exe['e_tot'] = 1000*(df_therm_exe['E_CH  [MW]'] + df_therm_exe['E_PH  [MW]']) / df_therm_exe['m']
    df_therm_exe['E_tot'] = (df_therm_exe['E_CH  [MW]'] + df_therm_exe['E_PH  [MW]'])
    for col in df_therm_exe.columns:
        df_therm_exe[col] = df_therm_exe[col].round(2).astype(str)
    # print latex exergy table with m, T, p and H
    # print(df_therm_exe.to_latex())

    # take economic values
    df_econ = df_exe_eco.filter(regex='^(c_|C_)')
    for col in df_econ.columns:
        df_econ[col] = df_econ[col].round(1).astype(str)
    # print latex exergy table with m, T, p and H
    print(df_econ.to_latex())

    not_frac = ['m', 'p', 'h', 'T', 's']


def components_gas(df_comp):
    df_comp.set_index('Unnamed: 0', inplace=True)
    wanted_id = ['V', 'Splitter V', 'DRue1', 'BK', 'MIX TIT', 'EXP']
    df_comp = df_comp[~df_comp.index.str.contains('Source|Sink')]
    df_comp = df_comp[df_comp.index.isin(wanted_id)]
    df_comp = df_comp.sort_index()
    df_comp = df_comp.astype(float)
    df_comp.insert(df_comp.columns.get_loc('Z') + 1, 'Z+ C_D', df_comp['Z'] + df_comp['C_D'])
    df_comp = df_comp.sort_values(by='Z+ C_D', ascending=False)
    for col in df_comp.columns:
        df_comp[col] = df_comp[col].round(1).astype(str)
    df_comp.replace('nan', '-', inplace=True)
    # print latex exergy table with m, T, p and H
    print(df_comp.to_latex())
    print('end')


def components_dampf(df_comp):
    df_comp.set_index('Unnamed: 0', inplace=True)
    wanted_id = ['V', 'Splitter V', 'DRue1', 'BK', 'MIX TIT', 'EXP']
    df_comp = df_comp[~df_comp.index.str.contains('Source|Sink')]
    df_comp = df_comp[~df_comp.index.isin(wanted_id)]
    df_comp = df_comp.sort_index()
    df_comp = df_comp.astype(float)
    df_comp.insert(df_comp.columns.get_loc('Z') + 1, 'Z+ C_D', df_comp['Z'] + df_comp['C_D'])
    df_comp = df_comp.sort_values(by='Z+ C_D', ascending=False)
    for col in df_comp.columns:
        df_comp[col] = df_comp[col].round(1).astype(str)
    df_comp.replace('nan', '-', inplace=True)
    # print latex exergy table with m, T, p and H
    print(df_comp.to_latex())
    print('end')


def components_bus(df_comp_bus):
    df_comp_bus.set_index('Unnamed: 0', inplace=True)
    # wanted_id_gas = ['V', 'EXP']
    wanted_id_dampf = ['P1', 'P2', 'P3', 'P4', 'DT1', 'DT2', 'DT3', 'DT4', 'DT5']
    df_comp_bus = df_comp_bus[df_comp_bus.index.isin(wanted_id_dampf)]
    df_comp_bus = df_comp_bus.sort_index()
    for col in df_comp_bus.columns:
        df_comp_bus[col] = df_comp_bus[col].round(2).astype(str)
    # print latex exergy table with m, T, p and H
    print(df_comp_bus.to_latex())
    print('end')


def power_costs(df_power):
    df_power.set_index('Unnamed: 0', inplace=True)
    df_power['power'] = df_power['power'] / 1000000
    for col in df_power.columns:
        df_power[col] = df_power[col].round(2).astype(str)
    # print latex exergy table with m, T, p and H
    df_power = df_power.sort_index()
    print(df_power.to_latex())
    print('end')

def sankey_func():
    labels = ["GuD ", "Brennstoff", "Luft", "Kühlwasser", "Verdichter", "Pumpe1", "Pumpe2", "Pumpe3", "Pumpe4", "Z: CI & OM", "Fernwärme", "Dampfturbine1", "Dampfturbine2", "Dampfturbine3", "Dampfturbine4", "Dampfturbine5", "Expander", "Drosseln - diss", "Kondensator - diss", 'Abgas']
    source = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    target = [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    value = [57633.37, 0.001, 0.001, 11846.29, 13.68, 6.25, 66.33, 9.98, 5770.00, 5197.75, 4251.52, 6572.50, 2296.08, 1365.65, 3105.58, 49874.85, 432, 705.55, 1543.35]
    value_str = list(map(lambda x: str(int(round(x))), value))
    value_str.insert(0,"")
    label_value = [a + '   ' + b +' €/h' for a, b in zip(labels, value_str)]
    label_value[0] = "GuD "
    color_list = [
        'orangered',
        'black',
        'black',
        'lightskyblue', # verdichter
        'lightskyblue',
        'lightskyblue',
        'lightskyblue',
        'lightskyblue',
        'lightseagreen',
        'greenyellow',
        'lightskyblue',
        'lightskyblue',
        'lightskyblue',
        'lightskyblue',
        'lightskyblue',
        'lightskyblue',
        'darkgrey',
        'darkgrey',
        'darkred'
    ]
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        arrangement="perpendicular", # ['snap', 'perpendicular', 'freeform', 'fixed']
        node=dict(
            pad=25,
            thickness=20,
            line=dict(color="white", width=0.5),
            label=label_value,
            color='darkgrey',

        ),
        link=dict(
            source=source,
            target=target,
            #label=value_str,
            value=value,
            color=color_list,
        ),
    )])

    fig.update_layout(
        showlegend=True,
        font=dict(size=30, color='black'),
        plot_bgcolor='yellow',
        paper_bgcolor='lightgrey'

    )
    # Show figure
    fig.show()


def sankey_network(path_sankey):
    with open(path_sankey + 'links.json', 'r') as json_file:
        links = json.load(json_file)
    with open(path_sankey + 'nodes.json', 'r') as json_file:
        nodes = json.load(json_file)

    filtered_lists = [(s, t, val, co) for s, t, val, co  in zip(links['source'], links['target'], links['value'], links['color']) if t not in {84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73} ] # 84 ED. 83 EL
    source, target, value, color = zip(*filtered_lists)
    # filtered_lists = [(s, t, val, co) for s, t, val, co in zip(source, target, value, color) if
    #                    t not in {1,2,3,4}]  # 84 ED. 83 EL
    # source, target, value, color = zip(*filtered_lists)
    links = {'source': source, 'target': target, 'value': value, 'color': color}
    fig = go.Figure(go.Sankey(
        arrangement="freeform",
        node={
            "label": nodes,
            'pad': 11,
            'color': 'orange'},
        link=links))
    # plot(fig, filename=path+'sankey')

    fig.update_layout(
        showlegend=True,
        font=dict(size=30, color='black'),
        #plot_bgcolor='yellow',
        paper_bgcolor='white'

    )
    fig.show()

def sankey_all():
    # Define the data
    labels = ["GT", "GT Vernichtung", "Source95", "Source1", "Source10", "Sink94", "SourcePumpen",
              "SinkDampfturbinen", "SinkKond", "SinkAbgas", "DKW", "DKWVernichtung", "SinkFernwärme"]

    labels_pers = ['','33 %', '31 %', '0 %', '100 %', '69 %', '0 %', '16 %', '0 %', '5 %', '30 %', '5 %', '5 %']
    labels_mwh = ['', '349 MWh', '332 MWh', '5 MWh', '1067 MWh', '732 MWh', '3 MWh', '172 MWh', '3 MWh', '49 MWh', '323 MWh', '54 MWh', '48 MWh']

    source = [2, 4, 3, 0, 0, 0, 10, 10, 10, 10, 6, 10]
    target = [0, 0, 0, 5, 1, 10, 12, 9, 7, 8, 10, 11]

    value_pers = [31, 100, 0.01, 69, 33, 30, 5, 5, 16, 0.01, 0.01, 5]

    colorlist = ['lightpink', 'lightpink', 'lightpink', 'lightgreen', 'orangered', 'grey', 'lightgreen', 'lightblue', 'lightgreen', 'lightblue', 'lightpink', 'orangered']


    fig = go.Figure(data=[go.Sankey(
        arrangement="freeform",  # ['snap', 'perpendicular', 'freeform', 'fixed']
        node=dict(
            pad=50,
            thickness=5,
            line=dict(color="grey", width=2.5),
            label=labels_pers,
            color='black',

        ),
        link=dict(
            arrowlen=100,
            source=source,
            target=target,
            value=value_pers,
            color='lightgrey'

        ),
    )])

    fig.update_layout(
        showlegend=True,
        font=dict(size=30, color='black'),
        plot_bgcolor='white',
        paper_bgcolor='white'

    )
    # Show figure
    fig.show()

def sankey_vernichtung():
    # Define the data
    labels = ["GT", "DKW", "BK", "EXP", "V", "MIX TIT", "DRue1", "Splitter V", "Abhitze", "MischerDrossel", "Heizkondensator", "TurbinePumpe", "KondesatorVorwärmer"]
    sources = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    sources_gt = [0, 0, 0, 0, 0, 0]
    sources_dkw = [ 1, 1, 1, 1, 1, 1, 1, 1]
    targets_dt = [2, 3, 4, 5, 6, 7]
    targets_dkw = [8, 9, 10, 11, 12, None, None, None]
    targets = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, None, None, None]
    targets_gt = [2, 3, 4, 5, 6, 7]
    targets_dkw = [8, 9, 10, 11, 12, None, None, None]
    values = [281.6, 33.7, 17.2, 14.8, 0.6, 0.001, 25.0, 4.3, 6.7, 13.0, 4.8, None, None, None]
    values_gt = [281.6, 33.7, 17.2, 14.8, 0.6, 0.001]
    values_dkw = [25.0, 4.3, 6.7, 13.0, 4.8, None, None, None]

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",  # ['snap', 'perpendicular', 'freeform', 'fixed']
        node=dict(
            pad=50,
            thickness=5,
            line=dict(color="black", width=2.5)

        ),

        link=dict(arrowlen=100,
                  source=sources_gt, # sources_dkw
                  target=targets_gt, # targets_dkw
                  value=values_gt))]) # values_dkw

    # Update the layout
    fig.update_layout( font_size=10)

    # Show the plot
    fig.show()


if __name__ =='__main__':
    path = 'C:/TU-Berlin/01_Masterarbeit/excel_read/results_df/'
    filename_thermo_connections = "thermodynamics_conn.xlsx"
    filename_connections = "connections.xlsx"
    filename_components = "components.xlsx"
    filename_components_bus = "components_bus_agg.xlsx"
    filename_power = "power_costs.xlsx"
    filename_network = "network.xlsx"

    df_thermo = pd.read_excel(path + filename_thermo_connections)
    df_exergy_eco = pd.read_excel(path + filename_connections)

    # df_thermo = modify_general(df_thermo)
    # df_exergy_eco = modify_general(df_exergy_eco)

    # connections_gas(df_thermo, df_exergy_eco)
    # connections_dampf(df_thermo, df_exergy_eco)

    # df_comp = pd.read_excel(path + filename_components)
    # components_gas(df_comp)
    # components_dampf(df_comp)

    # df_comp_bus = pd.read_excel(path + filename_components_bus)
    # components_bus(df_comp_bus)

    # df_power = pd.read_excel(path + filename_power)
    # power_costs(df_power)

    # network_exe_eco() # here

    # sankey_func()

    # sankey_all()

    sankey_vernichtung()

    #path_sankey = 'C:/TU-Berlin/01_Masterarbeit/excel_read/'
    #sankey_network(path_sankey)






# df = df.round(2).astype(str)
    # with open('output_table.tex', 'w') as f:
    #     f.write(df)

