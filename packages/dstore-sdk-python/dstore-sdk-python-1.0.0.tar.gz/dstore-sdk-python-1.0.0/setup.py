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

try:
   from setuptools import setup
   setup  # workaround for pyflakes issue #13
except ImportError:
   from distutils.core import setup

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
   version='1.0.0',
   author='dbap GmbH',
   author_email='',
   packages=find_packages(exclude=['tests']),
   url='http://www.dstore.de',
   #data_files=[('conf', [os.path.join('conf', _) for _ in os.listdir('conf') if _.startswith('example-')]),
   #            ('scripts', [os.path.join('scripts', _) for _ in os.listdir('scripts') if _.startswith('spam')])],
   include_package_data=True,
   install_requires=parsed_requirements,
   license='LICENSE',
   classifiers=[ ],
   description='dStore SDK for Python lanaguage.',
   long_description=open('README.md').read() + '\n\n',
)
