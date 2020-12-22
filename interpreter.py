''' ASX Interpreting / Execution '''

''' Change Log:

* 0.1
    -- Memory Mangement Patch -- 
    - AMM | Variable Storage Implemented
    - AMM | Function Content Storage Implemented
    - AMM | Function Parameter Name Storage Implemented

'''

__author__ = 'Lotus'
__version__ = '0.1'

def error_out(error_message: str): 
    print(f' * [ERROR] | {error_message}')

try:
    import asp              # Astro Parser (short: ASP)
    import llx              # tool kit
    from time import sleep  # pausing the program
except ImportError as ImportErr:
    error_out(f'Critical Import Error -> {ImportError}')
    exit()


# AMM - Astro Memory Management
variable_storage = {}               # Variable Names & Values
function_storage = {}               # Function Content
function_parameter_val_storage = {}  # Parameter Names & Values
function_parameter_storage = {}     # Parameter Names | Sub-Storage

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

    def assign_parameter_mem(self, values, params, name): 
        args = {}
        for value, param in zip(values, params):
            args[param] = value             

        # func = {name: args}
        function_parameter_val_storage[name] = args


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
            # print(f'Current Statement: {statement}') ### TODO -> RE-ENABLE

            ### AMM | Variables ### 
            if statement['type'] == 'assignment': 
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
                    if in_function:
                        parameter_name = statement['params'][0][1]                                  # Access Specifier
                        try: 
                            output_msg = function_parameter_val_storage[function_name][parameter_name][1] # Trying to Get Corresponding Param Value
                        except KeyError: 
                            try: 
                                output_msg = variable_storage[parameter_name]                       # Trying to Get Corresponding Var Value
                            except KeyError: 
                                output_msg = statement['params'][0][1]                              # Trying to Get raw output
                        self._exec_say(out=output_msg)
                    else: 
                        output_msg = statement['params'][0][1]
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
                            src_path=r'C:\Users\Martin\Desktop\EVERYTHING\Python\Astro - Scripting\src\sample.asx'
                        )

# CLS Instance Method Initialization
Interpreter.interpret(source=Interpreter.content, in_function=False)
