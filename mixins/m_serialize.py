""" The python side implementation of the Serialize module in astro.
"""
import astropy as apy
import os

__author__  = 'bellrise'
__version__ = '0.1'

# Global variable for holding the current filename for deserialization
# purposes. This works in combination of the fail() function which
# is responsible for throwing a RuntimeError with a "deserialization
# failed of file x: why" message.
file = ''


def fail(why):
    raise RuntimeError(f"Deserialization of '{file}' failed: {why}")

# Serialize special astro format opcodes grouped by types and
# instructions. These are for defining the types and element
# size in the bytes string. The instruction bytes have been made
# so specific to prepare for the map type model, which can have
# any astro type as the key and value (arrays too). In order
# to not change the whole format and make the previous versions
# incompatible, so this format is built in now. The raw string
# type is there as a placeholder for anything that could be a
# raw data type (bytes-style).
#
# There is always one BLOB byte (\x82) currently to signify
# one piece of data being stored. This is pretty much redundant
# and just takes up valuable space for now, but it may come in
# handy if a model system will ever be implemented. If that
# happens, the format will still be the same without the need
# to re-serialize all old data to keep the newest standard.
#
# If you looked closer into the serialization process, you could
# also see that the name of the object is being saved while it
# will always be "object" in this case, because the variable
# name is also always object. This is, also, because of the stable
# format version


FORMAT   = b'001'   # format version

# Types

ARRAY_T  = b'a'     # array type
BOOL_T   = b'b'     # boolean type
MAP_T    = b'm'     # map type
NUM_T    = b'n'     # number type
RSTR_T   = b'r'     # -
STRING_T = b's'     # string type

# Instructions

START    = b'\x80'  # start byte
NULL     = b'\x81'  # null byte
BLOB     = b'\x82'  # start of blob byte
NAME     = b'\x83'  # start of var name byte
DATA     = b'\x84'  # start of data byte
ELEMENT  = b'\x85'  # start of element byte
KEY      = b'\x86'  # start of key byte
VALUE    = b'\x87'  # start of value byte
STOP     = b'\x8F'  # ending byte

# Models

# If classes / objects / models will ever be implemented this
# is the place where the model bytes will be placed for complex
# serialization rules in order to achieve a high level of data
# safety (so it doesn't get corrupted).


def serialize_blob(data: apy.objects.var_t, __n=None, __t=DATA):
    """ Serializes one single object. Note: this does not place
    a BLOB byte at the beggining, this is handled by the parent
    function, serialize().
    :param data: the data you want to serialize
    :param __n: name of the variable, places an ELEMENT byte if
                not specified.
    :param __t: type of the data structure, this is placed after
                the name or the ELEMENT byte. The default is just
                DATA, can be KEY or VALUE. """

    # The bytes stack
    stack = b''
    if __n:
        stack += NAME + bytes(data.nameof(), 'utf8')
    else:
        stack += ELEMENT
    stack += __t

    if data.typeof() == 'str':
        # String type serialization, simple blob object
        stack += STRING_T
        stack += bytes(data.get(), 'utf8')

    if data.typeof() == 'num':
        # Number type serialization
        stack += NUM_T
        stack += bytes(str(data.get()), 'utf8')

    if data.typeof() == 'bool':
        # Boolean type serialization, false is 0 true is 1
        stack += BOOL_T
        if data.get(): stack += bytes(b'1')
        else: stack += bytes(b'0')

    return stack


def deserialize_blob(data: bytes):
    """ Returns a deserialized blob object in astropy model form. """

    if not isb(data[0], DATA):
        fail('unsupported operation for blob decoding')

    type_ = bytes([data[1]])
    data  = data[2:]

    if type_ == NUM_T:
        # Number type
        blob = apy.models.Num.new('null', float(data))

    elif type_ == STRING_T:
        # String type
        blob = apy.models.String.new('null', str(data, 'utf8'))

    elif type_ == BOOL_T:
        # Boolean type
        evaluation = True
        if data == b'0':
            evaluation = False
        blob = apy.models.Bool.new('null', evaluation)

    else:
        fail('unknown type')
        return None

    return blob


def serialize(data: apy.objects.var_t):
    """ Serializes the data into a bytes string. Controlls the whole
    serialization process, places the START/STOP and BLOB bytes. """

    # The bytes stack
    stack = START + FORMAT

    if data.typeof() == 'array':
        # Array model serialization
        stack += BLOB + ARRAY_T
        for i in data.get():
            stack += serialize_blob(apy.models.create('null', i))

    elif data.typeof() == 'map':
        # Map model serialization
        # TODO: Later implementation
        raise NotImplementedError('map serialization is not implemented')

    else:
        stack += BLOB + serialize_blob(data, __n=data.nameof())

    stack += STOP
    return stack


def isb(byte: int, other):
    """ Compares 2 bytes to eachother while the first one is an int,
    and the other just a byte string. This is just a shorthand. """
    return bytes([byte]) == other


def deserialize(data):
    """ Turns the data back into an astropy model. """

    # Start and stop check
    if not isb(data[0], START):
        fail('missing start byte')
    if not isb(data[-1], STOP):
        fail('missing ending byte')

    # Format check
    form = data[1:4]
    if form != FORMAT:
        fail('unreadable format')

    # Split by blob
    data = data[1:-1]
    blob = data.split(BLOB)[1:][0]

    if isb(blob[0], ARRAY_T):
        elements = blob.split(ELEMENT)[1:]
        blobs = []
        for e in elements:
            blobs.append(deserialize_blob(e))
        obj = apy.models.Array.new('null', blobs)

    elif isb(blob[0], MAP_T):
        # Map model serialization
        # TODO: Later implementation
        raise NotImplementedError('map serialization is not implemented')

    else:
        blob = DATA + blob.split(DATA)[1]
        obj = deserialize_blob(blob)

    return obj


def f_serialize(scope: apy.Scope):
    # params: (object: any, filename: str)
    # comment: Serialize the object into a special format used in only
    # this library and write it to a file.

    obj = scope.get('object')
    filename = scope.get('filename')

    # type checking
    if filename.typeof() != 'str':
        scope.throw(apy.errors.type_error, "'filename' has to be of type String")

    data: bytes = serialize(obj)
    try:
        with open(os.getcwd() + '/' + filename.get(), 'wb') as f:
            f.write(data)
    except Exception as e:
        scope.throw(apy.errors.file_error, e)

    return scope.format()


def f_deserialize(scope: apy.Scope):
    # params: (filename: str)
    # Deserialize the bytes from the given filename and return
    # them in an Astro format.

    filename = scope.get('filename')

    # type checking
    if filename.typeof() != 'str':
        scope.throw(apy.errors.type_error, "'filename' has to be of type String")

    try:
        with open(os.getcwd() + '/' + filename.get(), 'rb') as f:
            data = f.read()
    except Exception as e:
        scope.throw(apy.errors.file_error, e)

    global file
    file = filename.get()
    obj = deserialize(data)
    scope.set('object', obj)
    return scope.format()


def __build__():
    """ Library constructor. """
    return [
        apy.render(f_serialize, '__Serialize', 'serialize'),
        apy.render(f_deserialize, '__Serialize', 'deserialize')
    ]
