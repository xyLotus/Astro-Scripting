''' ASX Interpreting / Execution '''

''' Change Log:

* 0.1
    -- Basic Statements -- 
    - added "say" statement interpreting
    - added "wait" statement interpreting 
* 0.2
    -- Memory Management --
    - added function storage
    - added variable storage

* 0.3
    -- Functions & Variables -- 
    - added function calling / initialization
    - added variable defining

'''

# Credits
__author__ = 'Lotus'
__version__ = 0.3

# Configurations
debug_mode = False

# Error Output function
def error_out(out):
    print(f'Error -> {out}')

# Import Checking
try:
    from time import sleep  # pausing program
    import asp              # main-parser
    import llx              # tool kit lib | 1 
    import whitespace       # tool kit lib | 2
    import json             # used for parsing return value
    import datetime
except ImportError as e: 
    error_out(e)
    exit()

# debugging function
def debug(out): 
    if debug_mode: 
        print(f' * [DEBUG] : {out}')

# debug wrapper
def debugger(function):
    def wrapper(*args):
        if debug_mode: 
            time = datetime.datetime.now()
            debug(f'{function.__name__} called @ [{time}] with arguments -> {args}')
        return function(*args)
    return wrapper

# debugger that ignores the debug_mode configuration
def prior_debugger(function): 
    def wrapper(*args): 
        time = datetime.datetime.now()
        print(f'{function.__name__} called @ [{time}] with arguments >> {whitespace.IO.elaborate(args)}')
        return function(args)
    return wrapper


# Global Variables
file_path = r'Astro - Scripting\src\sample.asx'
function_storage = {}
variable_storage = {}

# Astro Memory Management
def store_function(function_name, content):
    ''' stores function in astro memory '''  
    function_storage[function_name] = content

def store_variable(variable_name, value): 
    variable_storage[variable_name] = value

class AstroStatements: 
    ''' class containing all statements that are currently in ASX '''
    @debugger
    def asx_say(self, *args): 
        ''' base output statement '''
        argument_count = 0
        while argument_count != len(args):
            print(args[0][argument_count])
            argument_count += 1
        
    def asx_wait(self, time): 
        ''' pause program statement ''' 
        sleep(time[0])
        

# Interpreting Class working with parser module : asp
class Interpreter: 
    def __init__(self, astro_instance): 
        self.astro_instance = astro_instance

    @debugger
    def execute_code(self, cls, attr, *args): 
        ''' calls code statements ''' 
        getattr(cls, attr)(args)

    def get_code(self, sample, specification: str = ''): 
        ''' outputs code in parsed json format ''' 
        with open(sample, 'r') as file: 
            code = asp.parse(file)
            if specification == '':
                print(code)
            else: 
                print(f'{specification}:')
                print(code[0][specification])

    def out_functions(self, specification: str = ''): 
        ''' outputs function storage ''' 
        print(f'Function Storage: {function_storage}')

    def out_variables(self): 
        ''' outputs variable storage '''
        print(f'Variable Storage: {variable_storage}')

    def _get_function_statements(self, function):
        ''' returns the statements in the function specified in parameter: function '''
        print(f'[{function}] statements -> {function_storage[function]}')
        return function_storage[function]

    def _render_function(self, render_function): 
        ''' renders the function '''
        function_statements = self._get_function_statements(render_function)
        # Main-Interpreting
        for statement in function_statements:
            # Statement Interpreting
            if statement['type'] == 'statement':
                if statement['instruction'] == 'say': 
                    if statement['args'][0][0] == 'var': 
                        instruction = statement['instruction']
                        args = variable_storage[statement['args'][0][1]]
                        self.execute_code(self.astro_instance, f'asx_{instruction}', args)
                    else: 
                        instruction = statement['instruction']
                        args = statement['args'][0][1]
                        self.execute_code(self.astro_instance, f'asx_{instruction}', args)
                    
                elif statement['instruction'] == 'wait':
                    instruction = statement['instruction']
                    args = statement['args'][0][1]
                    self.execute_code(self.astro_instance, f'asx_{instruction}', args)

    def interpret_sample(self, sample):
        ''' this function interprets a given sample in parameter sample ''' 
        try: 
            with open(sample, 'r') as file: 
                sample_code = asp.parse(file)
        except FileNotFoundError as FNF: 
            error_out(FNF)
            exit()

        # Main-Interpreting
        for statement in sample_code:
            # Statement Interpreting
            if statement['type'] == 'statement':
                if statement['instruction'] == 'say': 
                    if statement['args'][0][0] == 'var': 
                        instruction = statement['instruction']
                        args = variable_storage[statement['args'][0][1]]
                        self.execute_code(self.astro_instance, f'asx_{instruction}', args)
                    else: 
                        instruction = statement['instruction']
                        args = statement['args'][0][1]
                        self.execute_code(self.astro_instance, f'asx_{instruction}', args)
                    
                elif statement['instruction'] == 'wait':
                    instruction = statement['instruction']
                    args = statement['args'][0][1]
                    self.execute_code(self.astro_instance, f'asx_{instruction}', args)

            # Function Interpreting
            if statement['type'] == 'function': 
                store_function(statement['name'], statement['statements'])
            
            if statement['type'] == 'call':
                self._render_function(statement['name']) 
            
            if statement['type'] == 'assignment': 
                variable_value = statement['args'][0][1]
                store_variable(statement['variable'], variable_value)
                    

# AstroStatement CLS Instance initialization 
Satements = AstroStatements()

# Interpreter CLS Instance initialization 
Interpreter = Interpreter(Satements)
Interpreter.get_code(file_path)
Interpreter.interpret_sample(file_path)
