# Starbuilder

![Languages](https://img.shields.io/badge/Languages-C,%20Python-blueviolet)
![Version](https://img.shields.io/badge/Version-0.0.3-%2333aa33)

Starbuilder is a tool for creating `*.star` files which package all your Astro scripts and dependencies. This is useful for deploying
packaged scripts which can be run with one command, and also for easy and simple version control. This software is based on the `b` library.

___
## Building
Building your own star is as simple as typing one command, but it can be made nicer customizing a couple of lines. The versions are a bit different
on Windows and Linux, but they only really are different in one aspect - the executable name.

```batch
# Windows
> .\Starbuilder.exe build MyScript

# Linux 
$ asx-star build MyScript
```


#### Options
* `-h`, `--help` Show the help page and quit
* `-p`, `--parse` Parse the .asx files before packing
* `-c`, `--config` Use the configuration file for building


## Configuring
After building your first star, you can clearly see it's named `ExampleScript_0-0-1.star`. You probably want to change this, along with its version.
To achieve this, you simple need to edit a few lines in the `build.config` file to your liking.
```
# build.config

NAME    = MyScript
VERSION = 1.0.0
```
Save the file, and then run the build command again, but this time with the `--config` option to let the builder know you want to use
the configuration file.
```
$ Starbuilder build --config MyScript
```
And there you have it, `MyScript_1-0-0.star`!


___
## Compiling

Before actually using the program, it is required to compile it on your machine. Real releases will be placed after reaching a certain
point in development. This may sound scary, but this has also been automated for you. The only thing you need to run is this in a command
prompt of your choice. After that, you will get an executable which can be ran double clicking it, or prefferably from the command line.

#### Windows
Simply double clicking the compile.bat script will do the job, but you can also use the command line option and list the options
using `.\compile -h`
```bat
> .\compile
> .\StarBuilder.exe
```
#### Linux
This version is much more fun, as it offers a configuration file called `starbuilder.config` where you can change some default settings
or even automatically move the generated binary to /bin/ for later use. To make your life easier, you can stick a `chmod +x ./compile.sh`
line before doing anything, so you don't have to use `bash` every time.
```bash
$ bash ./compile.sh
$ ./StarBuilder
```
___
### b

`b` is a C library containing a lot of useful tools and object models for easier, object-oriented style programming with a lot
of automatic memory allocation and background functionality. This project has been based on this library to make it a lot easier
to program.
