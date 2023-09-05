import numpy as np


class componente_one:
    comp_name = 'Turbine'
    inl_c = 14

    inl2_c = 18
    out2_c = 180

    class cost_eq_conn_comp:
        def __get__(self, instance, owner):
            return getattr(instance, self.index_intern)

        def __set__(self, instance, value):
            setattr(instance, self.index_intern, value)

        def __init__(self, index_input):
            self.index_intern = index_input



    # descriptor equal to descriptor
    inl_c_comp = cost_eq_conn_comp('inl_c')
    out_c = cost_eq_conn_comp('inl_c')
    out_c_comp = cost_eq_conn_comp('out_c')

    # from connection to component all the time
    inl2_c_comp = cost_eq_conn_comp('inl2_c')
    out2_c_comp = cost_eq_conn_comp('out2_c')

    Q = 99





turb = componente_one()
print("connection 1 in = component 1 in = component =  1 out = connection 1 out\nhere we test that descriptor[comp in] = descriptor[comp out] \n")
print("inl_c = " + str(turb.inl_c))
print("inl_c_comp = " + str(turb.inl_c_comp))
print("out_c = " + str(turb.out_c))
print("out_c_comp= " + str(turb.out_c_comp))
turb.inl_c = 140
print("inl_c = " + str(turb.inl_c))
print("inl_c_comp = " + str(turb.inl_c_comp))
print("out_c = " + str(turb.out_c))
print("out_c_comp= " + str(turb.out_c_comp))

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

