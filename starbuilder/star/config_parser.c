/**
 * This is the config parser for the
 * 
 */
#include <stdlib.h>
#include <stdio.h>
#define B_DEBUG
#include "../b/String.h"

/** This function parses the config located at the given filename,
 * and returns the StringMap of the keys and values read.
 */
StringMap parse_config(String filename)
{
    FILE* fp = fopen(stringGet(&filename), "r");

    if (fp == NULL) {
        raise(RuntimeError, "File not found");
    }

    StringMap config = newStringMap();

    char buf[1024];
    while (fgets(buf, 1024, fp)) {
        String line = newString((const char*) buf);
        stringStrip(&line);
        line = stringSubstr(&line, 0, stringLength(&line) - 1);

        // Adds the line to the config map if its not an empty line or
        // a commented line.
        if (stringLength(&line) != 0) {
            if (stringGetChar(&line, 0) != '#') {
                
                StringArray element = stringSplit(&line, '=');
                if (stringArrayLength(&element) != 2) {
                    raise(RuntimeError, "Invalid configuration file");
                }
                
                String key = stringArrayGet(&element, 0);
                stringStrip(&key);
                stringLower(&key);
                String value = stringArrayGet(&element, 1);
                stringStrip(&value);
                
                stringMapAdd(&config, key, value);
            }
        }
    }

    fclose(fp);
    return config;

}
