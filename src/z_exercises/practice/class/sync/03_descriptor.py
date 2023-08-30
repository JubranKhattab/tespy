
"""A Descriptor is a reusable class"""


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
# Attributes with underscore at the beginning are called protected Variables. I can use them in the descriptor but I cant see them in debug
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
# If the value of EineAnzahl changes to 25, the vlaue of Anzahl will change to 25, why? because the value of Anzahl is equal to instance.EineAnzahl in get
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
    def __get__(self, instance, owner):  # __get__ is being automatically applied al the time
        return instance.EineAnzahl, instance.Sorte + '__'+str(instance.EineAnzahl)

    def __set__(self, instance, value):  # value is this: bestell6.Anzahl = value.   __set__ called only when "bestell6.Anzahl =" is written
        instance.EineAnzahl = value
        instance.Sorte = instance.Sorte + '__'+str(value)


class Bestellung6:
    Sorte = 'Orange'
    EineAnzahl = 10
    Anzahl = PositiveMenge6()


bestell6 = Bestellung6()
print(bestell6.Sorte)
print('EineAnzahl is ', bestell6.EineAnzahl)
print(bestell6.Anzahl)

bestell6.EineAnzahl = 25
print(bestell6.Sorte)
print('EineAnzahl is ', bestell6.EineAnzahl)
print(bestell6.Anzahl)

bestell6.Anzahl = 37
print(bestell6.Sorte)
print('EineAnzahl is ', bestell6.EineAnzahl)
print(bestell6.Anzahl)

bestell6.EineAnzahl = 44
print(bestell6.Sorte)
print('EineAnzahl is ', bestell6.EineAnzahl)
print(bestell6.Anzahl)
print("END 6\n\n")
# orange takes only the 37 because the function __set__ is being called when "bestell6.Anzahl =" is applied



class PositiveMenge7:
    def __get__(self, instance, owner):  # __get__ is being automatically applied al the time
        return instance.temp_variable

    def __set__(self, instance, value):  # value is this: bestell6.Anzahl = value.   __set__ called only when "bestell6.Anzahl =" is written
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
    print('.')


bestell9 = Bestellung9()
print(bestell9.Sorte)
print(bestell9.Anzahl)
print(bestell9.AnzahlB)

bestell9.Anzahl = 15
bestell9.AnzahlB = 17
print(bestell9.Anzahl)
print(bestell9.AnzahlB)

# descriptors change the variables inside of the objects
# the object bestell9 has 4 attributes, Sorte, EineAnzahl, Anzahl, AnzahlB.
# Anzahl and AnzahlB have always the value of EineAnzahl.
# First print Anzahl and AnzahlB have the value 10. They have exactly the same instance address and owner (see print)
# bestell9.Anzahl = 15 means that the value of Anzahl is now 15. That means also the value of EineAnzahl is now 15. The value in the object has been changed from 10 to 15.
# Because of that, AnzahlB will become 15 (AnzahlB is always equal to EineAnzahl because of te descriptors).

# bestell9.AnzahlB = 17 leads to the same thing. AnzahlB = 17 then EineAnzahl = 17 then Anzahl = 17 --> descriptors change the variables inside of the objects
# We don't want this. We want that the attribute Anzahl and AnzahlB use the logic of the defined descriptors but separately
# To solve that, we must disconnect/separate the descriptor from a specific variable (EineAnzahl)
# To do that see example 10
