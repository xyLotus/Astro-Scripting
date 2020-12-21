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
    String* value;
    int len;
} StringArray;


// String methods
String newString(const char* __s);  // Constructor
String stringSubstr(String* str, int __i, int size);  // Returns a substring from the created string 
int    stringLength(String* str);   // Returns the length of the string
char*  stringGet(String* str);  // Returns the chars from the String
char   stringGetChar(String* str, int __i);  // Returns the character at the given index
void   stringSet(String* str, const char* __s);  // Set the string to another character array 
void   stringAdd(String* str, const char* __s);  // Appends a char array to the String object
void   stringAddChar(String* str, char __c);  // Adds a single character to the String object
void   stringPrint(String* str); // Just prints the string, nothing else
void   stringQPrint(String* str);  // Prints the string but in quotes
void   stringReplaceChar(String* str, char a, char b);  // Replaces all char a's with char b's
void   stringReplace(String* str, const char* a, const char* b);  // Replaces all the substrings with the given substring. 
void   stringRemoveChar(String* str, char __c);  // Removes the selected character from the string
void   stringUpper(String* str);  // Changes the string to upper case
void   stringLower(String* str);  // Changes the string to lower case
void   stringStrip(String* str);  // Strips the string
bool   stringCompare(String* str, String* other);  // Checks if the string is equal to the other string
int    stringFindChar(String* str, char __c);  // Finds the character and return its index
int    stringFind(String* str, String* other);  // Finds the string and returns the 

// Transforming methods
StringArray stringSplit(String* str, char __c);  // Splits the string by the character
String      stringArrayJoin(StringArray* arr);  // Joins the string array into a string

// StringArray methods
StringArray newStringArray();  // Constructor
int         stringArrayLength(StringArray* arr);  // Returns the length of the string array
void        stringArrayAdd(StringArray* arr, String str);  // Add one string to the array
void        stringArrayPut(StringArray* arr, String str, int __i);  // Puts the string in the selected index
void        stringArrayPrint(StringArray* arr);  // Prints the string array in a nice list
String      stringArrayGet(StringArray* arr, int __i);  // Returns the string at the element

#include "String.c"
#endif // B_INCLUDED_STRING
