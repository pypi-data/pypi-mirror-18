#!/usr/bin/env python2
import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="cythereal-vbsdk",
    version="0.4.0",
    author="Cythereal",
    author_email="webmaster@cythereal.com",
    url="https://bitbucket.org/cythereal/virusbattle-sdk/src",
    description=("Client for accessing Cythereal Virusbattle and MAGIC"),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Security",
    ],
    license="Apache Software License 2.0",
    install_requires=[
        "requests>=2.11.1",
        "validate_email>=1.3",
    ],
    extras_require={
        'DEV': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            "vbclient=vbsdk:main",
        ],
    },
    packages=find_packages(exclude=['bin/']),
    package_data={
        'config': ['config/*.ini'],
        'libs': ['lib/*'],
    },
    py_modules=[ ],
)
