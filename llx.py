"""
llx - Life Longevity Xtra

This is a module containing several functions or classes that make
your life easier or just are nifty extensions to your current program.
For in-depth function or class explanation, check the docstrings
under the definition. The functions & classes are alphabetically
ordered.
All special-case data is set using the internal OP codes.
For example, if you pass a list to LoadingBar, and you want the list
to specify the length of the progress bar, you need to pass OP.LINK
as the first argument.
"""
import zoneinfo
import datetime
import random
import pickle
import uuid
import time

__author__  = 'bellrise'
__version__ = 0.8

# Global definitions
DEBUG = False


class OP:
    """ LLX Opcodes for passing special variables """
    START   = b'\x00'
    STOP    = b'\xFF'
    LINK    = b'L'
    NUMBERS = b'n'
    UUID    = b'u'


# Functions

def _debug(*msg):
    """ Prints a debug message if debug is set to True. """
    if DEBUG:
        msg = [str(i) for i in msg]
        print('[LLX:DEBUG]', ' '.join(msg))


def animated_bar(length: int = 10, step=1, char='█'):
    """ Creates an animated loading bar with the chosen parameters.
    The time between one frame and another is specified.
    :param length: Length of the loading bar
    :param step: How long should one step take (in seconds)
    :param char: The loading bar character """
    if len(char) > 1 or isinstance(char, str) is False:
        raise ArgumentError('\'char\' argument is invalid')
    bar = []
    ppi = 100 / length
    for _ in range(length):
        bar.append('-')
    for i in range(length):
        bar[i] = char
        percent = ppi * (i + 1)
        print('[' + ''.join(bar) + ']', f"{round(percent, 1)}%", end='\r')
        time.sleep(step)
    print()


def countdown(seconds: int, tab='\t\t\t'):
    """ Prints a countdown in one place only, uses 1 second from time
    to wait for the next step. Counts 0.
    :param seconds: Amount of seconds to count (+0)
    :param tab: For overwriting the longer numbers, keep it at
    least a tab. """
    _t = seconds
    left = _t % 60
    minutes = (_t - left) / 60

    while True:
        if seconds == 0:
            minutes -= 1
        if _t < 0:
            break
        seconds = _t % 60
        print(f"{int(minutes):02}:{seconds:02}", tab, end='\r')
        time.sleep(1)
        _t -= 1
    print()


def fetch(name, folder=None):
    """ Dynamically imports a module using the python __import__
    function. This was made because import_module from importlib
    has some problems with relative importing. This function is
    also much easier to use.
    :param name: This is the name of the module (or package).
    :param folder: This is the folder the module should be imported
    from. """
    if folder:
        return __import__(folder, globals(), locals(), [name])
    return __import__(name, globals(), locals())


def generate_list(amount: int, opcode: bytes = OP.UUID, *tops) -> list:
    """ Generates a list filled with the selected data.
    :param amount: Length of the generated list
    :param opcode: Type of the data generated, can be either
    OP.UUID (default) or OP.NUMBERS and then the top and bottom
    amount have to be chosen. """
    _t = []
    if opcode == OP.UUID:
        for _ in range(amount):
            _t.append(str(uuid.uuid4()))
        return _t
    if opcode == OP.NUMBERS:
        for _ in range(amount):
            try:
                _t.append(random.randint(tops[0], tops[1]))
            except IndexError:
                raise ArgumentError('Two integers have to be passed '
                                    'if the chosen opcode is OP.NUMBERS')
        return _t
    raise OpcodeError('Invalid opcode for data generation')


def get_today(timezone) -> datetime.datetime:
    """ Returns a datetime from the datetime module with the
    selected timezone from pytz.
    :param timezone: pytz timezone string. """
    return datetime.datetime.now(zoneinfo.ZoneInfo(timezone))


def hold(seconds: int = 0, countdown_=True):
    """ Holds the screen for a certain amount of seconds, or waits
    for a user input if 'seconds' is 0. After finishing, quits.
    :param seconds: Amount of seconds the screen is held
    :param countdown_: If True, prints the integrated countdown
    while closing. """
    if seconds == 0:
        input('\n\n\n[Press ENTER to exit]')
    else:
        if countdown_:
            print('\n\n\nExiting in...')
            countdown(seconds)
        else:
            time.sleep(seconds)
    quit()


