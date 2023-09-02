
"""A Descriptor is a reusable class"""
import numpy as np


class PositiveMenge1:
    def __get__(self, instance, owner):
        return instance, '-----', owner


class Bestellung1:
    Sorte = 'Orange'
    Anzahl = PositiveMenge1()


bestell1 = Bestellung1()
print(bestell1.Sorte)
print(bestell1.Anzahl)
print("END 1\n\n")
# instance is the object bestell1, owner is the class of te object, that means Bestellung1
# Anzahl ist attribute of Bestellung1 and at the same time an object of the reusable class PositiveMenge1
# when I create the attribute Anzahl, automatically it filled with the return of __get__
# if there is a __set__ function in PositiveMegne, Anzahl will have the vlaue in the __set__ function


class PositiveMenge2:
    def __get__(self, instance, owner):
        return instance.Sorte, instance.Sorte2


class Bestellung2:
    Sorte = 'Orange'
    Sorte2 = 'Apfel'
    Anzahl = PositiveMenge2()


bestell2 = Bestellung2()
print(bestell2.Sorte)
print(bestell2.Anzahl)
print("END 2\n\n")
# all attributes of Bestellung2 Sorte, Sorte2 can be used in the descriptors. They become automatically attributes of instance in PositiveMenge


class PositiveMenge3:
    def __get__(self, instance, owner):
        return instance.Sorte, instance.Sorte2, instance.Sorte3, instance._Sorte3


class Bestellung3:
    Sorte = 'Orange'
    Sorte2 = 'Apfel'
    Sorte3 = 'Banana'
    _Sorte3 = 'Avocado'
    Anzahl = PositiveMenge3()


bestell3 = Bestellung3()
print(bestell3.Sorte)
print(bestell3.Anzahl)
print("END 3 \n\n")
# Attributes with underscore at the beginning are called protected Variables. I can use them in the descriptor but I can't see them in debug
# instance has in it Sorte, Sorte2 and Sorte3. But still I can use _Sorte3


class PositiveMenge4:
    def __get__(self, instance, owner):
        return instance.EineAnzahl


class Bestellung4:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge4()


bestell4 = Bestellung4()
print(bestell4.Sorte)
print('EineAnzahl is ', bestell4.EineAnzahl)
print(bestell4.Anzahl)

bestell4.EineAnzahl = 25
print('EineAnzahl is ', bestell4.EineAnzahl)
print(bestell4.Anzahl)

bestell4.Anzahl = 37
print('EineAnzahl is ', bestell4.EineAnzahl)
print(bestell4.Anzahl)

bestell4.EineAnzahl = 44
print('EineAnzahl is ', bestell4.EineAnzahl)
print(bestell4.Anzahl)
print("END 4\n\n")
# Anzahl will be at first equal to the value of EineAnzahl 10
# If the value of EineAnzahl changes to 25, the value of Anzahl will change to 25, why? because the value of Anzahl is equal to instance.EineAnzahl in get
# If the value of Anzahl {not EIneAnzahl} is changed to 37, it gets the value 37. EineAnzahl is 25
# If I change EineAnzahl from 25 to 44, Anzahl stays 37 {even if in get instance.EineAnzahl stands. Anzahl has been set to 37 with a setter, that's why there is no effect on Anzahl from EineAnzahl}


class PositiveMenge5:
    def __get__(self, instance, owner):
        return instance.EineAnzahl

    def __set__(self, instance, value):
        instance.EineAnzahl = value


class Bestellung5:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge5()


bestell5 = Bestellung5()
print(bestell5.Sorte)
print('EineAnzahl is ', bestell5.EineAnzahl)
print(bestell5.Anzahl)

bestell5.EineAnzahl = 25
print('EineAnzahl is ', bestell5.EineAnzahl)
print(bestell5.Anzahl)

bestell5.Anzahl = 37
print('EineAnzahl is ', bestell5.EineAnzahl)
print(bestell5.Anzahl)

