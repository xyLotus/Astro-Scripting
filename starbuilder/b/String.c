/**
 * String.c
 * 
 * Implementation of the String.h header.
 */
#include <stdlib.h>
#include <stdarg.h>
#include "Bool.h"
#include "String.h"


// -----------------------------------------------------------------------
// String
// -----------------------------------------------------------------------


/** Creates a new String object from a constant char*.
 * As this does not use the stdlib string.h library,
 * it counts the length of the string by finding the 
 * null terminator. This is possible because the compiler
 * adds a null terminator to every defined const char*.
 */
String newString(const char* __s) 
{
    int size = 0;
    while (__s[size] != '\0') {
        size++;
    }

    String s = {(char*) __s, size};

    return s;
}

/** Returns the substring of a string */
String stringSubstr(String* str, int __i, int size) 
{
    String new = newString("");
    for (int i = __i; i < size + __i; i++) {
        char c = stringGetChar(str, i);
        stringAddChar(&new, c);
    }

    return new;
}

/** Returns the length of the string object. */
int stringLength(String* str)
{
    return str->len;
}

/** Returns the value of the string as a char ptr. */
char* stringGet(String* str)
{
    return str->value;
}

/** Retruns the character at the given index. Raises an
 * OverflowError if the char is out of bounds.
 */
char stringGetChar(String* str, int __i)
{
    if (__i >= str->len) {
        raise(OverflowError, "Index out of bounds");
    }

    return str->value[__i];
}

/** Sets the current string to the new string. Nothing more, 
 * just replaces the whole thing.
 */
void stringSet(String* str, const char* __s)
{
    String new = newString(__s);
    debug(printf("Set \"%s\" to \"%s\"\n", stringGet(str), __s));
    str->len = new.len;
    str->value = new.value;
}

/** Adds a const char* to the passed reference to the string 
 * object. How it works: First, the size of the const char*
 * is checked to allocate enough memory for the new string.
 * After creating a new char array, the base string and the
 * new string are copied over to it. 
 */
void stringAdd(String* str, const char* __s)
{
    char* joined = (char*) __s;
    int joined_len = 0;
    while (joined[joined_len] != '\0') {
        joined_len++;
    }

    char* buf = malloc(sizeof(char) * (stringLength(str) + joined_len));
    
    for (int i = 0; i < str->len; i++) {
        buf[i] = str->value[i];
    }
    
    for (int j = 0; j < joined_len; j++) {
        buf[j+str->len] = joined[j];
    }

    str->value = buf;
    str->len = str->len + joined_len;
    
    free(joined);
}


/** Adds a single character to the string. */
void stringAddChar(String* str, char __c)
{
    char buf[] = " \0";
    buf[0] = __c;
    stringAdd(str, buf);
    free(buf);
}


/** Print the string to stdout. This is used because printing
 * the normal str value using printf may cause formatting problems.
 */
void stringPrint(String* str)
{
    for (int i = 0; i < stringLength(str); i++) {
        printf("%c", str->value[i]);
    }
}


/** Prints the string but with quotes around it and a newline at the 
 * end. This was added to save some painful printf typing at the 
 * begginning and end of the stringPrint method.
 */
void stringQPrint(String* str) 
{
    printf("\""); stringPrint(str); printf("\"\n");   
}



/** Replaces all char a's with char b's in the whole string. 
 * This is much more efficient than the stringReplace method
 * which replaces substrings, so please use this when possible.
 */
void stringReplaceChar(String* str, char a, char b)
{
    for (int i = 0; i <= stringLength(str); i++) {
        if (str->value[i] == a) {
            str->value[i] = b;
        }
    }
}


/** Replaces all the found substrings with another substring.
 * Note: this operation is pretty expensive, so please use
 * stringReplaceChar whenever possible instead. How it works:
 * First, the length of both strings are calculated. Then, the
 * occurences are found. After that, a buffer is created to
 * store the result.
 */
void stringReplace(String* str, const char* a, const char* b)
{
    // Lengths
    int a_len = 0;
    int b_len = 0;
    while (a[a_len] != '\0') { a_len++; }
    while (b[b_len] != '\0') { b_len++; }

    int occurences = 0;
    bool where[(const int) str->len];
    
    // Setting all to 0
    for (int i = 0; i < str->len; i++) {
        where[i] = false;
    }

    debug(printf("Running compare loop %d times\n", str->len - a_len));
    for (int i = 0; i < str->len - a_len; i++) {
        for (int e = 0; e < a_len; e++) {
            if (str->value[i+e] == a[e]) {
                where[i+e] = true;
            }
            else {
                where[i+e] = false;
            }
        }
    }

    debug(printf("Contents of where: "); 
    for (int i = 0; i < str->len; i++) {
        printf("%d", where[i]);
    } printf("\n"); )

    // Buffer creation
    String buf = newString("\0");

    for (int i = 0; i < str->len; i++) {
        if (where[i] >= true) {
            debug(printf("Found occurence @ %d\n", i));
            stringAdd(&buf, b);
            i += a_len - 1;
        }
        else {
            stringAddChar(&buf, (char) str->value[i]);
        }
    }
    

    debug(printf("Generated string of length: %d\n", stringLength(&buf)));
    debug(stringPrint(&buf));

    str->value = buf.value;
    str->len   = buf.len;

}