def mix(info: bytes, key: int) -> bytes:
    """ Mixes the byte string to have make it unpickable using the key.
    :param info: The data that will be encrypted.
    :param key: Used for encrypting & decrypting the data. """
    if int(key) != key:
        raise ArgumentError('The key needs to be of type int')
    if key == 0:
        raise ArgumentError('The key cannot be 0')
    total: bytes = b''
    for i, c in enumerate(info):
        k = bytes(str(c * key), 'utf8')
        total += k + b'#'
    return total[:-1]


def pack(data: object, filename: str):
    """ Packs the object with the pickle module, and pushes the
    bytes into the selected file.
    :param data: The object being packed.
    :param filename: The name of the file the data should be
    saved to. """
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def pick_from(options):
    """ Returns a random item from the passed list.
    :param options: The valid data types for options are:
    list, tuple & set. """
    a = random.randint(0, len(options) - 1)
    return options[a]


def timer(func):
    """ The timer decorator. Times the called function and
    prints the result in milliseconds after execution. """
    def wrapper(*a, **kw):
        time_s = time.time()
        func(*a, **kw)
        time_e = round((time.time() - time_s) * 1000, 3)
        io.ok(f"'{func.__name__}' executed in: {time_e} ms")
    return wrapper


def unmix(info: bytes, key: int) -> bytes:
    """ Unmixes the byte string using the key.
    :param info: The byte string being demixed
    :param key: the key used. (must be int) """
    if int(key) != key:
        raise ArgumentError('The key needs to be of type int')
    if key == 0:
        raise ArgumentError('The key cannot be 0')
    info = info.split(b'#')
    info = [bytes([int(int(i) / key)]) for i in info]
    return b''.join(info)


def unpack(filename: str):
    """ Unpacks the pickled object from the selected file, and
    returns it.
    :param filename: Name of the file to unpack from. """
    with open(filename, 'rb') as f:
        data: object = pickle.load(f)
    return data


def void(*r):
    """ This function is used for voiding variables (basically
    doing nothing with them. Any amount of variables can be passed
    to this function. Returns a lambda function returning None.
    :param r: Anything. """
    str(r)
    return lambda: 'void'


# Classes

class ArgumentError(Exception):
    """ Internal error for incorrect or invalid arguments
    passed to any of these functions. """
    pass


class LoadingBar:
    def __init__(self, length=10, link=None, step=0.1, randomstep=0, char='█',
                 rdiv=1, title=False):
        """ You can either pass a integer or a iterable object to size.
        :param length: Size of the bar or the link to list opcode
        :param step: The time sleep amount (in seconds)
        :param randomstep: Randomization in the step time (in seconds)
        :param char: The loading bar character
        :param rdiv: The final random time will be divided by this (default 1)
        :param title: If text is printed after the bar """
        if length == OP.LINK:
            try:
                self.size = len(link)
                length = self.size
            except TypeError:
                raise ArgumentError('Cannot use OP.LINK if a list is not specified')

        if link is not None:
            # List linking
            try:
                _debug('linking @', length, 'bars for', len(link), 'items')
                self.link = self._link(length, link)
            except TypeError:
                raise ArgumentError("'link' must be an iterable")
        if link is None and length != OP.LINK:
            self.link = None

        self.size = length          # Size of the loading bar
        self.step_r = randomstep    # Step time deviation
        self.step_t = step          # Step time
        self.step_d = rdiv          # Random step time division
        self.char   = char          # Char
        self.pos    = 0             # Current position
        self.ppi    = 100 / length  # Percent per char
        self.bar    = []            # Visual bar
        self.reply  = title         # Bool if next() prints cur_point
        self._check_args()
        self._prepare_bar()

        # Variables for user usage
        self.progress  = None  # Calculated after every step (in percent)
        self.cur_point = None  # Calculated after every step (object in list)

    def _link(self, length, list_) -> dict:
        """ Links the list to a set of variables and returns the data """
        link = dict()
        link['step'] = round(length / len(list_), 2)
        link['steps'] = len(list_)
        link['list'] = ['empty'] + list_
        link['pos'] = 0

        max_of = 0
        for i in list_:
            if len(i) > max_of:
                max_of = len(i)
        link['max'] = max_of

        _debug('generated link; step:', link['step'], 'chars per item')
        return link

    def _prepare_bar(self):
        """ Fills the visual bar with empty spaces for later drawing """
        self.bar = ['-'] * self.size

    def _check_args(self):
        """ Validation checking for the args """
        if not isinstance(self.step_r, int):
            raise ArgumentError('randomstep has to be a int')
        if len(self.char) > 1:
            raise ArgumentError('char cannot be longer than 1 char')

    def _calculate_progress(self):
        """ Updates the progress """
        self.progress = self.pos * self.ppi
        try:
            self.cur_point = self.link['list'][self.link['pos']]
        except TypeError:
            pass

    def _render(self):
        """ Prints the line with a return at the end to overwrite the next one """
        per = 'Done!' if self.percent == '100.0%' else self.percent
        if self.reply and self.cur_point is not None:
            prefix = self.cur_point
        else:
            prefix = ''

        print(f"[{''.join(self.bar)}] {per} {prefix}",
              end=f"{''.join([' '] * self.link['max'])}\r")

    def _step(self):
        """ Change the bar completion by one (+1) """
        self.pos += 1
        self._calculate_progress()
        self.bar[self.pos - 1] = self.char
        self._render()
        rstep = random.randint(0, self.step_r)
        time.sleep(self.step_t + rstep / self.step_d)

    @property
    def percent(self) -> str:
        if self.progress is not None:
            return f"{round(self.progress, 1)}%"

    def auto(self):
        """ Automatically step to the end """
        if self.link:
            for _ in range(self.link['steps'] - 1):
                self.next()
            return
        for _ in range(self.size):
            self._step()

        print()

    def next(self):
        """ If list-linked, step by the amount of times needed to
        move to the next item """
        if self.link['pos'] >= len(self.link['list']):
            return

        if self.link is not None:
            points = self.link['step'] * self.link['pos']
            for _ in range(int(points) - self.pos):
                self._step()

            _debug('pos:', self.link['pos'], '@', self.link['list'][self.link['pos']])
            self.link['pos'] += 1

            if self.link['pos'] == self.link['steps'] - 1:
                self.auto()
                return
        else:
            self._step()


    @property
    def state(self) -> tuple:
        """ Returns a tuple containing the progress and current
        object point. Updated every step. """
        return self.progress, self.cur_point

    def range(self):
        """ Returns a range object for use in 'for' loops. """
        if self.link is None:
            return range(self.size)
        return range(self.link['steps'])


