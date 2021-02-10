# vsgb
A simple Game Boy emulator writen in Python
## [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/vitorsilverio/pygb)
[![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6InZpdG9yc2lsdmVyaW8iLCJyZXBvMSI6InZzZ2IiLCJpbmNsdWRlTGludCI6ZmFsc2UsImF1dGhvcklkIjoxMjQ4MSwiaWF0IjoxNjEyOTE2NzA2fQ.3C83CcYSlgCYnWsN7VFulf2QMM0deE8LJTpU5-WaArk)](https://www.deepcode.ai/app/gh/vitorsilverio/vsgb/_/dashboard?utm_content=gh%2Fvitorsilverio%2Fvsgb)

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
- `-s` or `--skip` Skip boot rom, let you go directly to rom
- `-c` or `--cgb` Game Boy Color mode

## Controller
- `Button A` <kbd> Z </kbd>
- `Button B` <kbd> X </kbd>
- `Button START` <kbd> Return ⏎ </kbd>
- `Button SELECT` <kbd> Backspace ⌫ </kbd>
- `Directional UP` <kbd> ↑ </kbd>
- `Directional DOWN` <kbd> ↓ </kbd>
- `Directional LEFT` <kbd> ← </kbd>
- `Directional RIGHT` <kbd> → </kbd>
- `Create Save State` <kbd> F4 </kbd>
- `Load Save State` <kbd> F5 </kbd>

## Coverage
- vsgb passed all cpu instruction tests

![](./screenshots/cpu_inst_tests.png)