bestell5.EineAnzahl = 44
print('EineAnzahl is ', bestell5.EineAnzahl)
print(bestell5.Anzahl)
print("END 5\n\n")
# Anzahl has always and directly the value of EineAnzahl. When EineAnzahl get a new value, Anzahl gets the same new value.
# AND EineAnzahl has always and directly the value of Anzahl. When Anzahl get a new value, EineAnzahl gets the same new value.
# why is that? because all attributes of Bestellung5 have a link to PositiveMenge5. There are same variables. See Example 6


class PositiveMenge6:
    def __get__(self, instance, owner):  # __get__ is being automatically applied all the time
        print('++++++++++++++++++++   __get__ has been called out  ++++++++++++++++++++')
        return instance.EineAnzahl, instance.Sorte + '__'+str(instance.EineAnzahl)

    def __set__(self, instance, value):  # value is this: bestell6.Anzahl = value.   __set__ called only when "bestell6.Anzahl =" is written
        instance.EineAnzahl = value
        instance.Sorte = instance.Sorte + '__'+str(value)
        print("++++++++++++++++++++   __set__ has been called out  ++++++++++++++++++++")


class Bestellung6:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge6()


bestell6 = Bestellung6()
print(bestell6.Sorte)
print('EineAnzahl is ', bestell6.EineAnzahl)
print(bestell6.Anzahl)  # carry out get
print(' new line \n')

bestell6.EineAnzahl = 25
print(bestell6.Sorte)
print('EineAnzahl is ', bestell6.EineAnzahl)
print(bestell6.Anzahl)  # carry out get
print(' new line \n')

bestell6.Anzahl = 37  # carry out set
print(bestell6.Sorte)
print('EineAnzahl is ', bestell6.EineAnzahl)  # carry out get
print(bestell6.Anzahl)
print(' new line \n')

bestell6.EineAnzahl = 44
print(bestell6.Sorte)
print('EineAnzahl is ', bestell6.EineAnzahl)  # carry out get
print(bestell6.Anzahl)
print("END 6\n\n")
# orange takes only the 37 because the function __set__ is being called when "bestell6.Anzahl =" is applied
# (44, 'Orange__37__44') means:  instance.EineAnzahl = 44, instance.Sorte = Orange__37 und add __instance.EineAnzahl --> Orange__37__44


class PositiveMenge7:
    def __get__(self, instance, owner):  # __get__ is being automatically applied all the time
        return instance.temp_variable

    def __set__(self, instance, value):  # value is this: bestell7.Anzahl = value.   __set__ called only when "bestell7.Anzahl =" is written
        instance.temp_variable = value


class Bestellung7:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge7()


bestell7 = Bestellung7()

bestell7.Anzahl = 9
print('EineAnzahl is ', bestell7.EineAnzahl)
print(bestell7.Anzahl)

bestell7.Anzahl = 54
print('EineAnzahl is ', bestell7.EineAnzahl)
print(bestell7.Anzahl)
print("END 7\n\n")
# if I don't want any dependency of Anzahl, I can use any variable name in the set and get.


class PositiveMenge8:
    def __get__(self, instance, owner):
        return instance.temp_variable

    def __set__(self, instance, value):
        instance.temp_variable = value


class Bestellung8:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge8()


bestell8 = Bestellung8()
print(bestell8.Sorte)
# There is error if I print bestell8.Anzahl here before assigning it a value (like bestell8.Anzahl = 15) because
# temp_variable ist not defined. If EineAnzahl instead of temp_Variable, then no problem.

# print(bestell8.Anzahl)
bestell8.Anzahl = 15
print(bestell8.Anzahl)
print("END 8\n\n")
# either use a defined attribute as Link (EineAnzahl) so you have an init value
# or use undefined variable temp_variable and assign a value for it before carrying it out.


class PositiveMenge9:
    def __get__(self, instance, owner):
        return instance, owner, instance.EineAnzahl

    def __set__(self, instance, value):
        instance.EineAnzahl = value


