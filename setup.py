#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext

from multiprocessing import cpu_count

with open('./README.md', 'r') as rm:
    long_description = rm.read()

thread_count = cpu_count()
print("Thread Count:", thread_count)

setup(
    name="pygb",
    version="1.0",
    packages=find_packages(),
    author="Vitor Silverio Rodrigues",
    author_email="vitor.silverio.rodrigues@gmail.com",
    long_description=long_description,
    content_type="text/markdown",
    url="https://github.com/vitorsilverio/pygb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
        "Topic :: System :: Emulators",
    ],
    cmdclass={'build_ext': build_ext},
    install_requires=[
        "cython",
        "pyopengl",
    ],
    include_dirs=[".", "pygb"],
    zip_safe=False,
    ext_modules=cythonize([
        './pygb/input.py',
        './pygb/window.py',
        './pygb/io_registers.py',
        './pygb/mmu.py',
        './pygb/__init__.py',
        './pygb/registers.py',
        './pygb/cpu.py',
        './pygb/sound.py',
        './pygb/interrupt_manager.py',
        './pygb/ppu.py',
        './pygb/byte_operations.py',
        './pygb/timer.py',
        './pygb/emulator.py',
        './pygb/stack_manager.py',
        './pygb/cartridge.py',
        './pygb/instruction_performer.py'
        ],
        include_path=[".", "pygb"],
        nthreads=thread_count,
        annotate=False,
        language_level=2,
        compiler_directives={
            "cdivision": True,
            "cdivision_warnings": False,
            "boundscheck": False,
            "wraparound": False,
            "initializedcheck": False,
            "nonecheck": False,
            "overflowcheck": False,
            "infer_types" : True,
        },
    )
)
