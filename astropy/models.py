""" This contains the python representations of astro data types,
referred to as "models" in astropy. """
from typing import Union
from abc import ABC, abstractmethod


class Variable(ABC):
    """ This represents a single astro variable, it is the top level
    object for all models to inherit from. """

    # Additional slots, this is for speeding up the variable object
    # and decreasing the memory usage of such object.
    __slots__ = ('_length', )

    _name = None
    _type = None
    _data = None

    @classmethod
    @abstractmethod
    def new(cls, name: str, data):
        """ Creates a new Variable object """
        pass

    def get(self):
        """ Returns a pythonic version of the number. """
        return self._data

    def nameof(self):
        """ Returns the name of the variable. """
        return self._name

    def typeof(self):
        """ Returns the type of the variable. """
        return self._type

    def __str__(self):
        """ Returns the basic string representation of the variable.
        Works pretty much the same as the __repr__. """
        return f'{self.__class__.__name__}({self.nameof()}, {self.get()})'

    def __repr__(self):
        """ Returns the representation of the object. Currently
        just returns the __str__ method with a 'models.' prefix """
        return 'models.' + self.__str__()


class String(Variable):
    """ A string """

    @classmethod
    def new(cls, name: str, data: Union[str, bytes]):
        """ Creates a new String object and returns it. """
        if not isinstance(data, (str, bytes)):
            raise TypeError('the passed object is not a string')
        return String(name, data)

    def __init__(self, name: str, data: Union[str, bytes]):
        self._name = name
        if isinstance(data, bytes):
            self._data = str(data, 'utf8')
        else:
            self._data = str(data)
        self._type = 'str'

    def set(self, data: str):
        """ Set the astro String to the python str """
        if not isinstance(data, str):
            raise TypeError('the passed object is not a string')
        self._data = data


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
        """ Constructor """
        self._name = name
        self._data = data
        self._type = 'num'

    def _ch(self, other):
        if isinstance(other, Num):
            return other.get()
        return other

    def __add__(self, other):
        return self.get() + self._ch(other)

    def __sub__(self, other):
        return self.get() - self._ch(other)

    def __ge__(self, other):
        return self.get() >= self._ch(other)

    def __eq__(self, other):
        return self.get() == self._ch(other)

    def __floordiv__(self, other):
        return self.get() // self._ch(other)

    def __gt__(self, other):
        return self.get() > self._ch(other)

    def __le__(self, other):
        return self.get() <= self._ch(other)

    def __lt__(self, other):
        return self.get() < self._ch(other)

    def __neg__(self):
        return -self.get()

    def __ne__(self, other):
        return self.get() != self._ch(other)

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

    _length: int = 0

    @classmethod
    def new(cls, name: str, data: list):
        """ Creates a new array from the variable arra"""
        for i in data:
            if not isinstance(i, (Array, Num, String, Bool)):
                raise TypeError('non-astro data type in array')
        return Array(name, data)

    def __init__(self, name: str, data):
        """ Sets up additional data """
        self._name = name
        self._data = data
        self._type = 'array'
        self._length = len(data)

    def __len__(self):
        """ Returns the length of the saved array. """
        return self._length

    def set(self, array: list):
        """ Sets the astro array to the python array. """
        # Type checks
        for i in array:
            if not isinstance(i, (Array, Num, String, Bool)):
                raise TypeError(f'non-astro data type in array')
        self._data = array
        self._length = len(array)

    def __getitem__(self, item):
        """ Returns the model at the index """
        return self._data[item]

    def __setitem__(self, key, value):
        """ Sets the model at the index to something else """
        self._data[key] = value


class Bool(Variable):
    """ Boolean type. """

    @classmethod
    def new(cls, name: str, data):
        """ Creates a new Bool instance from a python bool """
        if not isinstance(data, bool):
            raise TypeError("'data' has to be of type bool")
        return Bool(name, data)

    def __init__(self, name: str, data):
        """ Constructor. """
        self._data = data
        self._name = name
        self._type = 'bool'

    def __bool__(self):
        """ Simple bool check integration. """
        return self._data


# FOR THE FUTURE, NOT IMPLEMENTED IN CODE YET.
class Map(Variable):
    """ An array of key-value pairs. Dynamicaly typed. """

    _length: int = 0

    @classmethod
    def new(cls, name: str, data):
        pass

    def __init__(self, name: str, data):
        """ Constructor """
        pass

    def __len__(self):
        """ Returns the length of the map. """
        pass

    def valueof(self, key):
        """ Returns the value of the key. """
        pass

    def keyof(self, value):
        """ Returns the key of the value. """
        pass

    def __contains__(self, item):
        """ Returns true if the key exists in the Map. """
        pass

    def set(self, key, value):
        """ Set the value at the current key. """
        pass


def create(name, value):
    """ Returns a variable object from the tuple. """
    if value[0] == 'str':
        return String(name, value[1])
    if value[0] == 'num':
        return Num(name, value[1])
    if value[0] == 'array':
        return Array(name, value[1])
    if value[0] == 'bool':
        return Bool(name, value[1])
    raise TypeError('astropy does not support the %s data type' % value[0])
