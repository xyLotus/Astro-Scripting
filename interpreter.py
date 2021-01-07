''' ASX Interpreting / Execution '''

__author__ = 'Lotus'
__version__ = '0.1.6'

try:
    # Core Imports
    import asp.asp3 as asp          # Parser import
    from time import sleep          # Pausing the program
    import sys                      # PATH
    import argparse                 # argument parsing
    from astropy.errors import *    # Error Handling
    import os
except ImportError as ImportErr:
    error_out(f'Critical Import Error -> {ImportErr}')


# --------------------------------------- 
# Argument parsing
# ---------------------------------------

parser = argparse.ArgumentParser() # Initializing the ArgumentParser

# Adding arguments
parser.add_argument('asx', help='Name of the file')
parser.add_argument('-o', '--ignoreErrors', action='store_true', help="Ignores Program Errors")

args = parser.parse_args()

script_name = args.asx
if args.ignoreErrors: 
    ignore_errors: bool = True
else: 
    ignore_errors: bool = False


# --------------------------------------- 
# Mixin importing & building
# ---------------------------------------

def load_mixins():
    # This is put into a function to keep variables
    # local so they don't trash the global scope. 
    
    # Loading the mixins
    files = os.listdir('mixins')
    m_modules = []
    for mixin in files:
        if mixin.startswith('__'):
            continue
        m_ = __import__(f'mixins.{mixin[:-3]}', globals(), locals(), [mixin[:-3]])
        m_modules.append(m_)

    # Building the mixins
    mixins = {}
    for m in m_modules:
        try:
            funcs = m.__build__()
            if not isinstance(funcs, list):
                raise ReferenceError('__build__ function must return a list of Mixin objects')
        except AttributeError:
            # __build__ function not found
            raise ReferenceError('__build__ function was not found in mixin')
        
        for func in funcs:
            mixins[func.name] = func
        
    return mixins

mixins = load_mixins()
mixin_names = [str(y) for x, y in enumerate(mixins)]

# Error Output Function
def error_out(error_message: str, ErrorType: str = 'ERROR'): 
    if not ignore_errors:
        print(f'[{ErrorType}] | {error_message}')
        exit()
    else: 
        print(f'[{ErrorType}] | {error_message}')

# AMM - Astro Memory Management
variable_storage = {}                   # Global Scope  |   Variable Names & Values         | Main Storage
function_variable_storage = {}          # Local Scope   |   Function Var Storage            | Main Storage ### TODO MERGE with function function_parameter_val_storage
function_storage = {}                   # Global-Local  |   Function Content                | Sub-Storage
function_parameter_storage = {}         # Global-Local  |   Parameter Names                 | Sub-Storage

def _get_parse(src_file: str):  # Getting Parsed Code (ASP Module)
    try: 
        with open(src_file, 'r') as file:
            code = asp.parse(file, assignment_kw='params')
            return code
    except FileNotFoundError as FNF: 
        error_out(FNF)
        


class Dev:
    def __init__(self): 
        self.debug_mode = False

    def debug(self, *msg): 
        if self.debug_mode: 
            for _ in msg: 
                print(msg, end=' ')
        
    def out_mem(self, mem_type: dict):
        print(f'Memory: {mem_type}')


dev = Dev()     # Dev Tool Instance Initialization

class Memory: 
    def __init__(self): 
        pass

    def count_parameters(self, function_name: str): # Parameter Inconsistency Fix
        pass

    def store_variable(self, variable: str, value): # AMM | Storing Variables in Var Storage
        variable_storage[variable] = value

    def store_function_content(self, function: str, content): # AMM | Storing Function Content in Func Storage
        function_storage[function] = content

    def store_function_parameter(self, function: str, parameters: list): # AMM | Storing Func Param Names in Func Param Storage
        function_parameter_storage[function] = parameters

    def store_func_variable(self, function_name: str, variable: str, value: str):   # AMM | Storing Func Vars in Func Var Storage  
        try:
            function_variable_storage[function_name].update({variable: value})
        except KeyError:
            function_variable_storage[function_name] = {variable: value}

    def assign_parameter_mem(self, values, params, name):   # AMM | Storing Func Param Vals in FuncParamVal Storage
        args = {}
        for value, param in zip(values, params):
            args[param] = value             

        function_variable_storage[name] = args


class Math:
    def __init__(self): 
        pass

    def prioritise(self):
        pass


