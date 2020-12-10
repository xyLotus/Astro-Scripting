# python >= 3.9
""" This is the code parser for Astro Script Executable
(.asx) files. It is supposed to be used as a plug-in script,
not being executed as a standalone program. When using it as
a module, just use the parse function.

  * 0.2
    - changed the format to 2
    - added parse_data(), which parses the data on the right of
      an assignment type
    - changed the line comment from `//` to `--`

  * 0.3
    - minor bugfix, could not read a statement without params

"""
import llx
import re

__author__ = 'bellrise'
__version__ = 0.3

# This is the format version of the code object generated
# by the parser, each new format is most probably incompatible
# with the older one, as names get changed and data shifted
# around or added into other containers.
FORMAT = 2


class _Parser:
    # Internal class, do not use!

    def __init__(self, fp):
        # Entry point for the parser.
        self.lines = 0
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
            if item.strip().startswith('--'):
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

    def classify_type(self, string: str):
        # Returns a variable depending on the type defined in the
        # string, raises an parsing error if the formatting is
        # incorrect.
        # Test for string
        if string.count('"') != 2 and string.find('"') != -1:
            self.err(string, 0, 'Quotes placement is incorrect')
        if string.startswith('"') and string.endswith('"'):
            return 'str', string.strip('"')
        # Test for number
        try:
            return 'num', float(string)
        except ValueError:
            pass

        # Test for variable
        if re.match(r'[a-zA-Z_\d]', string):
            return 'var', string
        else:
            self.err(string, 0, 'Unknown data format')

    def parse_data(self, dat: str):
        # Parses the data struct, returns a different data
        # structure depending on the complexity of the
        # data given.
        dat = [self.classify_type(s.strip()) for s in dat.split(',') if s]
        return dat

    def parse_statement(self, st: str):
        # Statement parser, returns a code object
        if len(st.split()) > 1:
            ins, params = st.split(maxsplit=1)
        else:
            ins, params = st, ""

        # Function call
        if re.match(r'^.*\(.*\).*', st):
            func = self.parse_header(''.join([ins, params]), '')
            return {
                'type': 'call',
                'name': func[0],
                'args': self.parse_data(params)
            }

        # Assignment
        if re.match(r'^\w.*=.*', st):
            if params[0] == '=':
                p = params.strip('=').strip()
            else:
                self.err(st, 0, 'Cannot read assignment statement')
                p = ""

            return {
                'type': 'assignment',
                'variable': ins,
                'args': self.parse_data(p)
            }

        # Any other statement
        if not re.match(r'=', st):
            return {
                'type': 'statement',
                'instruction': ins,
                'args': self.parse_data(params)
            }

        self.err(st, 0, 'Invalid statement')

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

    def parse_header(self, head: str, prefix='#'):
        # Function header parser, returns a tuple
        header = head.replace(' ', '').replace(prefix, '').split('(')
        if len(header) < 2 or not self.find_all(head, '(', ')', prefix):
            self.err(head, 0, 'Invalid function format')
        params = header[1].replace(')', '').replace(':', '').split(',')

        return header[0], params

    def imports(self, code):
        # Finds all import statements and re-formats them
        for index, i in enumerate(code):
            if i['type'] == 'statement' and i['instruction'] == 'import':
                imports = []
                for p in i['args']:
                    if p[0] != 'var':
                        self.err('import', 0, 'Cannot import constant')
                    imports.append(p[1])
                i['modules'] = imports
                i['type'] = 'import'
                del i['args']
                del i['instruction']
                code[index] = i
        return code

    def args_access_element(self, st: dict):
        # Finds all access-element statements
        if 'args' in st:
            for index, arg in enumerate(st['args']):
                # Take only variables into consideration
                if arg[0] != 'var':
                    continue
                var: str = arg[1]
                if re.match(r'^.+\[\d+\]', var):
                    if var.count('[') != 1 or var.count(']') != 1:
                        self.err('Element access', 0, 'Incorrect amount of brackets')

                    # Parsing element access
                    name, num = var.split('[', maxsplit=1)
                    num = num.strip(']')
                    st['args'][index] = [
                        'access-element',
                        [name, num]
                    ]

        return st

    def recollect(self, code):
        # Recollects the parsed data, checks every type and replaces
        # it with another.
        # type->import
        code = self.imports(code)

        # params[n][0]->access-element
        for index, st in enumerate(code):
            code[index] = self.args_access_element(st)

        return code

    def collect(self):
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
        code = self.collect()
        return self.recollect(code)


def parse(fp):
    """ Starts the parsing process, returns a parsed code
    object. fp: The file pointer of an open file parameter.
    Example usage, this returns the code object:

    with open('sample.asx') as f:
        code = asp.parse(f)

    """
    return _Parser(fp).render()
