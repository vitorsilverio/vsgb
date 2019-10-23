# vsgb
A simple gameboy emulator writen in python
## [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/vitorsilverio/pygb)

## Requirements
- Python >= 3.6 ( i recommend to use pypy instead )
- PyOpenGL (https://pypi.org/project/PyOpenGL/)
- FreeGLUT (http://freeglut.sourceforge.net/)


## Running
The executable will be:
- **python main.py** if you running directly by python script
* For performance i recommend to use pypy3 instead python3

**executable** -r romfile.gb

## Parameters
- **-r/--rom** Specify the rom file
- **-d/--debug** Set logging to DEBUG and output to file
- **-s/--skip** Skip boot rom, let me directly to rom

## Coverage
- vsgb passed all cpu instruction tests
- ![](./screenshots/cpu_inst_tests.png)
