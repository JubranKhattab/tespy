class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass  # The base class doesn't define a specific sound


class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"


class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

# Creating instances of the subclasses
dog = Dog("Buddy") # attribute name is buddy
cat = Cat("Whiskers") # attribute name is Whiskers

# Calling the speak method on the subclasses
print(dog.speak())  # Output: Buddy says Woof!
print(cat.speak())  # Output: Whiskers says Meow!



