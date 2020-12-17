''' ASX Interpreting / Execution '''

''' Change Log:

*0.1
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
    import asp 
    import llx
except ImportError as ImportErr: 
    error_out(f'Critical Import Error -> {ImportError}')
    exit()


# AMM - Astro Memory Management
variable_storage = {}
function_storage = {}
function_parameter_storage = {}


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


class Interpreter: 
    def __init__(self, memory, dev, src_path): 
        self.dev = dev
        self.memory = memory
        self.content = _get_parse(src_path)
        
    def interpret(self): 
        for statement in self.content: 
            # print(f'Current Statement: {statement}') ###TODO - RE-ENABLE
            
            ### AMM | Variables ### 
            if statement['type'] == 'assignment': 
                variable_name = statement['var']
                variable_value = statement['data'][1]
                self.memory.store_variable(variable=variable_name, value=variable_value)
                print('Variable_Storage: ', end='')
                self.dev.out_mem(variable_storage)
            ### AMM | Functions - Content - Parameter Names ### 
            elif statement['type'] == 'function': 
                ## Content ##
                function_name = statement['name']
                function_content = statement['code']
                self.memory.store_function_content(function=function_name, content=function_content)
                print('Function_Storage: ', end='')
                self.dev.out_mem(function_storage)

                ## Parameter Names ##
                parameters = statement['parameters']
                self.memory.store_function_parameter(function=function_name, parameters=parameters)
                print('Function_Parameter_Storage: ', end='')
                self.dev.out_mem(function_parameter_storage)
            ### AMM | Function Parameter Values ###
            


dev = Dev()
mem = Memory()

Interpreter = Interpreter(
                            dev=dev,
                            memory = mem,
                            src_path=r'sample.asx'
                         )

# CLS Instance Method Initialization
Interpreter.interpret()