/** Removes the selected character from the string and removes it. 
 * How it works: First, the amount of matching characters are counted.
 * Then, a char pointer array is created with the selected amount of
 * fields. After that every not matching char is copied to the new
 * buffer, and assigned back to the string object. 
*/
void stringRemoveChar(String* str, char __c)
{
    int found = 0;
    for (int i = 0; i < stringLength(str); i++) {
        if (str->value[i] == __c) {
            found++;
        }
    }

    debug(printf("Found %d '%c' character(s)\n", found, __c));

    // Character buffer
    char* buf = malloc(sizeof(char) * (stringLength(str) - found));

    int j = 0;
    for (int i = 0; i < stringLength(str); i++) {
        if (str->value[i] != __c) {
            buf[j] = str->value[i];
            j++;
        }
    }

    str->len = stringLength(str) - found;
    str->value = buf;
}

/** Replaces every lower case letter with its upper case equivalent. */
void stringUpper(String* str)
{
    for (int i = 0; i <= stringLength(str); i++) {
        if (str->value[i] >= 97 && str->value[i] <= 122) {
            str->value[i] += 'A' - 'a';
        }
    }
}

/** Replaces every upper case letter with its lower case equivalent. */
void stringLower(String* str)
{
    for (int i = 0; i <= stringLength(str); i++) {
        if (str->value[i] >= 65 && str->value[i] <= 90) {
            str->value[i] -= 'A' - 'a';
        }
    }
}

/** Removes spaces from both the sides of the string. */
void stringStrip(String* str) 
{
    int leftw = 0;
    int rightw = 0;

    // Left side
    while (true) {
        if (stringGetChar(str, leftw) != ' ') {
            break;
        }
        leftw++;
    }

    while (true) {
        if (stringGetChar(str, stringLength(str) - rightw - 1) != ' ') {
            break;
        }
        rightw++;
    }

    debug(printf("Spaces found: %d...%d", leftw, rightw));

    *str = stringSubstr(str, leftw, stringLength(str) - leftw - rightw);

}

/** Checks if the 2 strings are equal, returns false if fails. 
 * It checks the length of both strings first, to make it faster
 * to process. If the length is the same, it checks every char
 * until it hits the end or a different one.
 */ 
bool stringCompare(String* str, String* other) 
{
    // Length check
    if (str->len != other->len) {
        return false;
    }

    // Comparing
    for (int i = 0; i < str->len; i++) {
        if (str->value[i] != other->value[i]) {
            return false;
        }
    }
    return true;
}

/** Returns the index of the first occurence of the passed character,
 * if no matching character is found it returns -1.
 */
int stringFindChar(String* str, char __c) 
{
    for (int i = 0; i < str->len; i++) {
        if (str->value[i] == __c) {
            return i;
        }
    }
    return -1;
}

/** Returns the index of the first letter in the string that matches the
 * other string. Returns -1 if no match is found.
 */
int stringFind(String* str, String* other) 
{
    int size = other->len;

    if (size > str->len) {
        return -1;
    }

    for (int i = 0; i < str->len - size; i++) {
        String a = stringSubstr(str, i, size);
        if (stringCompare(&a, other)) {
            return i;
        }
    }
    return -1;
}

/** Splits the string into multiple pieces and pushes them to the
 * StringArray.
 */
StringArray stringSplit(String* str, char __c) 
{
    StringArray buf = newStringArray();

    int cursor = 0;
    while (cursor < str->len) {
        debug(printf("Subbing string from %d to %d", cursor, str->len - cursor));
        String temp = stringSubstr(str, cursor, str->len - cursor);
        int to = stringFindChar(&temp, __c);
        debug(printf("Found %c at %d in: ", __c, to); stringPrint(&temp); printf("\n"));
        if (to == -1) {
            break;
        }
        stringArrayAdd(&buf, stringSubstr(str, cursor, to));
        cursor += to + 1;
    }

    stringArrayAdd(&buf, stringSubstr(str, cursor, str->len - cursor));

    return buf;
}


// TODO: NEEDS FIXING, DOESNT WORK

/** Collects all the elements of a string array into a single string
 * that is then returned. */
String stringArrayJoin(StringArray* arr)
{
    String new = newString("");
    for (int i = 0; i < stringArrayLength(arr); i++) {
        String s = stringArrayGet(arr, i);
        stringAdd(&new, (const char*) stringGet(&s));
    }

    return new;
}

// -----------------------------------------------------------------------
// StringArray
// -----------------------------------------------------------------------


/** String array constructor. This creates a new StringArray with 
 * the string buffor set to a NULL pointer and the length to 0.
 */
StringArray newStringArray() 
{
    StringArray arr = {NULL, 0};
    return arr;
}

/** Returns the length of the string array. */
int stringArrayLength(StringArray* arr) 
{
    return arr->len;
}

/** Adds a single thing to the string array. */
void stringArrayAdd(StringArray* arr, String str) 
{
    debug(printf("Reallocating to sizeof(String) * %d\n", (arr->len + 1)));
    arr->value = realloc(arr->value, sizeof(String) * (arr->len + 1));
    arr->value[arr->len] = str;
    arr->len++;
}

/** Puts a new string in the selected index of the array.
 * Raises OverflowError if the index is out of bounds.
 */
void stringArrayPut(StringArray* arr, String str, int __i)
{
    if (__i >= arr->len) {
        raise(OverflowError, "Index out of bounds");
    }

    arr->value[__i] = str;
}

/** Prints the contents of the list to stdout */
void stringArrayPrint(StringArray* arr) 
{
    printf("[");
    for (int i = 0; i < stringArrayLength(arr) - 1; i++) {
        printf("\""); stringPrint(&arr->value[i]); printf("\", ");
    }
    printf("\""); stringPrint(&arr->value[arr->len - 1]); printf("\"");
    printf("]");
}

/** Returns the string at the given index, raises an
 * OverflowError if it fails.
 */
String stringArrayGet(StringArray* arr, int __i) 
{
    if (__i >= arr->len) {
        raise(OverflowError, "Index out of bounds");
    }

    return arr->value[__i];
}
