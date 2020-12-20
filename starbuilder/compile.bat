:: Compiling rules for the Star astro package compiler
@echo off

set run=false
set compile=true

set /A argc=0
(for %%a in (%*) do (
    set /A argc = %argc% + 1

    :: Arguments
    if %run%==false if %%a==-r set run=true
    if %compile%==true if %%a==-n set run=false

))

:: Compiling with gcc
if %compile%==true gcc .\StarBuilder.c -o Starbuilder

:: Run after compiling
if %run%==true .\a

EXIT 0
