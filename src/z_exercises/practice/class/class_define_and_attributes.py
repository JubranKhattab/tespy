
class Players:
    def __init__(self):
        self.age = 20
        self.position = None
        self.foot = 'right'


# define object of the class
attack_1 = Players()

# see where the object is saved on my computer
# attack_1 = Players() means that the variable attack_1 has the address at which the object is saved on the computer
# the address leads you to the place (pointer), where all the data and attributes of this object are saved. Is as the reference (address) of the object.
# print the address:
print(attack_1)

# why __init__?
# when I define a class, it's like the structure of the objects (players) that I want to have.
# every object (player) must have an age, a foot and a position. Here there is nothing saved on my computer. It is only a definition.
# In other words. Only when I create the object will it have this structure. So only when...
# Because all objects have the same attributes, overwriting can occur. The init function therefore does the following: Whenever an object (player) is defined,
# a certain memory location (address) must be reserved for it. These attributes must be in each address --> init automatically places them in this memory location after creating the object
# So self is required for assigning the attributes to the created object.
# attack_1.age = None is equal to ´self.age in the class. I must not call attack_1.age to create this attribute at the address because it happens automatically after creating the object
# the attribute is not defined yet. It says only here, that the object CAN have this attribute.
# define/assign attributes
attack_1.age = "33"
attack_1.foot = "left"
# that means go the address 0x0000014D2D4AE5C0 and search for the attribute age und fill it with 33. The attribute was there because of the init method
print(attack_1.age)
print(attack_1.foot)


