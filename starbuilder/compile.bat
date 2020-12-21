:: Compiling rules for the Star astro package compiler
@echo off

set run=false
set compile=true
set help=false

set /A argc=0
(for %%a in (%*) do (
    set /A argc = %argc% + 1

    :: Arguments
    if %run%==false if "%%a"=="-r" set run=true
    if %run%==false if "%%a"=="--run" set run=true

    if %compile%==true if "%%a"=="-n" set run=false
    if %compile%==true if "%%a"=="--no-compile" set run=false

    if %help%==false if "%%a"=="-h" set help=true
    if %help%==false if "%%a"=="--help" set help=true

))

:: Show help page
if %help%==true call :help_page

:: Compiling with gcc
if %compile%==true gcc .\Starbuilder.c -o Starbuilder

:: Run after compiling
if %run%==true .\Starbuilder

goto :END

:help_page
    echo Usage: compile.bat [-r] [-n] [-h]
    echo -h, --help        - Show this
    echo -n, --no-compile  - Do not compile
    echo -r, --run         - Run after compilation
    goto :END

:END