class Bestellung9:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge9()
    AnzahlB = PositiveMenge9()


bestell9 = Bestellung9()
print(bestell9.Sorte)
print(bestell9.Anzahl)
print(bestell9.AnzahlB)

bestell9.Anzahl = 15
bestell9.AnzahlB = 17
print(bestell9.Anzahl)
print(bestell9.AnzahlB)
print("END 9\n\n")

# descriptors change the variables inside of the objects
# the object bestell9 has 4 attributes, Sorte, EineAnzahl, Anzahl, AnzahlB.
# Anzahl and AnzahlB have always the value of EineAnzahl.
# First print Anzahl and AnzahlB have the value 10. They have exactly the same instance address and owner (see print)
# bestell9.Anzahl = 15 means that the value of Anzahl is now 15. That means also the value of EineAnzahl is now 15. The value in the object has been changed from 10 to 15.
# Because of that, AnzahlB will become 15 (AnzahlB is always equal to EineAnzahl because of te descriptors).

# bestell9.AnzahlB = 17 leads to the same thing. AnzahlB = 17 then EineAnzahl = 17 then Anzahl = 17 --> descriptors change the variables inside of the objects
# We don't want this. We want that the attribute Anzahl and AnzahlB use the logic of the defined descriptors but separately
# To solve that, we must disconnect/separate the descriptor from a specific variable (EineAnzahl). We need dynamic variable
# Anzahl and AnzahlB share now the same variable EineAnzahl
# To do avoid that see example 10


class PositiveMenge10:
    def __get__(self, instance, owner):
        return instance.EineAnzahl

    def __set__(self, instance, value):
        instance.EineAnzahl = value

    def __set_name__(self, owner, name):
        print("++++++++++++++++++++   __set_name__ has been called out  ++++++++++++++++++++")
        print(owner, name)


class Bestellung10:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge10()
    AnzahlB = PositiveMenge10()


bestell10 = Bestellung10()
print("END 10\n\n")
#  set name ist carried out when I create an object of the class bestell10 = Bestellung10()
# owner is the class Bestellung10
# name is allways the name of the variable. Each object of the descriptor (PositiveMenge()) gets a name. This name is equal to the attribute name of the class Bestellung10
# In other words: each time I use the descriptor, a copy of this descriptor is being created with the name of the attribute. So I cane change the value in the descriptor OF an attribute.
# Not all attributes are effected wth these changes


class PositiveMenge11:
    def __get__(self, instance, owner):
        return instance.EineAnzahl

    def __set__(self, instance, value):
        instance.EineAnzahl = value

    def __set_name__(self, owner, name):
        print("++++++++++++++++++++   __set_name__ has been called out  ++++++++++++++++++++")
        self.variable_name_store = name
        print(self.variable_name_store)  # we use self here because each variable/Attribute of the class Bestellung11 is actually independent from the other even though they use the same descriptor
                                        # for the attribute create a variable with the name 'variable_name_store' und assign to it the name of the attribute
                                        # we can use this variable as a store for the value of each attribute like temp_variable in example 7
                                        # see debug with stop point at print self


class Bestellung11:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge11()
    AnzahlB = PositiveMenge11()


bestell11 = Bestellung11()
print("END 11\n\n")


class PositiveMenge12:
    def __get__(self, instance, owner):
        #return instance.EineAnzahl
        return getattr(instance, 'EineAnzahl')

    def __set__(self, instance, value):
        #instance.EineAnzahl = value
        setattr(instance, "EineAnzahl", value)

    # def __set_name__(self, owner, name):
    #     print("++++++++++++++++++++   __set_name__ has been called out  ++++++++++++++++++++")
    #     self.variable_name_store = name


class Bestellung12:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge12()
    AnzahlB = PositiveMenge12()


bestell12 = Bestellung12()

print(bestell12.Sorte)
print(bestell12.Anzahl)
print(bestell12.AnzahlB)

