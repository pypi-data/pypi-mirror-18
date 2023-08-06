import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "glassblower",
    version = "0.2.3",
    author = "Blas Martin Castro",
    author_email = "castro.blas.martin@gmail.com",
    description = ("The Best Flask Boilerplate Framework"),
    license = "BSD",
    keywords = "Flask Boilerplate Framework Web",
    url = "https://github.com/TheCraftsmen/GlassBlower-2",
    entry_points = {
        'console_scripts': ['glassblower=glassblower.glassblower:main'],
    },
    packages=['glassblower'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
