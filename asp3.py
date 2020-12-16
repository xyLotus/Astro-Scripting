# python >= 3.6
""" This is the code parser for Astro Script Executable
(.asx) files. It is supposed to be used as a plug-in script,
not being executed as a standalone program. When using it as
a module, just use the parse function.
"""
import re

__author__  = 'bellrise'
__version__ = '3.0'

# This is the format version of the code object generated
# by the parser, each new format is most probably incompatible
# with the older one, as names get changed and data shifted
# around or added into other containers.
FORMAT = 3


class _Parser:
    # Internal class, do not use!

    omit = []

    def __init__(self, lines: list):
        """ Entrypoint for the parser. """
        self.code = [s.strip('\n') for s in lines]
        self.clean()
        self.tabsize = self.init_whitespace()
        self.count_whitespace()
        self.code = self.type(self.code)

    def hash_strings(self, line, num):
        """ Replaces all strings with hashes for commenting
        purposes. """
        matches = re.finditer('"[^"]+"', line)
        for match in matches:
            if match:
                substr = line[match.start():match.end()]
                line = line.replace(substr, '#' * len(substr))
        if '"' in line:
            raise SyntaxError(f'Incorrect string formatting @ line {num}')
        return line

    def clean(self):
        """ Replaces all the comment lines with a double dash """
        in_comment = False
        commented = []

        # Multi line comments
        for index, line in enumerate(self.code):
            if in_comment:
                # In comment
                commented.append(index)

            if re.match('^/--', line.strip()):
                # Start of comment
                in_comment = True
                commented.append(index)

            if re.match('--/$', line.strip()):
                # End of comment
                if in_comment:
                    in_comment = False
                    commented.append(index)

        for i in commented:
            self.code[i] = ''

        # Single line comments
        for index, line in enumerate(self.code):
            modified: str = self.hash_strings(line, index)
            comment = modified.find('--')
            if comment != -1:
                chars = list(line)
                del chars[comment:]
                self.code[index] = ''.join(chars)

    def init_whitespace(self):
        """ Check the first occuring whitespace and return
        the basic whitespace amount. """
        for line in self.code:
            match = re.match(r'^ *', line)
            if match.end() != 0:
                return len(line[0:match.end()])
        return 4

    def count_whitespace(self):
        """ Take each line and present the tab size in an int. This also
        places a line number in each line, to keep track of the lines. """
        for index, line in enumerate(self.code):
            match = re.match(r'^ *', line)
            if match.end() == 0:
                self.code[index] = (index+1, 0, line.strip())
            # Size checking
            if match.end() % self.tabsize != 0:
                raise IndentationError(f'Invalid tab size @ line {index}')

            self.code[index] = (index+1, int(match.end() / self.tabsize), line.strip())

    def type(self, lines):
        """ This is the main function for setting the types of the
        statements and parsing them into valid ASX Parsed code format.
        This is called recursively because of the multiple functions. """

        in_func = False
        func_indent = 0
        func = []
        collected = []

        # Functions
        for pos, line in enumerate(lines):
            indent = line[1]
            text = line[2]

            if not text:
                continue

            # Functions
            if re.match(r'^#[_A-z][_A-z0-9]*\(.*\):', text) and not in_func:
                in_func = True
                func_indent = indent
                func.append(line)
                continue

            # Inside of function
            if in_func and (indent > func_indent):
                self.omit.append(line[0])
                func.append(line)
                continue

            # Outside of function
            if in_func and (indent <= func_indent) and text:
                in_func = False
                func_indent = 0
                collected.append(func)
                func = []

        # Statements / function calls
        for pos, line in enumerate(lines):
            text = line[2]

            # Imports
            if re.match(r'import .*', text):
                lines[pos] = self.parse_import(line)
                continue

            # Function header
            if re.match(r'#[_A-z][_A-z0-9]*\(.*\):', text):
                lines[pos] = self.parse_header(line)
                continue

            # Assignment
            if re.match(r'^[_A-z][_A-z0-9]* *= *.*', text):
                lines[pos] = self.parse_assignment(line)
                continue

            # Base statement
            if re.match(r'^[_A-z][_A-z0-9]* .*', text):
                lines[pos] = self.parse_statement(line)
                continue

            # Function call
            if re.match(r'^[_A-z][_A-z0-9]*\(.*\)', text):
                lines[pos] = self.parse_call(line)

        # Recollection
        for function in collected:
            lines[function[0][0]-1] = self.sort_function(self.type(function))

        return lines

    def sort_function(self, lines):
        """ Sorts the functions """
        header = lines[0]
        t = header[2]
        t.update({'code': lines[1:]})
        return header[0], header[1], t


    def parse_args(self, line, num):
        """ Parses the text and returns a data collected argument
        list. """
        splits = []
        for i, c in enumerate(self.hash_strings(line, num)):
            if c == ',': splits.append(i)

        if splits:
            data = []
            cursor = 0
            for i in splits:
                data.append(self.variable(line[cursor:i]))
                cursor = i+1
            data.append(self.variable(line[cursor:]))

            for i, s in enumerate(data):
                try:
                    data[i] = (s[0], s[1].replace(',', ' ').strip('"'))
                except AttributeError:
                    data[i] = s

        else:
            data = [self.variable(line)]

        return data

    def parse_array(self, line, num):
        """ Parses the array """
        elements = self.parse_args(line[1:-1], num)
        return 'arr', elements

    def variable(self, data):
        """ Returns the proper version of the variable """
        try:
            data = float(data)
            data = ('num', data)
        except ValueError:
            if '"' not in data:
                data = ('var', data)
            else:
                data = ('str', data[1:-1])

        return data

    # ------------------------------------------
    # Statement types
    # ------------------------------------------

    def parse_call(self, line: tuple):
        """ Parses a function call. """
        index = line[0]
        indent = line[1]
        text = line[2]

        name = text.split('(')[0]
        params = self.parse_args(text.split('(')[1][:-1], index)

        return (
            index, indent,
            {'type': 'call', 'name': name, 'params': params}
        )

    def parse_header(self, line: tuple):
        """ Parses a function header. """
        index = line[0]
        indent = line[1]
        text = line[2]

        for c in ['#', ':', ')']:
            text = text.strip(c)
        name, params = text.split('(')
        a = re.finditer('[^A-z0-9_, ]', params)
        for find in a:
            if find:
                raise SyntaxError(f'Invalid function parameters @ line {index}')

        # Parameters
        params = [s.strip() for s in params.split(',')]

        return (
            index, indent,
            {'type': 'function', 'name': name, 'parameters': params}
        )

    def parse_import(self, line: tuple):
        """ Parses an import statement. """
        try:
            import_ = line[2].split()[1]
        except IndexError:
            raise SyntaxError(f'Import statement cannot be empty @ line {line[0]}')
        return (
            line[0],
            line[1],
            {'type': 'import', 'name': import_}
        )

    def parse_statement(self, line: tuple):
        """ Parses a regular base statement. """
        index = line[0]
        indent = line[1]
        text = line[2]

        if len(text.split()) > 1:
            ins, params = text.split(maxsplit=1)
            # Parameter parsing
            params = self.parse_args(params, index)
        else:
            ins, params = text, None

        return (
            index, indent,
            {'type': 'statement', 'name': ins, 'params': params}
        )

    def parse_assignment(self, line):
        """ Parses an assigment. """
        index = line[0]
        indent = line[1]
        text = line[2]

        var, data = (s.strip() for s in text.split('='))

        if re.match(r'\[.*,.*\]', data):
            data = self.parse_array(data, index)
        else:
            data = self.variable(data)

        return (
            index, indent,
            {'type': 'assignemnt', 'var': var, 'data': data}
        )

    # ------------------------------------------
    # Other
    # ------------------------------------------

    def shift(self, statement):
        """ Shifts the statement around to keep the asx format. """
        d = statement[2]
        d.update({'line': statement[0]})
        return d

    def collect(self, code):
        """ Recollects the whole thing and adds a line number to each
        statement. """
        new = []
        for line in code:
            if line[0] not in self.omit and line[2]:
                data = {'line': line[0]}
                data.update(line[2])
                new.append(data)

        for index, st in enumerate(new):
            if st['type'] == 'function':
                sts = []
                for i in st['code']:
                    sts.append(self.shift(i))

                new[index]['code'] = sts

        return new

    def get(self):
        """ Returns the code object from the class. """
        return self.collect(self.code)


def parse(lines: list):
    """ Parses the code and returns a JSON serializable data
    object which works as the code.
    :param lines: The lines of code, prefferably coming from
     f.readlines() """

    return _Parser(lines).get()
