""" The python side implementation of the String module in astro.
"""
import astropy as apy
import re

__author__  = 'bellrise'
__version__ = '0.4'


def fetch(scope: apy.Scope, *params):
    """ Returns a list of parameters from the given parameter names
    in a tuple so you can easily unpack it. It also runs a type check
    for each parameter so it has to be a string. """

    collection = []
    for p in params:
        arg = scope.get(p)
        if not arg:
            scope.throw(apy.errors.undef_parameter, f"'{p}' is undefined")
        if arg.typeof() != 'str':
            scope.throw(apy.errors.type_error, f"'{p}' has to be of type String")
        collection.append(arg)

    return (i for i in collection)


def f_substr(scope: apy.Scope):
    # params: (string: str, __a: str, __b: str)
    # comment: Returns the substring of the passed string from
    # a to b inclusive.

    string, = fetch(scope, 'string')
    __a = scope.get('__a')
    __b = scope.get('__b')

    # Type check
    if __a.typeof() != 'num':
        scope.throw(apy.errors.type_error, f"__a has to be of type Num")
    if __b.typeof() != 'num':
        scope.throw(apy.errors.type_error, f"__b has to be of type Num")

    # Index check
    if __a < 0 or __b > len(string.get()):
        scope.throw(apy.errors.index_error, 'index out of bounds')

    r = [int(i.get()) for i in [__a, __b]]
    s = string.get()[r[0]:r[1]]
    scope.place(apy.models.String.new('string', s))

    return scope.format()


def f_split(scope: apy.Scope):
    # params: (string: str, sub: str)
    # comment: Splits the string at the found locations, returns
    # a copy of the string without any of the specified
    # substrings in them as they get removed from the whole
    # string. This may be useful for splitting emails for
    # example, as String.split(email, "@") will return a 2
    # element array with the username and the profile.

    string, sub = fetch(scope, 'string', 'sub')
    sa = string.get().split(sub.get())

    astro_array = []
    for s in sa:
        astro_array.append(apy.models.String.new('null', s))

    scope.place(apy.models.Array.new('__array', astro_array))

    return scope.format()


def f_regex(scope: apy.Scope):
    # params: (string: str)
    # comment: Returns an array of matches in the specified string.
    # You can later remove or read the matches comparing it
    # to the original string. When no matches are found, it
    # returns an empty list. (This may be changed to a null
    # value if it gets added or just False). This is based
    # on the python re module which uses the basic UNIX regex
    # format.

    string, re_ = fetch(scope, 'string', 're')

    array = re.findall(re_.get(), string.get())
    array = [apy.models.String.new('null', i) for i in array]

    scope.place(apy.models.Array.new('__array', array))
    return scope.format()


def f_lower(scope: apy.Scope):
    # params: (string: str)
    # comment: Converts the whole string to a lower case string.
    # Omits any non-alphabetical characters.

    string, = fetch(scope, 'string')
    scope.place(apy.models.String.new('string', string.get().lower()))
    return scope.format()


def f_upper(scope: apy.Scope):
    # params: (string: str)
    # comment: Converts the whole string to a upper case string.
    # Omits any non-alphabetical characters.

    string, = fetch(scope, 'string')
    scope.place(apy.models.String.new('string', string.get().upper()))
    return scope.format()


def f_length(scope: apy.Scope):
    # params: (string: str)
    # comment: Returns the total length of the string. Nothing
    # else. Simple as that.

    string, = fetch(scope, 'string')
    scope.place(apy.models.Num.new('_len', len(string.get())))
    return scope.format()


def f_find(scope: apy.Scope):
    # params: (string: str, sub: str)
    # comment: Returns the index of the first letter of the specified
    # substring in the string. This is of course done easily
    # in Python, but in any other implementation of Astro this
    # would be done by checking each substring of the string that
    # is the same length of the substring, and if the chars would
    # match the loop would return the current int index. Also, if
    # this does not find any matching substring in the string it
    # returns -1. Help: if you want to not care about the case of
    # the string, use String.lower(str) to change all your strings
    # and substrings to lower case so any case works.
    #
    # Currently this can be used in the "if sub in str" syntax
    # while that might be added(?) or if it won't, this is a good
    # and long-time solution to this problem. A short example:
    #
    # if String.find("abc", "a") != -1:
    #     -- Execute code if 'a' is found in 'abc'

    string, sub = fetch(scope, 'string', 'sub')
    scope.place(apy.models.Num.new('__i', string.get().find(sub.get())))
    return scope.format()


