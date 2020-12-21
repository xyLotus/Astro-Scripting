/**
 * This is the controller for the program. It contains an argument
 * parser, it works as an entrypoint for the whole program, executing
 * functions from this point depending on the arguments passed.  
 */
#include "../b/String.h"
#include "../b/Bool.h"
#include "config_parser.c"

bool contains_args(StringArray* args, const char* short_, const char* long_);

/** Parses the args array and calls the functions responsible for the
 * whole program. This returns an int as information to the main()
 * function on what to do next. This returns [1] if main needs to print
 * a fatal error message, returns [0] otherwise. 
 */
int start(StringArray* args)
{
    // Sneaky addition of "-h" if no arguments are found
    if (stringArrayLength(args) <= 1) {
        stringArrayAdd(args, newString("--help"));
    }

    // Looking for help option, if it's found the help page is brought up
    // and printed, ending the program.
    if (contains_args(args, "-h", "--help")) {
        
        // Clearing .\ if found from the execname
        String exec_name = stringArrayGet(args, 0);
        String __t = stringSubstr(&exec_name, 0, 2);
        
        // Prefix setting
        #if OS == OS_WIN
            String prefix = newString(".\\");
        #else
            String prefix = newString("./");
        #endif
        
        // Small prefix
        if (stringCompare(&__t, &prefix)) {
            exec_name = stringSubstr(&exec_name, 2, stringLength(&exec_name) - 2);
        }

        // Full path, for some reason        (linux support too)
        if (stringGetChar(&__t, 0) == 'C' || stringGetChar(&__t, 0) == '/') {
            StringArray splits = stringSplit(&exec_name, '\\');
            exec_name = stringArrayGet(&splits, stringArrayLength(&splits) - 1);
        }

        // Help page print
        printf("Usage: "); stringPrint(&exec_name); printf(" [build | run] [-h] [-p] script\n");
        printf("   build | run  : Build a star / run a star\n");
        printf("   -h, --help   : Show this and quit\n");
        printf("   -p, --parse  : Parse the script files before packing\n");
        printf("   -c, --config : Use the configuration file for building\n");
        printf("   script       : Name of the main file, like `Main`\n\n");

        printf("* The configuration file (pack.config) can be found in the installation\n");
        printf("  location of the Starbuilder.\n\n");

        printf("* This is the Starbuilder application used for building *.star files from\n");
        printf("  asx scripts. A single *.star file contains the main entrypoint for the\n");
        printf("  program, as well as all its dependencies in one place! This can be useful\n");
        printf("  for easy version control and dependency managment.\n\n");

        return 0;
    }

    /* Actual options, because -h/--help quits the program after showing the page
     *
     * A list of options to choose from:
     *   -h, --help   : Show the help page and quit.
     *   -p, --parse  : Parse the astro files before packing
     *   -c, --config : Use the configuration file for packing
     * 
     */
    bool opt_parse = false;
    bool opt_config = false;

    if (contains_args(args, "-p", "--parse")) {
        opt_parse = true;
    }

    if (contains_args(args, "-c", "--config")) {
        opt_config = true;
    
        // Config parser
        StringMap config = parse_config(newString("build.config"));
        stringMapPrint(&config);
    }

    return 0;
}

/** This is a shorthand for finding if the options are in the
 * argument array. This just saves some time and space in
 * the code, makes it more readable.
 */
bool contains_args(StringArray* args, const char* short_, const char* long_)
{
    if ((stringArrayFind(args, newString(short_)) != -1) || (stringArrayFind(args, newString(long_)) != -1)) {
        return true;
    }
    return false;
}