bestell12.Anzahl = 15
bestell12.AnzahlB = 17
print(bestell12.Anzahl)
print(bestell12.AnzahlB)
print("END 12\n\n")
# that is the same of example 9 but with using the functions setattr and getattr. You must give exactly the same name of the variable, on which they depend --> EineAnzahl
# If the name is not correct in getattr -> error because then undefined value
# If the name is not correct in setattr -> the value of Anzahl and AnzahlB will NOT change, when I change the value of EineAnzahl
# Why we need this? In this example 12, Anzahl and AnzahlB are linked and they depend on each other. We want to combine example 11 (set_name) und example 12 (setattr, getattr)
# setattr and getattr look better than instance.Variable but they are (maybe) not necessary for exe eco analysis


class PositiveMenge13:
    def __get__(self, instance, owner):
        #return instance.EineAnzahl
        # return getattr(instance, 'EineAnzahl')
        return getattr(instance, self.variable_name_store)

    def __set__(self, instance, value):
        #instance.EineAnzahl = value
        # setattr(instance, "EineAnzahl", value)
        setattr(instance, self.variable_name_store, value)

    def __set_name__(self, owner, name):
        self.variable_name_store = name + "_"  # I'm not allowed to use the exact same name. You could add something to the name (before or after)


class Bestellung13:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge13()
    AnzahlB = PositiveMenge13()


bestell13 = Bestellung13()


bestell13.Anzahl = 15
bestell13.AnzahlB = 17
print(bestell13.Sorte)
print(bestell13.Anzahl)
print(bestell13.AnzahlB)
print("END 13\n\n")
# I can  assign different value to different attributes that are using the same descriptor



"""
having 2 different classes 'Components' that use the same descriptor for creating costs_comp using the entering costs from the connections
Done:
    It is okay to use the same descriptor with the same connection name for DIFFERENT classes. You can change the value of eac connection or c_comp freely with effecting the other component.
    Through this you CAN'T use the descriptor twice in the SAME class because the entering connections have different names.
Limits:
    that applies of all the entering costs from the connections have the same name, namely 'inl_c_conn'
    each component has only one entering cost connection
ToDo:
    making the connection name dynamic by entering the wanted connection name like this:
        inl_c_comp_1 = in_costs_descriptor(inl_c_conn_1)
        inl_c_comp_2 = in_costs_descriptor(inl_c_conn_2)
"""


class in_costs_descriptor:
    def __get__(self, instance, owner):
        return getattr(instance, "inl_c_conn")

    def __set__(self, instance, value):
        setattr(instance, "inl_c_conn", value)

    def __set_name__(self, owner, name):
        self.variable_name_store = name + "_"  # I'm not allowed to use the exact same name. You could add something to the name (before or after)


class componente:
    comp_name = 'Turbine'
    inl_c_conn = 14
    inl_c_comp = in_costs_descriptor()


class componente2:
    comp_name = 'compressor'
    inl_c_conn = 28
    inl_c_comp = in_costs_descriptor()



comp1 = componente()
comp2 = componente2()

print('names:')
print(comp1.comp_name)
print(comp2.comp_name)
print('\n')

print('in costs')
print(comp1.inl_c_conn)
print(comp2.inl_c_conn)
print('\n')

print('in costs for component')
print(comp1.inl_c_comp)
print(comp2.inl_c_comp)
print('\n')

print('in costs for component after changing c_conn')
comp1.inl_c_conn = 114
print(comp1.inl_c_conn)
print(comp1.inl_c_comp)
comp2.inl_c_conn = 128
print(comp2.inl_c_conn)
print(comp2.inl_c_comp)
print('\n')

print('in costs for component after changing c_comp')
comp1.inl_c_comp = 214
print(comp1.inl_c_conn)
print(comp1.inl_c_comp)
comp2.inl_c_comp = 228
print(comp2.inl_c_conn)
print(comp2.inl_c_comp)


"""First of all we are trying to make it possible to put 2 inputs in a class without one value affecting the other"""


