#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
import ast
import re

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open(os.path.join(root_dir, 'pysimplevtk', '__init__.py'), 'r') as f:
    version = str(ast.literal_eval(_version_re.search(f.read()).group(1)))

setup(
    name='pysimplevtk',
    version=version,
    packages=find_packages(),
    url='https://github.com/ZeeD26/pysimplevtk',
    license='BSD',
    author='Dominik Steinberger',
    author_email='zeed.dev@icloud.com',
    description='High level wrapper to work with vtk xml files.',
    install_requires=[
        'numpy'
    ])
