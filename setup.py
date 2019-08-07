import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="pygb",
    version="1.0.0",
    description="A simple gameboy emulator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vitorsilverio/pygb",
    author="Vitor",
    author_email="vitor.silverio.rodrigues@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["pygb"],
    include_package_data=True,
    install_requires=[
        "PyOpenGL"
    ],
    entry_points={"console_scripts": ["pygb=main:main"]},
)
