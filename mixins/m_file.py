""" The python side implementation of the File module in astro.
"""
import astropy as apy
import os

__author__  = 'bellrise'
__version__ = '0.1'

type_e = apy.errors.type_error


def write(scope: apy.Scope, mode):
    """ Internal function for the write/append functions.
    Takes the scope and mode as parameters. """

    data = scope.get('data')
    filename = scope.get('filename')
    # type checking
    if filename.typeof() != 'str':
        scope.throw(type_e, "'filename' has to be of type String")
    if data.typeof() != 'str':
        scope.throw(type_e, "'data' has to be of type String")

    # Writing to the file
    try:
        with open(os.getcwd() + '/' + filename.get(), mode) as f:
            f.write(data)
    except Exception as e:
        scope.throw(apy.errors.file_error, e)

    return scope.format()


def f_read(scope: apy.Scope):
    # params: (filename: str)
    # comment: Reads the whole file and returns it in one string.

    filename = scope.get('filename')
    # type checking
    if filename.typeof() != 'str':
        scope.throw(type_e, "'filename' has to be of type String")

    # Reading the file
    try:
        with open(os.getcwd() + '/' + filename.get()) as f:
            text = f.read()
    except Exception as e:
        scope.throw(apy.errors.file_error, e)

    contents = apy.models.String.new('contents', text)
    scope.place(contents)

    return scope.format()


def f_write(scope: apy.Scope):
    # params: (data: str, filename: str)
    # Writes the given string to the file.

    return write(scope, 'w')


def f_append(scope: apy.Scope):
    # params: (data: str, filename: str)
    # Appends the given string to the file.

    return write(scope, 'a')


def __build__():
    """ Library constructor. """
    return [
        apy.render(f_read, '__File', 'read'),
        apy.render(f_write, '__File', 'write'),
        apy.render(f_append, '__File', 'append')
    ]
