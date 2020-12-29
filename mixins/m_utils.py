""" The python side implementation of the Utils module in astro.
"""
import astropy as apy
import hashlib
import random
import uuid

__author__  = 'bellrise'
__version__ = '0.1'


def _hash(scope, __hashing):
    """ Internal function for hashing, checks the type and hashes
    the string also placing it on the scope. """

    s = scope.get('string')

    # Type check
    if s.typeof() != 'str':
        scope.throw(apy.errors.type_error, "'string' has to be of type String")

    b = __hashing(bytes(s.get(), 'utf8'))
    scope.place(apy.models.String.new('injection', b.hexdigest()))
    return scope.format()


def f_random(scope: apy.Scope):
    # params: (__a: num, __b: num)
    # comment: Returns a pseudo-random number in the specified range.

    __a = scope.get('__a')
    __b = scope.get('__b')

    # Type checking
    if __a.typeof() != 'num':
        scope.throw(apy.errors.type_error, "'__a' has to be of type Num")
    if __b.typeof() != 'num':
        scope.throw(apy.errors.type_error, "'__b' has to be of type Num")

    picked = random.randint(__a.get(), __b.get())
    scope.place(apy.models.Num.new('injection', picked))
    return scope.format()


def f_md5(scope: apy.Scope):
    # params: (string: str)
    # comment: Returns a md5 hash from the specified string. Note: this
    # is not supposed to be used as a safe password hash because it
    # is easily crackable.

    return _hash(scope, hashlib.md5)


def f_sha512(scope: apy.Scope):
    # params: (string: str)
    # comment: Returns a sha512 hash from the specified string. This is the
    # Linux password hashing standard and can be safely used in
    # storing password shadows.

    return _hash(scope, hashlib.sha512)


def f_uuid(scope: apy.Scope):
    # params: ()
    # comment: Returns a random UUID for making unique element IDs.

    u = str(uuid.uuid4())
    scope.place(apy.models.String.new('injection', u))
    return scope.format()


def __build__():
    return [
        apy.render(f_random, '__Utils', 'random'),
        apy.render(f_md5, '__Utils', 'md5'),
        apy.render(f_sha512, '__Utils', 'sha512'),
        apy.render(f_uuid, '__Utils', 'uuid')
    ]