def f_replace(scope: apy.Scope):
    # params: (string: str, __a: str, __b: str)
    # comment: Replaces all the __a substrings with __b substrings as
    # specified in the arguments and returns a copy of the new
    # string. Just so you know, even on the Python level moving
    # strings around is quite an expensive operation.

    string, __a, __b = fetch(scope, 'string', '__a', '__b')
    s = string.get().replace(__a.get(), __b.get())
    scope.place(apy.models.Num.new('string', s))
    return scope.format()


def f_strip(scope: apy.Scope):
    # params: (string: str)
    # comment: Removes any whitespace characters on both ends of the strings,
    # returning only the core part. Note: this does not remove any
    # whitespace from inside the strings, only the outside.

    string, = fetch(scope, 'string')
    scope.place(apy.models.String.new('string', string.get().strip()))
    return scope.format()


def f_to_num(scope: apy.Scope):
    # params: (string: str)
    # comment: Casts the string to an astro number type. If the string contains
    # any invalid characters, it throws a TypeError. Maybe this will
    # be possible to catch, I'm not sure. If catching errors will not
    # be implemented before 1.0, i'll change this to return False rather
    # then stop the program throwing an error.

    string, = fetch(scope, 'string')
    s: str = string.get()

    if re.match(r'[^0-9.]+', s) or len(re.findall(r'\.+', s)) > 1:
        scope.throw(apy.errors.type_error, 'cannot cast string to Num type')

    f = float(s)
    scope.place(apy.models.Num.new('__num', f))
    return scope.format()


def f_to_bool(scope: apy.Scope):
    # params: (string: str)
    # comment: Converts any object to a boolean type. This function is pretty
    # big in comparison to the to_num function because a True or False
    # value can come in many shapes and forms, implementing other styles
    # of true/false formats and types. The default return value is True, returns
    # False otherwise. This is a handy list of all False values currently handled.
    #
    #  ""                   "no"
    #  []                   "No"
    #  False                "n"
    #  "False"              "N"
    #  "false"              "null"
    #  <= 0                 "nil"

    value = scope.get('value')
    ev = True

    if value.typeof() == 'bool':
        ev = value.get()

    elif value.typeof() == 'array':
        if len(value) == 0:
            ev = False

    elif value.typeof() == 'num':
        if value.get() <= 0:
            ev = False

    elif value.typeof() == 'str':
        if value.get().lower() in ['false', 'no', 'n', 'null', 'nil']:
            ev = False
        if not value.get(): ev = False

    scope.place(apy.models.Bool.new('__bool', ev))
    return scope.format()


def f_is_num(scope: apy.Scope):
    # params: (string: str)
    # comment: Returns True of the whole string can be turned into a number
    # type, that is all characters are numeric characters.

    string, = fetch(scope, 'string')
    scope.place(apy.models.Bool.new('__bool', string.get().isnumeric()))
    return scope.format()


def f_is_lower(scope: apy.Scope):
    # params: (string: str)
    # comment: Returns True if the passed string is all lower case. This only
    # counts ascii characters, excluding any numbers or special characters.

    string, = fetch(scope, 'string')
    scope.place(apy.models.Bool.new('__bool', string.get().islower()))
    return scope.format()


def f_is_upper(scope: apy.Scope):
    # params: (string: str)
    # comment: Returns True if the passed string is all upper case. This only
    # counts ascii characters, excluding any numbers or special characters.

    string, = fetch(scope, 'string')
    scope.place(apy.models.Bool.new('__bool', string.get().isupper()))
    return scope.format()


def __build__():
    """ build function for the Array module. """
    renders = {
        f_substr: 'substr',
        f_split: 'split',
        f_regex: 'regex',
        f_lower: 'lower',
        f_upper: 'upper',
        f_length: 'length',
        f_find: 'find',
        f_replace: 'replace',
        f_strip: 'strip',
        f_to_num: 'to_num',
        f_to_bool: 'to_bool',
        f_is_num: 'is_num',
        f_is_lower: 'is_lower',
        f_is_upper: 'is_upper'
    }

    return [apy.render(f, '__String', k) for f, k in renders.items()]
