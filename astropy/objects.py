""" This contains the objects for the astropy package, they are mostly for
an abstraction layer on top of the raw data passed around by the interpreter,
and for more convinience. """
from typing import List, Union

from . import models

# The Variable type
var_t = Union[models.Num, models.Array, models.String]


class Scope:
    """ This class defines the variable scope and contains methods used
    to get and put variable data to modify the scope. """

    __vars: List[var_t] = []  # Variable container

    def __init__(self, scope: dict):
        """ Contructor. Unpacks the scope dict and collects the variables
        into the __vars container. """

        # todo: receive the scope format from the interpreter and parse
        # todo: it collecting the variables into the __vars container.

        # v TEMP
        __temporary = [
            {'name': 'x',       'type': 'str', 'data': 'some string'},
            {'name': 'number',  'type': 'num', 'data': 123},
            {'name': 'my_nums', 'type': 'arr', 'data': [1, 2, 3, '4']}
        ]
        variables = __temporary
        # ^ TEMP

        for var in variables:
            self.__vars.append(models.create(var))

    def get_variable(self, name: str):
        """ Returns a variable with the given name. """
        for var in self.__vars:
            if var.nameof() == name:
                return var
        return None

    def set_variable(self, name: str, var: var_t):
        """ Set the variable """
        if not issubclass(var, models.Variable):
            raise TypeError('this only accepts astropy Variable objects')
        # Check for existing var
        to_replace = None
        for var in self.__vars:
            if var.nameof() == name:
                to_replace = var

        if to_replace:
            index = self.__vars.index(to_replace)
            self.__vars[index] = var
        else:
            self.__vars.append(var)

    def throw(self, err, why):
        """ Throws an error for the interpreter to catch. """
        raise RuntimeError(f'{err}::{why}')

    def format(self):
        """ Returns a data format that the  """


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
