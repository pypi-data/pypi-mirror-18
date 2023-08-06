#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import sys

from setuptools import find_packages

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

requirements = open('requirements.txt').readlines()

# Strip comments and newlines from requirements.
parsed_requirements = []
for req in requirements:
   req = req.strip()
   if not req or req.startswith('#'):
       continue
   parsed_requirements.append(req)

setup(
   name='dstore-sdk-python',
   version='1.0.2.3',
   author='dbap GmbH',
   author_email='',
   packages=find_packages(exclude=['tests']),
   url='http://www.dstore.de',
   include_package_data=True,
   install_requires=parsed_requirements,
   classifiers=[ ],
   description='dStore SDK for Python lanaguage.',
   long_description=open('README.md').read() + '\n\n',
)
