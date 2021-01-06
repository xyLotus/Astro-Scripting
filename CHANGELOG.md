Change Log: (See Interpreter)

* 0.0.1
    -- Memory Mangement Patch -- 
    - AMM | Variable Storage Implemented
    - AMM | Function Content Storage Implemented
    - AMM | Function Parameter Name Storage Implemented

* 0..2
    -- Memory Management Patch -- 
    - AMM | Parameter Name AND Value storage FINALLY FUCKING finished C: (thanks to bellrise)


* 0.0.3 Pre-Patch 
    -- Interpreter CLS Changes --
    - 2 New Interpret Method Parameters
    - 1st Parameter: in_function                        | For Interpreting Functions
    - 2nd Parameter: function_name                      | For Interpreting Functions <- Getting Mem [AMM]

* 0.0.3
    -- Memory Handling Patch -- 
    -- Statement Implementation -- 
    - Say Statement Added                               | Output
    - Wait Statement Added                              | Pausing Program
    - Say Statement Parameter Mem Grabbing Implemented  | In/Out-Function (See 0.3 Pre-Patch)
    - Wait Statement Parameter Mem Grabbing Implemented | In/Out-Function (See 0.3 Pre-Patch)
    - Say Statement Variable Mem Grabbing Implemented   | In/Out-Function (See 0.3 Pre-Patch)
    - Wait Statement Variable Mem Grabbing Implemented  | In/Out-Function (See 0.3 Pre-Patch)

* 0.0.4
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

* 0.0.6
    -- Argument Parsing -- 
    - Added argparsing with the argparse module
    - You are now able to execute files after setting up the ASX-Entrypoint
    - ^ (See wiki page -> Setup Astro! [Not finished yet])

* 0.0.7
    -- Variable Error Handling -- 
    - Added Variable Error Handling
    - ^ Corresponding error: UndefinedVariable / UndefinedParameter
    - The error_out function output changed for error specification
    - Added force quitting the program if an error occurs

* 0.0.8
    -- Function Error Handling --
    - Added Function Error Handling
    - ^ Error Added: UndefinedFunction

* 0.0.9
    -- Array / List Output --
    - Added multi value storing datatype output support
    - [^ Thus meaning changes to the "_exec_say" function]
    - Added correct String & Int output in list / array

* 0.1.0
    -- New CMD Argument added -- 
    - "--ignoreErrors" argument added
    -  ^ outputs errors but doesn't exit program
    - Note: Bugs could occur, it's easy to forget to catch an error
   
* 0.1.1
    -- Mixin Loading Added --
    - You can now load mixins | AMM 

* 0.1.2
    -- Statement Name Chaning --
    - Wait -> Pause
    - Say -> Out

* 0.1.3
    -- Import Interpreting --
    - Import AMM Implementation | AMM
    - Function saving (function_storage, function_variable_storage)
    - etc. (See interpret method @ Interpreter cls)

* 0.1.4
    -- Array Element Accessing --
    - You can now access elements in arrays by using ´array_name[index]´

* 0.1.5
    -- Call Statement Method Changes --
    - Different return type when statement parameter type is 'elm'
