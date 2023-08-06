#!/usr/bin/env python

import os
import os.path
from setuptools import setup

os.chdir(os.path.abspath(os.path.dirname(__file__)))

setup(
    version="0.1.0",
    url="https://github.com/nathforge/expbackoff",
    name="expbackoff",
    description="Exponential backoff with jitter.",
    long_description=open("README.rst").read(),
    author="Nathan Reynolds",
    author_email="email@nreynolds.co.uk",
    packages=["expbackoff"],
    package_dir={"": "src"},
    test_suite="tests",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7"
    ]
)
