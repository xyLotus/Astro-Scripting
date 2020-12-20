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

    debug(printf("Concatinating '%s' + '%s'\n", stringGet(str), joined));
    
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
