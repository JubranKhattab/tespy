
class Players:
    def __init__(self):
        self.age = None
        self.position = None
        self.foot = None
        # 3 as standard position. you cal select other position to be the standard.
        self.x_pos = 3
        self.y_pos = 3

        # define a method, which can change the attributes of the object
    def move(self, x, y):
        self.x_pos += x
        self.y_pos += y


# define object of the class
attack_1 = Players()


# method
print(attack_1.x_pos)
print(attack_1.y_pos)
attack_1.move(4, 8)
print(attack_1.x_pos)
print(attack_1.y_pos)
