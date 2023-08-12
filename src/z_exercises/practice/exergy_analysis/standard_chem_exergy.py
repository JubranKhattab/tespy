import json
import tespy.data.ChemEx as stand_chem_ex


def stand_ch_exe_dict(model):
    module_path = stand_chem_ex.__path__[0]
    file_name = f'/{model}.json'
    file_path = module_path + file_name
    with open(file_path, 'r') as json_file:
        ch_exe_dict = json.load(json_file)
        return ch_exe_dict


if __name__ == '__main__':
    model = 'Ahrendts'
    # model = 'Szargut1988'
    # model = 'Szargut2007'
    ch_exe_dict = stand_ch_exe_dict(model)
    print('end')



