""" The python side implementation of the Array module in astro.
"""
import astropy as apy

__author__  = 'bellrise'
__version__ = '0.3'


def buf_check(scope, buf, name='buf'):
    """ Throws an error if the buffer var is not an array. """
    if not buf:
        scope.throw(apy.errors.undef_parameter, f"'{name}' is not defined")

    if buf.typeof() != 'array':
        scope.throw(apy.errors.type_error,
                    f"'{name}' parameter has to be of type Array")


def reformat(buf):
    """ Reformats the array and turns it into astro types. """
    for i, v in enumerate(buf):
        buf[i] = apy.models.create('null', v)
    return buf


def f_len(scope: apy.Scope):
    # params: (buf: array)
    # comment: Returns the length of an array

    # Get the buffer
    buf: apy.models.Array = scope.get('buf')
    buf_check(scope, buf)

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
    buf_check(scope, buf)
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


def f_sum(scope: apy.Scope):
    # params: (buf: array)
    # comment: Returns the sum of all numbers in the array. It also works
    # for strings, as their length is calculated. If any other
    # type is found in the array, it is discarded and not counted
    # in to the total size.

    buf = scope.get('buf')
    buf_check(scope, buf)

    total = 0
    for i in range(len(buf)):
        e = buf[i]
        if e[0] == 'str':
            total += len(e[1])
        if e[0] == 'num':
            total += e[1]

    scope.place(apy.models.Num.new('injection', total))
    return scope.format()


def f_average(scope: apy.Scope):
    # params: (buf: array)
    # comment: Returns the average for all numbers in the array, if a string
    # is found the length of the string is taken into consideration.

    buf = scope.get('buf')
    buf_check(scope, buf)

    total, amount = 0, 0
    for i in range(len(buf)):
        e = buf[i]
        if e[0] == 'str':
            total += len(e[1])
            amount += 1
        if e[0] == 'num':
            total += e[1]
            amount += 1

    scope.place(apy.models.Num.new('injection', total / amount))
    return scope.format()


def f_contains(scope: apy.Scope):
    # params: (buf: array, item: any)
    # comment: Returns True if the item is found in the array, returns False
    # if not.

    buf: apy.models.Array = scope.get('buf')
    item = scope.get('item')
    buf_check(scope, buf)

    found = False
    for i in range(len(buf)):
        if buf[i] == item.raw():
            found = True
            break

    scope.place(apy.models.Bool('injection', found))
    return scope.format()


def f_find(scope: apy.Scope):
    # params: (buf: array, item: any)
    # comment: Returns the index of the first found item, returns -1 if no
    # such item is found.

    buf: apy.models.Array = scope.get('buf')
    item = scope.get('item')
    buf_check(scope, buf)

    index = -1
    for i in range(len(buf)):
        if buf[i] == item.raw():
            index = i
            break

    scope.place(apy.models.Num('injection', index))
    return scope.format()


def f_sort(scope: apy.Scope):
    # params: (buf: array)
    # comment: Sorts the array in a particular way. Numbers come first and then
    # strings. Each group of numbers and strings are sorted from smallest
    # to largest and alphabetically.

    buf: apy.models.Array = scope.get('buf')
    buf_check(scope, buf)

    nums = []
    strings = []
    other = []

    for i in range(len(buf)):
        e = buf[i]
        if e[0] == 'str':
            strings.append(e[1])
        elif e[0] == 'num':
            nums.append(e[1])
        else:
            other.append(e)

    nums.sort()
    strings.sort()

    total = []
    for i in nums:
        total.append(apy.models.Num.new('null', i))
    for i in strings:
        total.append(apy.models.String.new('null', i))
    for i in other:
        total.append(apy.models.create('null', i))

    scope.place(apy.models.Array.new('injection', total))
    return scope.format()


def f_reverse(scope: apy.Scope):
    # params: (buf: array)
    # comment: Reverses the whole array around.

    buf = scope.get('buf')
    buf_check(scope, buf)

    temp = buf.get()
    temp.reverse()
    temp = reformat(temp)

    scope.place(apy.models.Array.new('injection', temp))
    return scope.format()


def f_put(scope: apy.Scope):
    # params: (buf: array, item: any)
    # comment: Appends an item to the array. It it always put on the last place
    # without exceptions.

    buf = scope.get('buf')
    item = scope.get('item')
    buf_check(scope, buf)

    t = buf.get()
    t = reformat(t)
    t.append(item)
    scope.place(apy.models.Array.new('injection', t))
    return scope.format()


def f_pop(scope: apy.Scope):
    # params: (buf: array, index: any)
    # comment: Removes an item from the array at the specified index, this results
    # in shortening the array length by 1 and moving the items around so
    # there aren't any spaces left. This is using a simple Python list in
    # the background, so it happens automatically. This may not be the fastest,
    # but that's not the point of this language.

    buf = scope.get('buf')
    index = scope.get('index')
    if index.get() > len(buf.get()):
        scope.throw(apy.errors.index_error, 'index out of range')

    t = buf.get()
    t.pop(index.get())
    t = reformat(t)

    scope.place(apy.models.Array.new('injection', t))
    return scope.format()


def f_append(scope: apy.Scope):
    # params: (buf: array, other: array)
    # comment: Joins two array together creating one single array. Note: do not
    # mix this up with the Pythonic .append(), which adds a single item
    # to the array. This is done by the put() function.

    buf = scope.get('buf')
    other = scope.get('other')
    buf_check(scope, buf)
    buf_check(scope, other, 'other')

    t = buf.get()
    t.extend(other.get())
    t = reformat(t)

    scope.place(apy.models.Array.new('injection', t))
    return scope.format()


def __build__():
    """ build function for the Array module. """
    renders = {
        f_len: 'len',
        f_join: 'join',
        f_sum: 'sum',
        f_average: 'average',
        f_contains: 'contains',
        f_find: 'find',
        f_sort: 'sort',
        f_reverse: 'reverse',
        f_put: 'put',
        f_pop: 'pop',
        f_append: 'append'
    }

    return [apy.render(f, '__Array', k) for f, k in renders.items()]
