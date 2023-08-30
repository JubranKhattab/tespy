"""
The setter is a method that is used to set the property's value.

In OOP, the getter and setter pattern suggests that public attributes should be used only when you’re sure that no one will ever need to attach behavior to them.
If an attribute is likely to change its internal implementation, then you should use getter and setter methods.

Implementing the getter and setter pattern requires:

1-Making your attributes non-public --> _attribute instead of attribute
2-Writing getter and setter methods for each attribute

more: https://realpython.com/python-getter-setter/#replacing-getters-and-setters-with-more-advanced-tools
"""


"""
Adding getter and setter methods to your classes can considerably increase the number of lines in your code.
Getters and setters also follow a repetitive and boring pattern that’ll require extra time to complete. This pattern can be error-prone and tedious.
You’ll also find that the immediate functionality gained from all this additional code is often zero.

All this sounds like something that Python developers wouldn’t want to do in their code. In Python, you’ll probably write the Label class like in the following snippet:

class Label:
    def __init__(self, text, font):
        self.text = text
        self.font = font

Here, .text, and .font are public attributes and are exposed as part of the class’s API. This means that your users can and will change their value whenever they like.
Making your attributes public, like in the above example, is a common practice in Python. In these cases, switching to getters and setters will introduce breaking changes.
 So, how do you deal with situations that require adding behavior to your attributes? The Pythonic way to do this is to replace attributes with properties.

The Pythonic way to attach behavior to an attribute is to turn the attribute itself into a property.
 Properties pack together methods for getting, setting, deleting, and documenting the underlying data. Therefore, properties are special attributes with additional behavior.
You can use properties in the same way that you use regular attributes. When you access a property, its attached getter method is automatically called.
Likewise, when you mutate the property, its setter method gets called.
"""

from datetime import date

class Employee:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

    @property
    def name(self):
        return self._name
    # the value of the attribute 'name' is saved locally in the class as '_name' -> non-public

    @name.setter
    def name(self, value):
        self._name = value.upper()
    # editing the value of the attribute 'name'
    # object.name('John') --> value='John' --> locally attribute '_name' will be the value 'John' as upper case.
    # from the property, the attribute 'name' will get the new value of the local attribute '_name' that means 'JOHN'

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = date.fromisoformat(value)
        # new value of _birth_date is the result of the function fromisoformat in date by entering a value in ( ) when setting it

