class Greet:
  def __init__(self, country, greeting):
    self.country = country
    self.greeting = greeting
    self.greet = greeting + " from " + country


first = Greet('France', 'Bonjour')
print(first.greet)
# when the user only updates greeting or country, the variable greet is not updated
first.country = 'Germany'
print(first.greet)


"""-----------------------------------------------------------------"""


class Greet2:
  def __init__(self, country, greeting):
    self.country = country
    self.greeting = greeting
  def greet(self):
    return self.greeting + " from " + self.country


second = Greet2('Germany', 'Hallo')
print(second.greet())  # call a method that why ()
# update the country, the variable greet is updated because it is a function that has been called
second.country = 'Italy'
print(second.greet())


"""-----------------------------------------------------------------"""
# The @property decorator allows a function to be accessed like an attribute. No need to call the function
# that means Greet and Greet2 become Greet3


class Greet3:
  def __init__(self, country, greeting):
    self.country = country
    self.greeting = greeting
  @property
  def greet(self):
    return self.greeting + " from " + self.country


third = Greet3('Spain', 'Hola')
print(third.greet)  # greet is not a method more. call a variable without ()
# update the country, the variable greet is updated because it is a function that has been called
third.country = 'Portugal'
print(third.greet)
