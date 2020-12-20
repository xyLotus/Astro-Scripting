# Starbuilder

![Languages](https://img.shields.io/badge/Languages-C,%20Python-blueviolet)
![Version](https://img.shields.io/badge/Version-0.0.1-%2333aa33)

Starbuilder is a tool for creating `*.star` files which package all your Astro scripts and dependencies. This is useful for deploying
packaged scripts which can be run with one command, and also for easy and simple version control. This software is based on the `b` library.
___
### Compiling

Before actually using the program, it is required to compile it on your machine. Real releases will be placed after reaching a certain
point in development. This may sound scary, but this has also been automated for you. The only thing you need to run is this in a command
prompt of your choice. After that, you will get an executable which can be ran double clicking it, or prefferably from the command line.

#### Windows
Simply double clicking the compile.bat script will do the job, but you can also use the command line option and list the options
using `.\compile -h`
```bat
.\compile
.\StarBuilder.exe
```
#### Linux
This version is much more fun, as it offers a configuration file called `starbuilder.config` where you can change some default settings
or even automatically move the generated binary to /bin/ for later use. To make your life easier, you can stick a `chmod +x ./compile.sh`
line before doing anything, so you don't have to use `bash` every time.
```bash
bash ./compile.sh
./StarBuilder
```
___
### b

`b` is a C library containing a lot of useful tools and object models for easier, object-oriented style programming with a lot
of automatic memory allocation and background functionality. This project has been based on this library to make it a lot easier
to program.
