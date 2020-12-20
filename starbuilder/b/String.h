/**
 * String.h
 * 
 * This is the interface for the String structure and its 
 * functions.
 * 
 */
#ifndef B_INCLUDED_STRING
#define B_INCLUDED_STRING
#include <string.h>
#include "Base.h"

// Dynamic array of characters
typedef struct {
    char* value;
    int len;
} String;


// Dynamic array of strings
typedef struct {
    String* buf;
    int len;
} StringArray;


// String methods
String newString(const char* __s);  // Constructor
int    stringLength(String* str);   // Returns the length of the string
char*  stringGet(String* str);  // Returns the chars from the String
void   stringSet(String* str, const char* __s);  // Set the string to another character array 
void   stringAdd(String* str, const char* __s);  // Appends a char array to the String object
void   stringAddChar(String* str, char __c);  // Adds a single character to the String object
void   stringPrint(String* str); // Just prints the string, nothing else
void   stringReplaceChar(String* str, char a, char b);  // Replaces all char a's with char b's
void   stringReplace(String* str, const char* a, const char* b);  // Replaces all the substrings with the given substring. 
void   stringRemoveChar(String* str, char __c);  // Removes the selected character from the string
void   stringUpper(String* str);  // Changes the string to upper case
void   stringLower(String* str);  // Changes the string to lower case

#include "String.c"
#endif // B_INCLUDED_STRING
