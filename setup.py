#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "nova-tunner",
    version = "0.2",
    author = "Alexis López Zubieta",
    author_email = "azubieta@estudiantes.uci.cu",
    description = ("Application to customize the system on the first boot."),
    license = "GPL3",
    keywords = "system optimization",
    url = "http://...",
    long_description=read('README'),
    packages=['nova_tunner_extensions', 'nova_tunner'],
    scripts = ['bin/nova_tunner'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
    ],
)
