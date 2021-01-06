# python >= 3.6
""" This is the astro parser (asp) toolkit, creatively named Astro Parser
Toolkit, (apt). Don't mix it up with the linux apt application though! As
the parser itself was getting quite long, above 700 lines, some functiona-
-lity has been moved here to make the code more readable and maintainable.
This is a universal toolkit version for all asp versions, as it's a fully
standalone program without any parsing mechanisms, so it can be imported
in any parser format or edition. As for the non-semantic version style, my
smaller programs all use the major-minor format, because it's much eaiser
maintaning that kind of style, not caring about the builds, releases or
minor fixes. The versioning here is simple - if the major version changes,
any existing versions are either deprecated or just not work with the new
additions.
"""

__author__  = 'bellrise'
__version__ = '0.1'


# This error is thrown when there is a problem with the parser itself,
# not the code that it's parsing. This is so you can easily differentiate
# between actual Python code errors and Astro errors being thrown. All
# intentional errors in the parser itself are a ParserError.
class ParserError(Exception):
    pass
