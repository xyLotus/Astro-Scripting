/**
 * This is the implementation of the Error methods defined
 * in the Error.h header file.
 */
#include <stdlib.h>
#include <stdio.h>
#include "Error.h"

/** Internal function for the raise function. This is wrapped in
 * the raise(ERROR) defined below. 
 */
void binternal_raise(Error err, int line, const char* func, char* file, char* why)
{
    printf("[!] %s:\n", err.name);
    printf(" * \"%s\", in %s(...) on %d\n", file, func, line);
    printf(" * -> %s\n", why);
    exit(EXIT_FAILURE);
}

#define raise(ERROR, WHY) binternal_raise(ERROR, __LINE__, __FUNCTION__, __FILE__, WHY)