class OpcodeError(Exception):
    """ Internal error for signifying incorrect or invalid
    opcodes. """
    pass


class _io:
    """ General input/output class for simple colour controlling
    and input data type casting. All output methods call the _paint
    method which depending on the HALT_STREAM setting prints it out
    to stdout or pushes the data to the stream stack for the user
    to pick up from. This is a singleton classm, that's why this
    is signed as an internal class. Note: When redirecting the
    stream to the stream stack this class takes care of clearing
    it every 5 messages. """
    HALT_STREAM = False
    TIMESTAMP = False
    stream = []

    def __lshift__(self, other):
        """ Pushes the data object on the stream. The stack
        clearing mechanism is also integrated within this
        method. """
        if len(self.stream) < 5:
            self.stream.clear()
        self.stream.append(other)

    def _push(self, clr, dat_list):
        """ Outputs a coloured message with a timestamp before it.
        After the message it reverts to the default terminal colouring. """
        data = [str(i) for i in dat_list]
        timestamp = f"[{datetime.datetime.utcnow()}]" if self.TIMESTAMP else ''
        if not self.HALT_STREAM:
            print(f"{timestamp}{clr}{' '.join(data)} \u001b[0m")
        else:
            self << f"{timestamp}{clr}{' '.join(data)} \u001b[0m"

    def num(self, prefix='λ ') -> float:
        """ Returns a number from input. Returns 0 if the number is invalid."""
        i = input('\u001b[1;93m' + prefix + '\u001b[0m')
        try:
            return float(i)
        except ValueError:
            return 0

    @property
    def top(self):
        """ Returns the latest item from the stream stack. """
        return self.stream[-1]

    def log(self, *data):
        """ White text. """
        self._push('\u001b[1;97m', data)

    def err(self, *data):
        """ Red text. """
        self._push('\u001b[1;31m', data)

    def ok(self, *data):
        """ Green text. """
        self._push('\u001b[1;92m', data)

    def warn(self, *data):
        """ Yellow text. """
        self._push('\u001b[1;93m', data)

    def master(self, *data):
        """ Black text & white background. """
        self._push(' \u001b[48;5;15m\u001b[38;5;0m', data)

    def low_log(self, *data):
        """ Grey text (low importance). """
        self._push('\u001b[1;90m', data)

    def big_err(self, *data):
        """ Black text & red background. """
        self._push(' \u001b[48;5;9m\u001b[38;5;0m', data)


# Singleton creation
io = _io()  # Output object
