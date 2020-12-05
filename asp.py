""" This is the code parser for Astro Script Executable
(.asx) files. It is supposed to be used as a plug-in script,
not being executed as a standalone program. When using it as
a module, just use the parse function. """

import llx
import re

__author__ = 'bellrise'
__version__ = 0.1


class _Parser:
    # Internal class, do not use!

    def __init__(self, fp):
        # Entry point for the parser.
        self.code = self.clean(fp.readlines())

    def err(self, line, linenum, *info):
        # Prints an errors and quits the parser.
        llx.io.err('Parser error')
        print(f"at \u001b[1;96m{linenum}\u001b[0m: ", end='')
        llx.io.low_log(line.strip())
        print('why: ', end='')
        llx.io.warn(*info)
        raise RuntimeError('Cannot parse script')

    def clean(self, lines):
        # Removes all empty lines and comments from the code
        new = []
        in_comment = False
        for index, item in enumerate(lines):
            item: str
            if item.strip().startswith('//'):
                new.append(index)
            if in_comment:
                new.append(index)
            if not in_comment and item.strip().startswith('/--'):
                in_comment = True
                new.append(index)
            if in_comment and item.strip().endswith('--/'):
                in_comment = False

        code = []
        for i, line in enumerate(lines):
            if i not in new and line.strip() != '':
                code.append(line.rstrip())

        return code

    def find_all(self, string: str, *sub):
        # Finds all substrings in a string
        tests = []
        for i in sub:
            if string.find(i) != -1:
                tests.append(0)
        if len(tests) != len(sub):
            return False
        return True

    def startswith_any(self, string: str, *sub):
        # Checks if the string provided starts with any of the
        # given string samples.
        for i in sub:
            if string.startswith(i):
                return True
        return False

    def parse_statement(self, st: str):
        # Statement parser, returns a code object
        st = st.strip().split(' ', 1)
        try:
            params = st[1]
            if params.startswith('='):
                params = params.replace('=', '').strip()
                return {
                    'type': 'assignment',
                    'variable': st[0],
                    'data': params
                }

        except IndexError:
            params = ""
        return {
            'type': 'statement',
            'instruction': st[0],
            'params': params
        }

    def parse_collection(self, col: list):
        # Collection parser, returns a code object
        col[0] = self.parse_header(col[0])
        statements = [self.parse_statement(s) for s in col[1:]]
        return {
            'type': 'function',
            'name': col[0][0],
            'params': col[0][1],
            'statements': statements
        }

    def parse_header(self, head: str):
        # Function header parser, returns a tuple
        header = head.replace(' ', '').replace('#', '').split('(')
        if len(header) < 2 or not self.find_all(head, '(', ')', '#'):
            self.err(head, 0, 'Invalid function format')
        params = header[1].replace(')', '').replace(':', '').split(',')
        #       name      *params
        return header[0], params

    def statement_collector(self):
        # Returns an object of statements and functions
        code = self.code

        tab: int = -1
        # Finding indent size
        for i, line in enumerate(code):
            pat = re.compile(r'^[ \t]+')
            found = pat.search(line)
            if found is not None and tab == -1:
                tab = found.regs[0][1]
            if found is None:
                continue
            if tab != -1 and found.regs[0][1] != tab:
                self.err(line, i, 'Invalid tab size')

        # Finds the type of the statement
        i = 0
        new = []
        collection = []
        while i < len(self.code):
            # Normal statement
            line = self.code[i]
            if line.startswith('#'):
                collection.append(line)
            elif self.startswith_any(line, ' ', '\t'):
                collection.append(line)
            else:
                if collection:
                    new.append(self.parse_collection(collection))
                collection = []
                new.append(self.parse_statement(line))
            i += 1

        return [s for s in new if s]

    def render(self):
        # Returns the code object.
        return self.statement_collector()


def parse(fp):
    """ Starts the parsing process, returns a parsed code
    object. fp: The file pointer of an open file parameter.
    Example usage, this returns the code object:

    with open('sample.asx') as f:
        code = asp.parse(f)

    """
    return _Parser(fp).render()
