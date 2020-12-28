""" This contains the objects for the astropy package, they are mostly for
an abstraction layer on top of the raw data passed around by the interpreter,
and for more convinience. """
from typing import Union, Dict

from . import models

# The Variable type
var_t = Union[models.Num, models.Array, models.String, models.Bool]
var_tuple = (models.Num, models.Array, models.String, models.Bool)


class Scope:
    """ This class defines the variable scope and contains methods used
    to get and put variable data to modify the scope. """

    __vars: Dict[str, var_t] = {}  # Variable container

    def __init__(self, scope: dict):
        """ Contructor. Unpacks the scope dict and collects the variables
        into the __vars container. """

        for name, value in scope.items():
            self.__vars[name] = models.create(name, value)

    def get(self, name: str, default=None):
        """ Returns the variable with the given name, else returns
        the default value. """
        try:
            return self.__vars[name]
        except KeyError:
            return default

    def place(self, var: var_t):
        """ Place the variable onto the scope, without needing its name. """
        self.set(var.nameof(), var)

    def set(self, name: str, var: var_t):
        """ Set the variable """
        if not isinstance(var, var_tuple):
            raise TypeError('this only accepts astropy models')

        if isinstance(var, models.Array):
            # Convert each item into a astro version of it
            for i, e in enumerate(var):
                var[i] = (e.typeof(), e.get())

        self.__vars[name] = var

    def throw(self, err, why):
        """ Throws an error for the interpreter to catch. """
        raise RuntimeError(f'{err}::{why}')

    def format(self):
        """ Returns a data format that the interpreter can understand. """
        container = {}
        for name, value in self.__vars.items():
            name: str
            value: var_t
            container[name] = (value.typeof(), value.get())

        return container


class Mixin:
    """ This class represents a mixin object passed to the interpreter
    for it to be executed. """

    __slots__ = ('name', 'func')

    def __init__(self, func, lib: str, name: str):
        """ Constructor of the mixin object. The name checks are executed
        in the render function. """

        self.name = lib + '#' + name
        self.func = func

    def execute(self, data):
        """ Execute the current function with the passed scope (variable
        data), and return any data from the function. """

        return self.func(Scope(data))
