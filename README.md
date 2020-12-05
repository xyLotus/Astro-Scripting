# Astro-Scripting
Astro Scripting (short: ASX), is a simple scripting language interpreted in python.

# Satements:
- say "text" / say varialbe |-> takes one parameter (output) and outputs it, can output a manually given string or a variable. 

- wait seconds              |-> takes one parameter (seconds) waits / pauses the program for the given time. 

                            |                                   func-name  |  func-params
- #function_name():         |-> creation of a function, usage: #function_name(): <-(:) = end of func declaration
      #function_content     |->                                ^function-syntax(#)
      
--Comment / -- Comment      |-> creation of comment; Syntax : -- 

/-- Comment1                |-> "       
Comment2                    |-> Creation of multi-line comment; 
Comment3                    |-> Syntax : /-- --/ 
Comment4 --/                |-> "

string_variable = "string variable content"         |-> string variable declaration and definition
integer_variable = 7                                |-> integer variable decleration and definition
boolean_variable = True // boolean_variable = False |-> boolean variable decleration and definition
a_list = 1, 2, 3                                    |-> list variable declaration and definition
