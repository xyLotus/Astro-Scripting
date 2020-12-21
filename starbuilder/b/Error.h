/**
 * This is the header file for the Error system in b.
 * This defines the Error and a couple of methods with
 * the errors.
 */
#ifndef B_ERROR_H
#define B_ERROR_H

typedef struct {
    int id;
    char* name;
} Error;


static Error RuntimeError  = { 0,  "RuntimeError"  };
static Error StringError   = { 1,  "StringError"   };
static Error OverflowError = { 2,  "OverflowError" }; 
static Error MemoryError   = { 3,  "MemoryError"   };

#include "Error.c"
#endif  // B_ERROR_H