class Interpreter:
    def __init__(self, memory, dev, src_path):
        self.dev = dev
        self.memory = memory
        self.content = _get_parse(src_path)
        
    def _exec_function(self, func_name: str):   # executes function | used @ interpret method
            self.interpret(source=function_storage[func_name], in_function=True, function_name=func_name)

    def call_out(self, out, type_str: str, statement: dict, variable_name: str):   # say statement execution function
        if type_str == 'array':
            out = out[1]
            print('[', end='')
            item_count = 0
            for item in out:
                if item[0] == 'str':
                    if item_count == len(out)-1:
                        print(f'"{item[1]}"', end='')
                    else:
                        print(f'"{item[1]}",', end=' ')
                else:
                    if item_count == len(out)-1:
                        print(f'{item[1]}', end='')
                    else:
                        print(f'{item[1]},', end=' ')
                    
                item_count += 1
            print(']')
        elif type_str == 'elm':
            try:
                print(out[1][statement['params'][0][1]['element']][1])
            except IndexError:
                error_out(f'Index given in variable "{variable_name}" is out of range', index_error)
        else:
            try:
                print(out[1])
            except TypeError:
                pass

    def _exec_wait(self, time): # wait statement execution function
        sleep(time)

    def assign_variable(self, statement: dict, inside_function: bool, func_name: str, elm_spec: bool = False): # Variable AMM Snippet used @ Interpret Method
        if inside_function:
            variable_name = statement["var"]
            print(variable_name, ' <- var name')
            if elm_spec:
                variable_spec = statement['params'][1]['var']
                _location = statement['params'][1]['element']
                try:
                    variable_value = function_variable_storage[func_name][variable_spec][1][_location]
                except Exception as e:
                    error_out(f'Variable "{variable_name}" is not defined', undef_var)
                    try:
                        variable_value = variable_storage[variable_spec][1][_location]
                    except Exception as ex:
                        error_out(f'Variable "{variable_name}" is not defined', undef_var)
            else:
                variable_value = statement['params']
            print(variable_value, ' <- var val')
            self.memory.store_func_variable(
                                            function_name=func_name,
                                            variable=variable_name,
                                            value=variable_value
                                           )
        else:
            variable_name = statement['var']

            if elm_spec:
                variable_spec = statement['params'][1]['var']
                _location = statement['params'][1]['element']
                try:
                    variable_value = variable_storage[variable_spec][1][_location]
                except Exception:
                    error_out(f'Variable "{variable_name}" is not defined', undef_var)
            else:
                variable_value = statement['params']
                            
            self.memory.store_variable(variable=variable_name, value=variable_value)

    def assign_function(self, statement: dict, func_name: str):
        function_name = statement['name']
        function_content = statement['code']
        self.memory.store_function_content(function=function_name, content=function_content)

        parameters = statement['parameters']
        self.memory.store_function_parameter(function=function_name, parameters=parameters)

    def call_function(self, statement: dict, function_name: str):
        function_name = statement['name']
        param_vals = statement['params']

        try: 
            self.memory.assign_parameter_mem(
                                         values=param_vals,
                                         params=function_parameter_storage[function_name],
                                         name=function_name
                                        )
        except KeyError: 
            error_out(f'Function "{function_name}" not defined', undef_function)
        try:
            self._exec_function(func_name=function_name)
        except KeyError: 
            pass

    def call_statement(self, statement: dict, inside_function: bool, func_name: str): # base statement execution
        parameter_type = statement['params'][0][0]  # Parameter Type Handle ('var', 'str', ...)
        parameter_name = statement['params'][0][1]  # Parameter Name Handle                          
        
        if parameter_type == 'elm':

            parameter_name = statement['params'][0][1]['var']
        
        if inside_function:
            if parameter_type == 'var' or parameter_type == 'elm':                                                 #-----------------INSIDE-FUNC-----------------
                try:                                                                    #-----------------INSIDE-FUNC----------------- 
                    val = function_variable_storage[func_name][parameter_name]      # Trying to get local scope func storage (2. prior)
                except KeyError:
                    try: 
                        val = variable_storage[parameter_name]                      # Trying to get global scope variable storage (3. prior)
                    except KeyError:
                        error_out(f'Variable "{parameter_name}" undefined', undef_var)
            else: 
                val = statement['params'][0]                                   # Trying to get non-AMM implemented parameter (Last prior)
        else:
            if parameter_type == 'var':                                                #----------------OUTSIDE-FUNC----------------
                try:                                                                    #----------------OUTSIDE-FUNC----------------
                    val = variable_storage[parameter_name]                              # Trying to get variable storage (First prior)
                except KeyError:
                    error_out(f'Variable "{parameter_name}" undefined', undef_var) 
            elif parameter_type == 'elm':
                try:
                    val = variable_storage[parameter_name]
                except KeyError:
                    error_out(f'Variable "{parameter_name} undefined', undef_var)
            else: 
                val = statement['params'][0]                                      # Trying to get non-AMM implemented parameter (Last prior)                                       
        
        try:
            if parameter_type == 'elm': 
                return ['elm', val[1], parameter_name]                  # Returning, Now, Handled Parameter
            else:
                return val                                                                
        except UnboundLocalError: 
            pass

    def check_import(self, statement: dict):
        import_name = statement['name']
        if f'{import_name}.asx' in os.listdir('lib'): 
            return 'STD' # Standard Lib 
        elif f'{import_name}.asx' in os.getcwd():
            return 'USER' # Custom Lib
        else:
            return 'INVALID' # Lib Not Found

    def call_import(self, lib_name: str, std_check: str):
        # Calling the import
        if std_check == 'STD':
            with open(f'lib\\{lib_name}.asx', 'r') as f:
                lib_content = _get_parse(f'lib\\{lib_name}.asx')
                print(lib_content)
            self.interpret(source=lib_content, in_function=False)

    def _exec_delete(self, variable: str): 
        pass

    def call_if(self, statement: dict):     ### TODO Finish If-Statement Checking Function, return True / False
        pass

    # Main Method - Uses a lot of function from above this line ^^^^
    def interpret(self, source, in_function: bool, function_name: str = ''): 
        # main interpreting loop
        for statement in source:
            # print('Statement: ', statement)
            ### AMM | Variable Storage ###
            if statement['type'] == 'assignment':
                try:
                    if statement['params'][0] == 'elm':
                        self.assign_variable(statement=statement, inside_function=in_function, func_name=function_name, elm_spec=True) # AMM | Storing Variables
                    else:
                        self.assign_variable(statement=statement, inside_function=in_function, func_name=function_name) # AMM | Storing Variables
                except KeyError as E:
                    print(E)
                except IndexError as E: 
                    print(E)

            ### AMM | Function Content & Parameter Name Storage ### 
            elif statement['type'] == 'function': 
                self.assign_function(statement=statement, func_name=function_name)  # AMM | Storing Function Params Names & Content

            ### AMM | Function Calling ###
            elif statement['type'] == 'call':
                self.call_function(statement=statement, function_name=function_name) # AMM | Calling Storage And Executing Function

            ### Statement Execution ###
            elif statement['type'] == 'statement':
                ### Say Statement ###
                if statement['name'] == 'out' or statement['name'] == 'say':
                    out = self.call_statement(statement=statement, inside_function=in_function, func_name=function_name)    # AMM | Param Handling
                    type_str = out[0]
                    try:
                        self.call_out(out=out, type_str=type_str, statement=statement, variable_name=out[2])     # Executing Statement with handled parameter/s
                    except IndexError: 
                        self.call_out(out=out, type_str=type_str, statement=statement, variable_name='')     # Executing Statement with handled parameter/s
                ### Wait Statement ###
                elif statement['name'] == 'pause':
                    sec = self.call_statement(statement=statement, inside_function=in_function, func_name=function_name)[1]    # AMM | Param Handling
                    self._exec_wait(time=sec)   # Executing Statement with handled parameter/s
                ### Delete Statement ###
                elif statement['name'] == 'delete':
                    var = self.call_statement(statement=statement, inside_function=in_function, func_name=function_name)[1]
                    self._exec_delete(variable=var)
            elif statement['type'] == 'import':
                in_mixin = self.check_import(statement=statement) # Checking if imported libary is in STD or User lib
                self.call_import(std_check=in_mixin, lib_name=statement['name'])
            elif statement['type'] == 'mixin': 
                mixin_name = statement['name']
                function_variable_storage[function_name] = mixins[mixin_name](function_variable_storage[function_name])


mem = Memory()  # Memory Instance Initialization
Interpreter = Interpreter(
                            dev=dev,                # Dev Tools 
                            memory=mem,             # AMM | Memory Handling
                            src_path=script_name    # _PATH_
                        )

math = Math()

Interpreter.interpret(source=Interpreter.content, in_function=False) # Main Interpreting Method
print('\n\n\nVariable Storage: ', variable_storage)
 
