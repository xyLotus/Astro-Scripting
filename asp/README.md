# asp
*Documentation pulled from asp3.py*
___
This is the code parser for Astro Script Executable (.asx) files.
It is supposed to be used as a plug-in script, not being executed as
a standalone program. When using it as a module, just use the parse
function. This has no dependencies apart from the Python standard
library.

### asp3
  The third asx code format (`pax3`) will probably be supported
  for quite some time, as it is the main parser ASX is based on, as of
  December, 2020. The previous version called just asp, has been deprecated
  as it was very buggy and had a lot problems and missing functionality.
  asp3 will hopefully fix these problems by implementing a new way and
  format for the asx code, so using it also becomes easier. Quick note:
  the `__version__` of the parser is defined with 3 numbers: the first one
  represents the format, the second one shows the major version, and the
  third the minor version. If two implementations have the same format
  & major version, it is highly possible there should be no compatibilty
  issues.

### Versions
  This version will be supported as long as the interpreter will
  be using it, however parallel development of a new format can happen.
  This style of work has been chosen because creating a new, stable parser
  takes a lot of work and time, so in order to shorten the project development
  downtime to a minimum, an older version will be supported & bugfixed
  while a fresh and new version is being worked on. Every new version of
  asp will be thoroughly tested before deployment, even if the beta is
  alredy commited to the Github repository.

### How it works
  The main function of this whole parser would be the `parse()`
  function, taking in the lines of the script as a list of strings, and
  returning a JSON-serializable code object for the interpreter to read
  and execute. Intenally, the `parse()` function creates an instance of the
  `_Parser` class to call its `render()` method which returns the generated code
  object (which happens already in the `__init__` function. The constructor
  takes in the list of strings, cleaning them up, removing comments and
  calculating tabsizes. Note: a single tab can be any amount of spaces,
  but then it has to be kept the same for every single indent, or the
  parser will raise an IndentError which the interpreter can catch and
  read.


### Typing
  After cleaning, each line of code is passed to the `type()` method,
  which defines the type and class of the code, using regular expression
  patterns. After that, each type is sent out to a different method returning
  the parsed line. You can easily tell such a method as its name starts with
  the 'parse_' prefix.

### Sorting
  After typing, the lines are sorted and put into blocks depending
  on their indent size. All the different blocks can be found just scrolling
  down a bit and looking at the `BLOCKS` constant, containing a list of
  block statement types.

### Shifting
  After sorting, the lines and blocks are shifted to the final
  astro code compatible format from the parser-only internal format. The
  final result is the JSON-serializable code object represented as a list
  of statements (list of dicts).
   
# Parser options
You can now specify some options for the parser which you pass as keyword
arguments to the parse() method. Example:
```python
code = asp3.parse(lines, header_title='header')
```

Option          | Type | What is does
----------------|------|----------------------------------
`header_title`  | str  | Changes the header 'type' field.
`assignment_kw` | str  | The keyword used for the 'data' field in the assignment type.
