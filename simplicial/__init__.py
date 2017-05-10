# Initialisation for simplicial package
#
# Copyright (C) 2017 Simon Dobson
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

'''`simplicial` is a Python package for manipulating simplicial
topological complexes.

Simplicial complexes are generalisations of the triangulation of a
plane. A :term:`complex` is built from simplices (singular:
:term:`simplex`), and can be used for a number of purposes: as
discrete approximations of continuous spaces or manifolds, or as
abstract descriptions of information relationships that can then be
explored and anlysed using techniques from algebraic :term:`topology`.

`simplicial` provides a class of :class:`SimplicialComplex` to
represents complexes and provide some topological operations. It also
provides some "standard" complexes, typically representatives of a
particularly structured class of spaces, that can be used as building
blocks for larger complexes.

`simplicial` also provides functions to visualise complexes, although
these need a lot more work for them to be really useful.

'''

# representation and computation
from .simplicialcomplex import SimplicialComplex

# some sample figures
from .triangularlattice import TriangularLattice
from .toroidallattice import ToroidalLattice

# file I/O
import simplicial.file
from simplicial.file import *

# drawing support
#import simplicial.drawing
#from simplicial.drawing import *


