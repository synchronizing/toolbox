from builtins import property
from typing import Type


class classproperty(property):
    """Decorator to set a class method as a class property.

    Combines a property and a classmethod into one, creating a class property. Allows
    access to computed class attributes.

    Example:

        .. code-block:: python

            from toolbox.builtins.property import classproperty

            class Animal:
                @classproperty
                def dog(cls):
                    return "whoof!"

            print(Animal.dog) # >>> 'whoof!'
    """

    def __get__(self, cls: Type, owner: object) -> classmethod:
        return classmethod(self.fget).__get__(None, owner)()
