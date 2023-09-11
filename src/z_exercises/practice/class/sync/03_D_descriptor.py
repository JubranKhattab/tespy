import numpy as np


class cost_eq_conn_comp:
    def __get__(self, instance, owner):
        return instance.inl_c + instance.Z * 22

    # def __set__(self, instance, value):
    #     instance.out_c = value


class componente_one:
    def __init__(self):
        self.comp_name = 'Turbine'
        self.inl_c = 14
        self.Z = 50

        self.out_c = cost_eq_conn_comp()


turb = componente_one()
print("Connection out = function of connection in: out_c = inl_c + Z * 22 \n")
print("Z = " + str(turb.Z))
print("inl_c = " + str(turb.inl_c))
print("out_c = " + str(turb.out_c))
turb.inl_c = 140
print("inl_c = " + str(turb.inl_c))
print("out_c = " + str(turb.out_c))


print('--------------------- \n---------------------')
print("component 2 in = connection 2 in    and   connection 2 out = component 2 out \nWe want to build a relationship with equation between the component in and out\n")


print("inl2_c = " + str(turb.inl2_c))
print("inl2_c_comp = " + str(turb.inl2_c_comp))
print("out2_c_comp= " + str(turb.out2_c_comp))
print("out2_c = " + str(turb.out2_c))

print('\ndo exergy economic balance and calculate out2_c_comp by multiplying component 2 in with 500\n')
# like exergy balance
turb.out2_c_comp = turb.inl2_c_comp * 500

print("inl2_c = " + str(turb.inl2_c))
print("inl2_c_comp = " + str(turb.inl2_c_comp))
print("out2_c_comp= " + str(turb.out2_c_comp))
print("out2_c = " + str(turb.out2_c))


print('\nChange Connection 2 in and see what happen\n')
# todo_: if Component in changes, tComponent out should also change. In other words: The equation in the exergy balance should always apply
turb.inl2_c = 22
print("inl2_c = " + str(turb.inl2_c))
print("inl2_c_comp = " + str(turb.inl2_c_comp))
print("out2_c_comp= " + str(turb.out2_c_comp))
print("out2_c = " + str(turb.out2_c))

