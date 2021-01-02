# python >= 3.6
""" This is the AstroPy module for writing astro libraries in Python.
The way this works, is you register your function with the correct
parameters, process some data in it and then exit the function to
continue running the astro script. On the asx script side, you need
a simple @mixin lib_function in order to execute the function with
the current data in the scope.
"""
import re

__author__  = 'bellrise'
__version__ = '0.2.9'

# Interface imports
from .objects import Scope, Mixin
from . import errors
from . import models


def render(func, lib: str, name: str):
    """ Returns a mixin object for the interpreter to execute when it
    is called in asx code with the @mixin instruction. """

    for i in [lib, name]:
        if not re.match('[A-z].+', i):
            raise RuntimeError('Invalid mixin name')

    return Mixin(func, lib, name)


def void(*r):
    # ! Pulled from llx
    """ This function is used for voiding variables (basically
    doing nothing with them. Any amount of variables can be passed
    to this function. Returns a lambda function returning None.
    :param r: Anything. """
    str(r)
    return lambda: None


def notImplemented(func):
    """ Not implemented decorator for astro functions. Raises
    NotImplemented if you try to use them. """
    def wrapper(*a, **kw):
        void(a, kw)
        raise NotImplementedError(f'{func.__name__} is not implemented yet')
    return wrapper
