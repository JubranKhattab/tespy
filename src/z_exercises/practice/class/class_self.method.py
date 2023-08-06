class Players:
    # so that the attributes could have a clear overview, you can put all the attributes in one or more methods
    def __init__(self):
        self.get_attr_shape()
        self.get_attr_playing()

    # attributes for shape
    def get_attr_shape(self):
        self.age = 20
        self.hair = 'black'
        self.hight = 175

    # attributes for playing
    def get_attr_playing(self):
        self.foot = 'right'
        self.position = 'centre'
        self.x_pos = 3
        self.y_pos = 3

    # actual methods
    def move(self, x, y):
        self.x_pos += x
        self.y_pos += y


attack_1 = Players()
print(attack_1.age)
