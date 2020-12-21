/**
 * Base.h
 * 
 * Base tools for the B toolkit library. This is all about 
 * random time saving tools and different data structures.
 * This does not need to be imported as every file in here
 * imports this automatically.
 * 
 * @author   bellrise
 * @version  0.2.3
 */

// Header guards
#ifndef B_INCLUDED_BASE
#define B_INCLUDED_BASE

typedef unsigned int uint;

// Debug mode
#ifdef B_DEBUG
    #define debug(FUNCTION) printf("* [%d in %s] ", __LINE__, __FUNCTION__); FUNCTION
#else 
    #define debug(FUNCTION) ;
#endif

// Base scripts that every file will include
#include "Error.h"
#include "Bool.h"
#include "String.h"



#endif
