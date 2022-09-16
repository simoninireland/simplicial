# Initialisation for simplicial package
#
# Copyright (C) 2017--2022 Simon Dobson
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

'''``simplicial`` is a Python package for manipulating simplicial
complexes.

Simplicial complexes are generalisations of the triangulation of a
plane. A :term:`complex` is built from simplices (singular:
:term:`simplex`), and can be used for a number of purposes: as
discrete approximations of continuous spaces or manifolds, or as
abstract descriptions of information relationships that can then be
explored and anlysed using techniques from algebraic :term:`topology`.

``simplicial`` provides a class :class:`SimplicialComplex` to
represents complexes and provide some topological operations. It also
provides some "standard" complexes, typically representatives of a
particularly structured class of spaces, that can be used as building
blocks for larger complexes. It also provides a function to "embed"
a complex into a space, which can be used for spatial computing and
for visualisation (although this still needs a lot more work).

'''

# representation and computation
from .types import Simplex, Attributes, Renaming
from .rep import Representation
from .simplicialcomplex import ReferenceRepresentation
from .base import SimplicialComplex

# generator functions for common complexes
from .generators import k_simplex, k_skeleton, k_void, ring

# sequences of complexes ordered by inclusion
from .filtration import Filtration

# Euler integration
from .eulerintegrator import EulerIntegrator

# spatial embeddings and computations
from .embedding import Embedding

# some sample figures
from .triangularlattice import TriangularLattice, TriangularLatticeEmbedding
#from .toroidallattice import ToroidalLattice

# file I/O
from . import file

# drawing support
#import simplicial.drawing
#from simplicial.drawing import *
