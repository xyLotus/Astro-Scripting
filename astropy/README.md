# astropy

This is the AstroPy package for writing astro libraries in Python. The way this works, is you register your function with the 
correct parameters, process some data in it and then exit the function to continue running the astro script. On the astro script 
side, the only thing you need is a simple `@mixin lib_function` in order to execute the function with the current data in the scope.

This is mostly used in the standard library, when implementing something in pure astro is just not possible, so you need to 
add functionality one level lower, in Python. You can find information on how to write astro modules in Python here, along with
a couple of examples, and a simple project - writing a function that returns the current time.

## Python package

* `render(func, lib: str, name: str)` this is the only function you need to call yourself, the rest happens in the background.

* `errors` contains error types. Used in `scope.throw()`
  - `syntax_error`
  - `undef_var`
  - `undef_parameter`
  - `undef_function`
  - `type_error`

* `models` Variable objects for a layer of abstraction on the astro interepreter format.
  - `Variable` base variable object
  - `String` string type
  - `Num` number type
  - `Array` list type
  - `create()` automatic object creation from var format
  
  
## Creating your own module

The astro interpreter calls the mapped python functions when it hits a @mixin statement, so first you need to register the function
written in astro, and that what astropy is for. This is a step by step instruction how to write a Time module:

### Creating the module

In order for this to work, you need the Python function and the astro function as the wrapper for it. So, create 2 files:
one named `Time.asx` and the other `m_time.py`. Notice the naming convention, the python modules for astro scripts start with
a `m_` and are all lowercase. One you've created the files, open `Time.asx` and type:

```
/--
  This is the "library comment", telling users what this library does.

  @author   yourName
  @version  0.1
--/

/-- Function comment, tells you what this function does. --/
#time():
    current_time = ""
    @mixin Time#time
    return current_time
```

And that's the astro side done, the `time` function will return the current time in `h:m:s` format.
___
### Adding functions

After that, open `m_time.py` and import the astropy library (for your own convinience as apy). Also, import the datetime module
where we'll get our time from.
```py
import astropy as apy
import datetime
```
Create a new function with a scope parameter, called `f_nameOfAstroFunction`. In our example, it will be called `f_time`. The
scope object holds all local variables defined in the astro function, so we can access them or write to astro.
```py
def f_time(scope: apy.Scope):
    
    # Creating the time string
    time_str = datetime.datetime.now().strftime('%H:%M:%S')
```
Now if we want to pass the created back to astro, and set it to the `current_time` variable we will need to create a new astro 
String object. This is done like seen below. `astro_string` is now our astro String object with the name of `current_time` and the
value of the time_str we specified earlier.
```py
astro_string = apy.models.String.new('current_time', time_str)
```
Now we need to export the astro string back to the variable scope using `set_variable()`.
```py
scope.set_variable('current_time', astro_string)
```
The final element in our function is actually returning the scope back to the interpreter, so `return scope.format()` will do.
**Be sure to return this at the end of the function, or else your code will not run!**

___
### Building your module

You can add more functions if you want, but this will be do for now. To actually register the functions, you need to change the
function into a *Mixin* - but do not worry! This is very easy. At the end of your file, create the `__build__` function that 
the interpreter will call to map your function to the internal storage.

```py
def __build__():
    return [
        apy.render(f_time, lib='Time', name='time')
    ]
```

Thats it! Place your files in the correct folders and off you go coding in astro! The source code for this small project can be found 
**[here](https://github.com/xyLotus/Astro-Scripting/tree/main/examples/Time%20module)**.
