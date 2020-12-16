# Astro scripting 0.3
![](https://img.shields.io/badge/Implementation-Python%203.9-important)
![](https://img.shields.io/badge/Version-0.3-%2333aa33)
![](https://img.shields.io/tokei/lines/github/xyLotus/Astro-Scripting?label=Total%20lines)

Astro Scripting (short: ASX), is a simple, interpreted scripting language implemented in Python.


## Syntax
#### Variables
Because Astro is an dynamic typed language, so you don't have to specify the types.
```
-- Normal variables
var = 12

-- Arrays
array = 1, 2, 3
```
#### Comments
```
-- Single line comments
/-- Multi
    line
    comments --/
```

#### Functions 
```
#function_name(param):
      say "something"
      return param
      

-- Function calling
function_name(12)
```


## Statements
* `say <data>` - outputs the passed data to stdout
* `wait <seconds>` - waits / pausees the program for the selected time


## Data types
* String `"a string"`
* Number `7.1`
* Boolean `True` / `False`
* Array `1, 2, "3"`
Note: arrays can be multi-type
