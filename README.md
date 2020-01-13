# vsgb
A simple Game Boy emulator writen in Python
## [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/vitorsilverio/pygb)

## Requirements
- Python >= 3.6 (pypy3 is recommended instead)
- PyOpenGL (https://pypi.org/project/PyOpenGL/)
- FreeGLUT (http://freeglut.sourceforge.net/)

## Running
The executable is:
- `python main.py` if you are running directly by Python script
* For performance, it is recommended to use [pypy3](https://pypy.org/) instead of python3

`executable -r romfile.gb`

### Parameters
- `-r` or `--rom` Specify the rom file
- `-d` or `--debug` Set logging to DEBUG and output to file
- `-s` or `--skip` Skip boot rom, let you directly to rom
- `-c` or `--cgb` Game Boy Color mode

## Coverage
- vsgb passed all cpu instruction tests
![](./screenshots/cpu_inst_tests.png)
