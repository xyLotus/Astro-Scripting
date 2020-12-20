/**
 * This is the header file for the Error system in b.
 * This defines the Error and a couple of methods with
 * the errors.
 */
#ifndef B_INCLUDED_ERROR
#define B_INCLUDED_ERROR

typedef struct {
    int id;
    char* name;
} Error;


static Error RuntimeError  = { 0,  "RuntimeError"  };
static Error StringError   = { 1,  "StringError"   };
static Error OverflowError = { 2,  "OverflowError" }; 

#include "Error.c"
#endif  // B_INCLUDED_ERROR
