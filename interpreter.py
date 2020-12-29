''' ASX Interpreting / Execution '''

''' Change Log:

* 0.1
    -- Memory Mangement Patch -- 
    - AMM | Variable Storage Implemented
    - AMM | Function Content Storage Implemented
    - AMM | Function Parameter Name Storage Implemented

* 0.2
    -- Memory Management Patch -- 
    - AMM | Parameter Name AND Value storage FINALLY FUCKING finished C: (thanks to bellrise)


* 0.3 Pre-Patch 
    -- Interpreter CLS Changes --
    - 2 New Interpret Method Parameters
    - 1st Parameter: in_function                        | For Interpreting Functions
    - 2nd Parameter: function_name                      | For Interpreting Functions <- Getting Mem [AMM]

* 0.3
    -- Memory Handling Patch -- 
    -- Statement Implementation -- 
    - Say Statement Added                               | Output
    - Wait Statement Added                              | Pausing Program
    - Say Statement Parameter Mem Grabbing Implemented  | In/Out-Function (See 0.3 Pre-Patch)
    - Wait Statement Parameter Mem Grabbing Implemented | In/Out-Function (See 0.3 Pre-Patch)
    - Say Statement Variable Mem Grabbing Implemented   | In/Out-Function (See 0.3 Pre-Patch)
    - Wait Statement Variable Mem Grabbing Implemented  | In/Out-Function (See 0.3 Pre-Patch)

* 0.4
    -- Interpreter CLS Changes --
    -- Reformatting -- 
    - Reformatted Interpreter CLS
    - Code In "Interpret" Method Now Split Into Sub-Methods
    - Interpret Method -> Main Method
    - A Lot Of New Comments

* 0.5
    -- Memory Handling Patch --
    - AMM | "function parameter value storage" deleted
    - AMM | "function variable storage" merged with the "function parameter value storage"
    - AMM | You can now change parameter values inside of the given function

* 0.6
    -- Argument Parsing -- 
    - Added argparsing with the argparse module
    - You are now able to execute files after setting up the ASX-Entrypoint
    - ^ (See wiki page -> Setup Astro! [Not finished yet])

* 0.7
    -- Variable Error Handling -- 
    - Added Variable Error Handling
    - ^ Corresponding error: UndefinedVariable / UndefinedParameter
    - The error_out function output changed for error specification
    - Added force quitting the program if an error occurs

* 0.8
    -- Function Error Handling --
    - Added Function Error Handling
    - ^ Error Added: UndefinedFunction
'''

__author__ = 'Lotus'
__version__ = '0.7'


def error_out(error_message: str, ErrorType: str = 'ERROR'): 
    print(f'[{ErrorType}] | {error_message}')

try:
    import asp.asp3 as asp          # Parser import
    from time import sleep          # Pausing the program
    import sys                      # PATH
    import argparse                 # argument parsing
    from astropy.errors import *     # Error Handling
except ImportError as ImportErr:
    error_out(f'Critical Import Error -> {ImportErr}')
    exit()


# Argument parsing
parser = argparse.ArgumentParser() # Initializing the ArgumentParser

# Adding arguments
parser.add_argument('asx', help='Name of the file')
args = parser.parse_args()

script_name = args.asx


# AMM - Astro Memory Management
variable_storage = {}                   # Global Scope  |   Variable Names & Values         | Main Storage
function_variable_storage = {}          # Local Scope   |   Function Var Storage            | Main Storage ### TODO MERGE with function function_parameter_val_storage
function_storage = {}                   # Global-Local  |   Function Content                | Sub-Storage
function_parameter_storage = {}         # Global-Local  |   Parameter Names                 | Sub-Storage

