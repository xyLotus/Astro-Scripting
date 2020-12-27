""" The python side implementation of the Arrays module in astro.
"""
import astropy as apy

__author__  = 'bellrise'
__version__ = '0.1'


def f_len(scope: apy.Scope):
    # params: (buf: arr)
    # comment: Returns the length of an array

    # Get the buffer
    buf: apy.models.Array = scope.get('buf')
    if buf.typeof() != 'arr':
        scope.throw(
            apy.errors.type_error,
            "'buf' parameter needs to be of type Array"
        )

    length = apy.models.Num.new('length', len(buf))
    scope.set('length', length)

    return scope.format()


def f_join(scope: apy.Scope):
    # params: (buf: arr, between: str)
    # comment: Collects the whole array into one string, turns
    # every element into a string before adding to the string.

    # Fetching variables
    buf: apy.models.Array = scope.get('buf')
    between: apy.models.String = scope.get('between')

    # Type checking
    if buf.typeof() != 'arr':
        scope.throw(
            apy.errors.type_error,
            "'buf' parameter needs to be of type Array"
        )
    if between.typeof() != 'str':
        scope.throw(
            apy.errors.type_error,
            "'between' parameter needs to be of type String"
        )

    # Joining
    buffer = [str(i) for i in buf.get()]
    joined = between.get().join(buffer)
    str_ = apy.models.String.new('joined', joined)

    # Setting the buf variable
    scope.set('joined', str_)

    return scope.format()


def __build__():
    """ build function for the Arrays module. """
    return [
        apy.render(f_len, '__Arrays', 'len'),
        apy.render(f_join, '__Arrays', 'join')
    ]
