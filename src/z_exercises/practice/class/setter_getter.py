class AgeCalculator:
    def __init__(self):
        self._age1 = 1
        self._age2 = 26

    @property
    def age1(self):
        return self._age1

    @age1.setter
    def age1(self, new_age1):
        self._age1 = new_age1
        self._age2 = new_age1 * 2

    @property
    def age2(self):
        return self._age2

    def sumsum(self):
        self.sums = self._age1 + self._age2

# Creating an instance of the class
Jubran_calc = AgeCalculator()


print("Age1:", Jubran_calc.age1)  # Output: Age1: 0
print("Age2:", Jubran_calc.age2)

Jubran_calc.age1 = 30

print("Age1:", Jubran_calc.age1)  # Output: Age1: 10
print("Age2:", Jubran_calc.age2)

print("sumsum:", Jubran_calc.sumsum())
print('end')
