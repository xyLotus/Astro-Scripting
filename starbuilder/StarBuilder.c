/**
 * This is the entrypoint for the Star Collector software. 
 * 
 * @author   bellrise
 * @version  0.0.3
 */
#include <stdio.h>
#include "b/String.h"
#include "star/controller.c"

// Main entrypoint
int main(int argc, char* argv[])
{

    // Moving arguments to a string array, omiting the filename.
    StringArray args = newStringArray();
    for (uint i = 0; i < argc; i++) {
        stringArrayAdd(&args, newString(argv[i]));
    }

    int result = start(&args);
    if (result == 1) {
        printf("\nFatal error occured during program execution.\n");
        return 1;
    }

    return 0;

}
