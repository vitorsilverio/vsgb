# pygb
A simple gameboy emulator writen in python

## Requirements
- Python >= 3.6
- PyOpenGL (https://pypi.org/project/PyOpenGL/)
- FreeGLUT (http://freeglut.sourceforge.net/)
* If you want to compile a binary:
  - pyinstaller
  - wheel
  
## Compiling
pyinstaller --onefile main.py -n pygb
The binary file will be in dist directory

## Running
The executable will be:
- **python main.py** if you running directly by python script
- **pygb** if you compiled the source


**executable** -r romfile.gb

## Parameters
- **-r/-rom** Specify the rom file
- **-d/--debug** Set logging to DEBUG and output to file
- **-s/--skip** Skip boot rom, let me directly to rom
