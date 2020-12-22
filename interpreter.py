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
    - 1st Parameter: in_function                        | for interpreting functions
    - 2nd Parameter: function_name                      | for interpreting functions <- and getting MEM [AMM]

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
    -- CMD / Powershell ArgHandling --
    - Argument Parsing Implemented 

'''

__author__ = 'Lotus'
__version__ = '0.4'

def error_out(error_message: str): 
    print(f' * [ERROR] | {error_message}')

try:
    import asp.asp3 as asp  # Parser import
    from time import sleep          # Pausing the program
    import sys                      # PATH
except ImportError as ImportErr:
    error_out(f'Critical Import Error -> {ImportErr}')
    exit()


# AMM - Astro Memory Management
variable_storage = {}                   # Variable Names & Values
function_variable_storage = {}
function_storage = {}                   # Function Content
function_parameter_val_storage = {}     # Parameter Names & Values
function_parameter_storage = {}         # Parameter Names | Sub-Storage

def _get_parse(src_file: str):
    try: 
        with open(src_file, 'r') as file: 
            code = asp.parse(file)
            return code
    except FileNotFoundError as FNF: 
        error_out(FNF)
        exit()


class Dev:
    def specify_parse(self, parse_content, specification: int, optional_specification: str):
        try: 
            if optional_specification == '':
                parse_content[specification]
            else: 
                parse_content[specification][optional_specification]
        except Exception as Ex:
            error_out(Ex)

    def out_mem(self, mem_type: dict):
        print(f'Memory: {mem_type}')


class Memory: 
    def __init__(self): 
        pass

    def store_variable(self, variable: str, value): 
        variable_storage[variable] = value

    def store_function_content(self, function: str, content):
        function_storage[function] = content

    def store_function_parameter(self, function: str, parameters: list):
        function_parameter_storage[function] = parameters

    def store_func_variable(self, function_name: str, variable: str, value: str): 
        try:
            function_variable_storage[function_name].update({variable: value})
        except KeyError:
            function_variable_storage[function_name] = {variable: value}

    def assign_parameter_mem(self, values, params, name): 
        args = {}
        for value, param in zip(values, params):
            args[param] = value             

        function_parameter_val_storage[name] = args


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
        print(out)

    def _exec_wait(self, time): # wait statement execution function
        sleep(time)

    def interpret(self, source, in_function: bool, function_name: str = ''): 
        for statement in source:
            ### AMM | Variables ### 
            if statement['type'] == 'assignment': 
                if in_function:
                    variable_name = statement["var"]
                    variable_value = statement['data'][1]
                    self.memory.store_func_variable(
                                                    function_name=function_name, 
                                                    variable=variable_name, 
                                                    value=variable_value
                                                    )
                else: 
                    variable_name = statement['var']
                    variable_value = statement['data'][1]
                    self.memory.store_variable(variable=variable_name, value=variable_value)
            ### AMM | Functions - Content - Parameter Names ### 
            elif statement['type'] == 'function': 
                ## Content ##
                function_name = statement['name']
                function_content = statement['code']
                self.memory.store_function_content(function=function_name, content=function_content)

                ## Parameter Names ##
                parameters = statement['parameters']
                self.memory.store_function_parameter(function=function_name, parameters=parameters)
            ### AMM | Function Parameter Values ###
            elif statement['type'] == 'call': 
                function_name = statement['name']
                param_vals = statement['params'] 
                self.memory.assign_parameter_mem(
                                                 values=param_vals,
                                                 params=function_parameter_storage[function_name],
                                                 name=function_name
                                                )
                self._exec_function(func_name=function_name)
            ### Statement Execution ###
            elif statement['type'] == 'statement': 
                if statement['name'] == 'say':
                    parameter_type = statement['params'][0][0]
                    parameter_name = statement['params'][0][1]                                      
                    if parameter_type == 'var': 
                        if in_function:                                      
                            try: 
                                output_msg = function_parameter_val_storage[function_name][parameter_name][1] 
                            except KeyError: 
                                try: 
                                    output_msg = function_variable_storage[function_name][parameter_name]
                                except KeyError:
                                    try: 
                                        output_msg = variable_storage[parameter_name]
                                    except KeyError:
                                        output_msg = statement['params'][0][1]
                        else: 
                            try: 
                                output_msg = variable_storage[parameter_name]
                            except KeyError: 
                                output_msg = parameter_name
                else: 
                    output_msg = parameter_name
                self._exec_say(out=output_msg)
                if statement['name'] == 'wait': 
                    if in_function: 
                        parameter_name = statement['params'][0][1]                                  # Access Specifier
                        try: 
                            sec = function_parameter_val_storage[function_name][parameter_name][1]  # Trying to Get Corresponding Param Value
                        except KeyError:
                            try: 
                                sec = variable_storage[parameter_name]                              # Trying to Get Corresponding Var Value
                            except KeyError: 
                                sec = statement['params'][0][1]                                     # Trying to Get raw output
                    self._exec_wait(time=sec)
                    

dev = Dev()
mem = Memory()
Interpreter = Interpreter(
                            dev=dev,
                            memory=mem,
                            src_path='_PATH_' ### Will be updated to an automatic version in the future
                        )

# CLS Instance Method Initialization
Interpreter.interpret(source=Interpreter.content, in_function=False)
print(function_variable_storage)