def _get_parse(src_file: str):  # Getting Parsed Code (ASP Module)
    try: 
        with open(src_file, 'r') as file:
            code = asp.parse(file)
            return code
    except FileNotFoundError as FNF: 
        error_out(FNF)
        exit()


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

    def _exec_say(self, out):   # say statement execution function
        print(out[1])

    def _exec_wait(self, time): # wait statement execution function
        sleep(time)

    def assign_variable(self, statement, inside_function: bool, func_name: str): # Variable AMM Snippet used @ Interpret Method
        if inside_function:
            variable_name = statement["var"]
            variable_value = statement['data']
            self.memory.store_func_variable(
                                            function_name=func_name,
                                            variable=variable_name,
                                            value=variable_value
                                           )
        else:
            variable_name = statement['var']
            variable_value = statement['data']
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
            quit()
        self._exec_function(func_name=function_name)

    def call_statement(self, statement: dict, inside_function: bool, func_name: str): # base statement execution
        parameter_type = statement['params'][0][0]  # Parameter Type Handle ('var', 'str', ...)
        parameter_name = statement['params'][0][1]  # Parameter Name Handle                                                  #-----------------VARIABLE==TRUE------------------
        if inside_function:
            if parameter_type == 'var':                                                          #-----------------INSIDE-FUNC-----------------
                try:                                                                    #-----------------INSIDE-FUNC----------------- 
                    val = function_variable_storage[func_name][parameter_name]      # Trying to get local scope func storage (2. prior)
                except KeyError:
                    try: 
                        val = variable_storage[parameter_name]                      # Trying to get global scope variable storage (3. prior)
                    except KeyError:
                        error_out(f'Variable "{parameter_name}" undefined', undef_var)
                        quit()
            else: 
                val = statement['params'][0]                                   # Trying to get non-AMM implemented parameter (Last prior)
        else:
            if parameter_type == 'var':                                                                     #----------------OUTSIDE-FUNC----------------
                try:                                                                    #----------------OUTSIDE-FUNC----------------
                    val = variable_storage[parameter_name]                              # Trying to get variable storage (First prior)
                except KeyError:
                    error_out(f'Variable "{parameter_name}" undefined', undef_var) 
                    quit()
            else: 
                val = statement['params'][0]                                      # Trying to get non-AMM implemented parameter (Last prior)                                         # Trying to get non-AMM implemented parameter (Always prior)
        
        return val                                                              # Returning, Now, Handled Parameter

    def call_if(self, statement: dict):     ### TODO Finish If-Statement Checking Function, return True / False
        check_bool = False

    # Main Method - Uses a lot of function from above this line ^^^^
    def interpret(self, source, in_function: bool, function_name: str = ''): 
        # main interpreting loop
        for statement in source:
            # print('Statement: ', statement) ### TODO RE-ENABLE
            ### AMM | Variable Storage ###
            if statement['type'] == 'assignment':
                self.assign_variable(statement=statement, inside_function=in_function, func_name=function_name) # AMM | Storing Variables

            ### AMM | Function Content & Parameter Name Storage ### 
            elif statement['type'] == 'function': 
                self.assign_function(statement=statement, func_name=function_name)  # AMM | Storing Function Params Names & Content

            ### AMM | Function Calling ###
            elif statement['type'] == 'call':
                self.call_function(statement=statement, function_name=function_name) # AMM | Calling Storage And Executing Function

            ### Statement Execution ###
            elif statement['type'] == 'statement':
                ### Say Statement ###
                if statement['name'] == 'say':
                    out = self.call_statement(statement=statement, inside_function=in_function, func_name=function_name)    # AMM | Param Handling
                    self._exec_say(out=out)     # Executing Statement with handled parameter/s
                ### Wait Statement ###
                elif statement['name'] == 'pause':
                    sec = self.call_statement(statement=statement, inside_function=in_function, func_name=function_name)[1]    # AMM | Param Handling
                    self._exec_wait(time=sec)   # Executing Statement with handled parameter/s
            elif statement['type'] == 'if': 
                self.call_if(statement=statement)


mem = Memory()  # Memory Instance Initialization
Interpreter = Interpreter(
                            dev=dev,                                                                                # Dev-Tools 
                            memory=mem,                                                                             # AMM | Memory Handling
                            src_path=script_name                                                                    # _PATH_
                        )

Interpreter.interpret(source=Interpreter.content, in_function=False) # Main Interpreting Method
