# The Astro Scripting Language
![Implementation](https://img.shields.io/badge/Implementation-Python%203.9-%2300A3E0?logo=python)
![Version](https://img.shields.io/badge/Version-0.4-%2333aa33?logo=gitea)
![Lines](https://img.shields.io/tokei/lines/github/xyLotus/astro?label=Total%20lines&logo=stackoverflow)
![Issues](https://img.shields.io/github/issues/xyLotus/astro?label=Issues)

Astro Scripting (short: ASX), is a simple, interpreted scripting language implemented in Python.


## Syntax
### Variables
Because Astro is an dynamic typed language, you don't have to specify the types.
```
var = 12
x = 12 * var
```
### Comments
```
-- Single line comments
/-- Multi
    line
    comments --/
```

### Functions 
```
#function_name(param):
      say "something"
      return param
      

-- Function calling
function_name(12)
```

### Arrays
This will print `2`, as elements in the array are counted from 0.
```
array = [1, 2, "a string"]
say array[1]

```

### Conditions
```
if 1 == 2:
    say "Something is wrong here!"
elif 1 >= 3:
    say "This is even worse"
else:
    say "Math works!"
```


## Statements
* `say <data>` - outputs the passed data to stdout
* `wait <seconds>` - waits / pausees the program for the selected time


## Data types
* String `"a string"`
* Number `7.1`
* Boolean `True` / `False`
* Array `[1, 2, "3"]`
Note: arrays can be multi-type
