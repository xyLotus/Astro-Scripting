/**
 * String.h
 * 
 * This is the interface for the String structure and its 
 * functions.
 * 
 */
#ifndef B_STRING_H
#define B_STRING_H
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


// Dynamic map of strings
typedef struct {
    StringArray keys;
    StringArray values;
    int len;
} StringMap;


// -----------------------------------------------------------------------
// String
// -----------------------------------------------------------------------

/* Creates a new String object from a constant char*.
 * As this does not use the stdlib string.h library,
 * it counts the length of the string by finding the 
 * null terminator. This is possible because the compiler
 * adds a null terminator to every defined const char*.
 */
String newString(const char* __s);

/* Returns the substring of a string 
 */
String stringSubstr(String* str, int __i, int size);

/* Returns the length of the string object. 
 */
int stringLength(String* str);

/* Returns the value of the string as a char ptr. 
 */
char* stringGet(String* str);

/* Retruns the character at the given index. Raises an
 * OverflowError if the char is out of bounds.
 */
char stringGetChar(String* str, int __i);

/* Sets the current string to the new string. Nothing more, 
 * just replaces the whole thing.
 */
void stringSet(String* str, const char* __s);

/* Adds a const char* to the passed reference to the string 
 * object. How it works: First, the size of the const char*
 * is checked to allocate enough memory for the new string.
 * After creating a new char array, the base string and the
 * new string are copied over to it. 
 */
void stringAdd(String* str, const char* __s);

/* Adds a single character to the string.  
 */
void stringAddChar(String* str, char __c); 

/* Print the string to stdout. This is used because printing
 * the normal str value using printf may cause formatting problems.
 */
void stringPrint(String* str); 

/* Prints the string but with quotes around it and a newline at the 
 * end. This was added to save some painful printf typing at the 
 * begginning and end of the stringPrint method.
 */
void stringQPrint(String* str);

/* Replaces all char a's with char b's in the whole string. 
 * This is much more efficient than the stringReplace method
 * which replaces substrings, so please use this when possible.
 */
void stringReplaceChar(String* str, char a, char b);

/* Replaces all the found substrings with another substring.
 * Note: this operation is pretty expensive, so please use
 * stringReplaceChar whenever possible instead. How it works:
 * First, the length of both strings are calculated. Then, the
 * occurences are found. After that, a buffer is created to
 * store the result.
 */
void stringReplace(String* str, const char* a, const char* b); 

/* Removes the selected character from the string and removes it. 
 * How it works: First, the amount of matching characters are counted.
 * Then, a char pointer array is created with the selected amount of
 * fields. After that every not matching char is copied to the new
 * buffer, and assigned back to the string object. 
*/
void stringRemoveChar(String* str, char __c);

/* Replaces every lower case letter with its upper case equivalent. 
 */ 
void stringUpper(String* str);

/* Replaces every upper case letter with its lower case equivalent. 
 */
void stringLower(String* str); 

/* Removes spaces from both the sides of the string. 
 */
void stringStrip(String* str); 

/* Checks if the 2 strings are equal, returns false if fails. 
 * It checks the length of both strings first, to make it faster
 * to process. If the length is the same, it checks every char
 * until it hits the end or a different one.
 */ 
bool stringCompare(String* str, String* other); 

/* Returns the index of the first occurence of the passed character,
 * if no matching character is found it returns -1.
 */
int stringFindChar(String* str, char __c);

/* Returns the index of the first letter in the string that matches the
 * other string. Returns -1 if no match is found.
 */
int stringFind(String* str, String* other); 

// Transforming methods

/* Splits the string into multiple pieces and pushes them to the
 * StringArray.
 */
StringArray stringSplit(String* str, char __c);

/* Collects all the elements of a string array into a single string
 * that is then returned. 
 */
String stringArrayJoin(StringArray* arr);

// -----------------------------------------------------------------------
// StringArray
// -----------------------------------------------------------------------

/* String array constructor. This creates a new StringArray with 
 * the string buffor set to a NULL pointer and the length to 0.
 */
StringArray newStringArray();

/* Returns the length of the string array.
 */
int stringArrayLength(StringArray* arr);

/* Adds a single thing to the string array. 
 */
void stringArrayAdd(StringArray* arr, String str);

/* Puts a new string in the selected index of the array.
 * Raises OverflowError if the index is out of bounds.
 */
void stringArrayPut(StringArray* arr, String str, int __i); 

/* Prints the contents of the list to stdout 
 */
void stringArrayPrint(StringArray* arr);

/* Returns the string at the given index, raises an
 * OverflowError if it fails.
 */
String stringArrayGet(StringArray* arr, int __i);

/* Finds the index of the given string, returns -1 if no
 * such string is found.
 */
int stringArrayFind(StringArray* arr, String match);

// -----------------------------------------------------------------------
// StringMap
// -----------------------------------------------------------------------

/* This is the constructor for the string map, it sets the
 * StringArrays to null pointers and the length to 0. Be
 * sure to call this when creating a new StringMap, or else
 * serious problems can occur.
 */
StringMap newStringMap();

/* Prints the StringMap in a nice, formatted way with brackets
 * and all that fancy stuff.
 */
void stringMapPrint(StringMap* map);

/* Adds a single key-value pair to the map, both the key and
 * the value have to be new strings, not string pointers. Apart
 * from just adding the strings to the string arrays, it checks 
 * the lengths of the arrays just in case.
 */
void stringMapAdd(StringMap* map, String key, String value);

/* This returns the length of the passed StringMap. This is the
 * preffered way of getting the length, because the contents of
 * the StringMap struct should be read only for the user.
 */
int stringMapLength(StringMap* map);

/* Returns the key at the specified index. This throws an
 * Overflow error if the index is out of bounds.
 */
String stringMapGetKey(StringMap* map, int __i);

/* Returns the value at the specified index. This throws an
 * Overflow error if the index is out of bounds.
 */
String stringMapGetValue(StringMap* map, int __i);

/* Finds the given key in the map and returns the index of
 * it. If no matching key is found, returns -1.
 */
int stringMapFindKey(StringMap* map, String match);

/* Finds the given value in the map and returns the index of
 * it. If no matching value is found, returns -1.
 */
int stringMapFindValue(StringMap* map, String match);


#include "String.c"
#endif // B_STRING_H
