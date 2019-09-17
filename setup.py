#!/usr/bin/env python

# Setup for simplicial
#
# Copyright (C) 2017--2019 Simon Dobson
# 
# This file is part of simplicial, simplicial topology in Python.
#
# Simplicial is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Simplicial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Simplicial. If not, see <http://www.gnu.org/licenses/gpl.html>.

from setuptools import setup

with open('README.rst') as f:
    longDescription = f.read()

setup(name = 'simplicial',
      version = '0.5.1',
      description = 'Simplicial topology in Python',
      long_description = longDescription,
      url = 'http://github.com/simoninireland/simplicial',
      author = 'Simon Dobson',
      author_email = 'simon.dobson@computer.org',
      license = 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      classifiers = [ 'Development Status :: 4 - Beta',
                      'Intended Audience :: Science/Research',
                      'Intended Audience :: Developers',
                      'Programming Language :: Python :: 2.7',
                      'Programming Language :: Python :: 3.7',
                      'Topic :: Scientific/Engineering :: Mathematics',
                      'Topic :: Scientific/Engineering :: Physics' ],
      packages = [ 'simplicial' ],
      zip_safe = True,
      install_requires = [ "numpy","matplotlib" ])