class in_costs_descriptor_one:
    def __get__(self, instance, owner):
        return getattr(instance, self.index_intern)

    def __set__(self, instance, value):
        setattr(instance, self.index_intern, value)

    # def __set_name__(self, owner, name):
    #     self.variable_name_store = name + "_"  # I'm not allowed to use the exact same name. You could add something to the name (before or after)
    def __init__(self, index_input):
        self.index_intern = index_input

class componente_one:
    comp_name = 'Turbine'
    inl_c_conn = 14
    inl_c_conn_B = 18
    inl_c_comp = in_costs_descriptor_one('inl_c_conn')
    inl_c_comp_B = in_costs_descriptor_one('inl_c_conn_B')


comp1_one = componente_one()

print('names:')
print(comp1_one.comp_name)
print('\n')

print('in costs')
print(comp1_one.inl_c_conn)
print(comp1_one.inl_c_conn_B)
print('\n')

print('in costs for component')
print(comp1_one.inl_c_comp)
print(comp1_one.inl_c_conn_B)
print('\n')

print('in costs for component after changing c_conn')
comp1_one.inl_c_conn = 114
print(comp1_one.inl_c_conn)
print(comp1_one.inl_c_conn_B)
print(comp1_one.inl_c_comp)
print(comp1_one.inl_c_comp_B)
print('\n')

print('in costs for component after changing c_comp')
comp1_one.inl_c_comp_B = 218
print(comp1_one.inl_c_conn)
print(comp1_one.inl_c_conn_B)
print(comp1_one.inl_c_comp)
print(comp1_one.inl_c_comp_B)


"""Second of all we are trying to make it possible to put 2 inputs in 2 classes without one value affecting the other"""


class in_costs_descriptor_two:
    def __get__(self, instance, owner):
        return getattr(instance, self.index_intern)

    def __set__(self, instance, value):
        setattr(instance, self.index_intern, value)

    # def __set_name__(self, owner, name):
    #     self.variable_name_store = name + "_"  # I'm not allowed to use the exact same name. You could add something to the name (before or after)
    def __init__(self, index_input):
        self.index_intern = index_input


class componente_two_turbine:
    comp_name = 'Turbine'
    inl_c_conn = 14
    inl_c_conn_B = 18
    inl_c_comp = in_costs_descriptor_two('inl_c_conn')
    inl_c_comp_B = in_costs_descriptor_two('inl_c_conn_B')


class componente_pump:
    comp_name = 'Pump'
    inl_c_conn = 140
    inl_c_conn_B = 180
    inl_c_comp = in_costs_descriptor_two('inl_c_conn')
    inl_c_comp_B = in_costs_descriptor_two('inl_c_conn_B')


turb = componente_two_turbine()
pump = componente_pump()

print('names:')
print(turb.comp_name)
print(pump.comp_name)
print('\n')

print('in costs')
print(turb.inl_c_conn)
print(pump.inl_c_conn)
print(turb.inl_c_conn_B)
print(pump.inl_c_conn_B)
print('\n')

print('in costs for component')
print(turb.inl_c_comp)
print(pump.inl_c_comp)
print(turb.inl_c_conn_B)
print(pump.inl_c_conn_B)
print('\n')

print('in costs for component after changing c_conn')
turb.inl_c_conn = 114
print(turb.inl_c_conn)
print(pump.inl_c_conn)
print(turb.inl_c_conn_B)
print(pump.inl_c_conn_B)
print(turb.inl_c_comp)
print(pump.inl_c_comp)
print(turb.inl_c_comp_B)
print(pump.inl_c_comp_B)
print('\n')

print('in costs for component after changing c_comp')
turb.inl_c_comp_B = 218
print(turb.inl_c_conn)
print(pump.inl_c_conn)
print(turb.inl_c_conn_B)
print(pump.inl_c_conn_B)
print(turb.inl_c_comp)
print(pump.inl_c_comp)
print(turb.inl_c_comp_B)
print(pump.inl_c_comp_B)
