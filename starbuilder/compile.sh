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
opt_cfg="false"


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

function load_config {
    # Loads the config from the file
    
    cfg_main="StarBuilder.c"
    cfg_name="StarBuilder"
    cfg_bin="false"

    local ln=0
    while read line; do
        
        if [ ${line:0:1} != "#" ]; then 
            # Non comment line, parse and set        
            # Splitting the line
            IFS='='
            read -ra ADDR <<< "$line"
            local setting=${ADDR[0]}
            local data=${ADDR[1]}
            
            if [ $setting == "MAIN" ]; then cfg_main=$data; fi   
            if [ $setting == "NAME" ]; then cfg_name=$data; fi   
            if [ $setting == "BIN" ]; then cfg_bin=$data; fi   
        fi

        # Counter step
        ln=$(( ln + 1 ))
    done < starbuilder.config

}

# Load config before continuing to compilation
load_config

if [ $opt_help == "true" ]; then
    print_help
fi  

if [ $opt_compile == "true" ]; then
    gcc ./$cfg_main -o $cfg_name  
fi  

if [ $opt_run == "true" ]; then
    chmod +x ./$cfg_name
    ./$cfg_name
fi

if [ $cfg_bin == "true" ]; then
    sudo mv ./$cfg_name /bin/$cfg_name
    rm ./$cfg_name
fi


