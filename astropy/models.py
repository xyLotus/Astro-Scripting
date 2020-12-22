""" This contains the python representations of astro data types,
referred to as "models" in astropy. """
from typing import Union
from abc import ABC, abstractmethod


class Variable(ABC):
    """ This represents a single astro variable, it is the top level
    object for all models to inherit from. """

    # Additional slots, this is for speeding up the variable object
    # and decreasing the memory usage of such object.
    __slots__ = ('__length', )

    __name = None
    __type = None
    __data = None

    @classmethod
    @abstractmethod
    def new(cls, name: str, data):
        """ Creates a new Variable object """
        pass

    def get(self):
        """ Returns a pythonic version of the number. """
        return self.__data

    def nameof(self):
        """ Returns the name of the variable. """
        return self.__name

    def typeof(self):
        """ Returns the type of the variable. """
        return self.__type


class String(Variable):
    """ A string """

    @classmethod
    def new(cls, name: str, data: Union[str, bytes]):
        """ Creates a new String object and returns it. """
        if not isinstance(data, (str, bytes)):
            raise TypeError('the passed object is not a string')
        return String(name, data)

    def __init__(self, name: str, data: Union[str, bytes]):
        self.__name = name
        if isinstance(data, bytes):
            self.__data = str(data, 'utf8')
        else:
            self.__data = str(data)
        self.__type = 'str'

    def set(self, data: str):
        """ Set the astro String to the python str """
        if not isinstance(data, str):
            raise TypeError('the passed object is not a string')
        self.__data = data

    def __str__(self):
        return f'String({self.nameof()}, {self.get()})'


class Num(Variable):
    """ A number: int / float """

    @classmethod
    def new(cls, name: str, data: Union[int, float]):
        """ Creates a new Num object and returns it. """
        if not isinstance(data, (int, float)):
            raise TypeError('this passed object cannot be interpreted'
                            'as a number value')
        return Num(name, data)

    def __init__(self, name: str, data):
        """  """
        self.__name = name
        self.__data = data
        self.__type = 'num'

    def __str__(self):
        return f'Num({self.nameof()}, {self.get()})'

    def __add__(self, other):
        return self.get() + other.get()

    def __sub__(self, other):
        return self.get() - other.get()

    def __ge__(self, other):
        return self.get() >= other.get()

    def __eq__(self, other):
        return self.get() == other.get()

    def __floordiv__(self, other):
        return self.get() // other.get()

    def __gt__(self, other):
        return self.get() > other.get()

    def __le__(self, other):
        return self.get() <= other.get()

    def __lt__(self, other):
        return self.get() < other.get()

    def __neg__(self):
        return -self.get()

    def __ne__(self, other):
        return self.get() != other.get()

    def __pos__(self):
        return +self.get()

    def __round__(self, n=None):
        return round(self.get(), 0)

    def __bool__(self):
        if self.get() == 0:
            return False
        return True


class Array(Variable):
    """ A multi-type array. """

    __length: int = 0

    @classmethod
    def new(cls, name: str, data: list):
        """ Creates a new array from the variable arra"""
        for i in data:
            if not issubclass(i, Variable):
                raise TypeError('non-astro data type in array')
        return Array(name, data)

    def __init__(self, name: str, data):
        """ Sets up additional data """
        self.__name = name
        self.__data = data
        self.__type = 'arr'
        self.__length = len(data)

    def __str__(self):
        return f'Array({self.nameof()}, {self.get()})'

    def __len__(self):
        """ Returns the length of the saved array. """
        return self.__length

    def get(self):
        """ Returns the array in python form """
        return self.__data

    def set(self, array: list):
        """ Sets the astro array to the python array. """
        # Type checks
        for i in array:
            if not issubclass(i, Variable):
                raise TypeError(f'non-astro data type in array')
        self.__data = array
        self.__length = len(array)


def create(var: dict):
    """ Returns a variable object from the tuple. """
    if var['type'] == 'str':
        return String(var['name'], var['data'])
    if var['type'] == 'num':
        return Num(var['name'], var['data'])
    if var['type'] == 'arr':
        return Array(var['name'], var['data'])
    raise TypeError('astropy does not support the %s data type' % var[0])
