#!/bin/bash

# This is a simple bash script to help in the compilation process,
# making it super simple and quick by just typing in one line.
# There are some config options which you can view by using the
# -h or --help option.

argv=("$@")

# Default options
opt_compile="true"
opt_run="false"
opt_help="false"


for arg in "${argv[@]}"; do
    # Compile option    
    if [ $opt_compile == "true" ]; then
        if [ $arg == "-n" ] || [ $arg == "--no-compile" ]; then
            opt_compile="false"
        fi 
    fi

    # Run option
    if [ $opt_run == "false" ]; then
        if [ $arg == "-r" ] || [ $arg == "--run" ]; then
            opt_run="true"
        fi 
    fi
    
    # Help option
    if [ $opt_help == "false" ]; then
        if [ $arg == "-h" ] || [ $arg == "--help" ]; then
            opt_help="true"
        fi 
    fi

done

function print_help {
    # Print the help screen and quit    
    echo "Usage: compile.sh [-h] [-r] [-n]"
    echo "       -h, --help : Shows this page"
    echo "       -r, --run  : Runs the program after compilation"
    echo "       -n, --no-compile : Don't compile the program" 
    exit 0
}


if [ $opt_help == "true" ]; then
    print_help
fi  

if [ $opt_compile == "true" ]; then
    gcc ./StarBuilder.c -o StarBuilder  
fi  

if [ $opt_run == "true" ]; then
    chmod +x ./StarBuilder
    ./StarBuilder
fi

