# Base class for simplical complex representations
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

import numpy
from typing import List, Set
from simplicial import Simplex, Attributes

# There is a circular import between SimplicialComplex and
# SimplicialComplexRepresentation at the typing level (but not at the execution
# level) (See https://www.stefaanlippens.net/circular-imports-type-hints-python.html)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simplicial import SimplicialComplex


class Representation:
    '''The base class for implementations of simplicial complexes.

    This class defines the interface to be implemented by representations,
    plus some housekeeping functions.

    :param c: the complex we're representing
    '''

    # ---------- Initialisation and helpers ----------

    def __init__(self):
        self._complex: 'SimplicialComplex' = None                        # the complex we-re representing

    def setComplex(self, c: 'SimplicialComplex'):
        '''Set the complex we're representing. This allows the representation
        to make use of the complex's more flexible operations if required.

        :param c: the complex'''
        self._complex = c


    # ---------- Core interface ----------

    def newSimplex(self, d: int) -> str:
        """Generate a new unique identifier for a simplex.

        :param d: dimension of the simplex to be identified
        :returns: an identifier not currently used in the complex"""
        raise NotImplementedError('newSimplex')

    def addSimplex(self, fs: List[Simplex], id: Simplex, attr: Attributes):

        """Add a simplex to the complex whose faces are the elements
        of fs.

        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) name for the simplex
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex

        """
        raise NotImplementedError('addSimplex')

    def relabelSimplex(self, s: Simplex, q: Simplex):
        '''Relabel a simplex.

        :param s: the simplex to rename
        :param q: the new name'''
        raise NotImplementedError('relabelSimplex')

    def forceDeleteSimplex(self, s: Simplex):
        """Delete a simplex without sanity checks.

        :param s: the simplex"""
        raise NotImplementedError('forceDeleteSimplex')

    def orderOf(self, s: Simplex) -> int:
        """Return the order of a simplex.

        :param s: the simplex
        :returns: the order of the simplex"""
        raise NotImplementedError('orderOf')

    def indexOf(self, s: Simplex) -> int:
        """Return the inmdex of a simplex.

        :param s: the simplex
        :returns: an index"""
        raise NotImplementedError('indexOf')

    def basisOf(self, s: Simplex) -> Set[Simplex]:
        """Return the basis of a simplex.

        :param s: the simplex
        :returns: the set of 0-simplices that form the basis of s"""
        raise NotImplementedError('basisOf')

    def maxOrder(self) -> int:
        """Return the largest order of simplices in the complex.

        :returns: the largest order that contains at least one simplex, or -1"""
        raise NotImplementedError('maxOrder')

    def simplices(self, reverse: bool) -> List[Simplex]:
        """Return all the simplices in the complex, in order: the
        low orders first (unless reverse is True), and in canonical
        order within each order.

        :param reverse: (optional) reverse the sort order if True
        :returns: a list of simplices"""
        raise NotImplementedError('simplices')

    def simplicesOfOrder(self, k: int) -> List[Simplex]:
        """Return all the simplices of the given order.
        The simplices are returned in "canonical" order, meaning the order
        they appear in the boiundary operator matrices.

        :param k: the desired order
        :returns: a set of simplices, which may be empty"""
        raise NotImplementedError('simplicesOfOrder')

    def containsSimplex(self, s: Simplex) -> bool:
        """Test whether the complex contains the given simplex.

        :param s: the simplex
        :returns: True if the simplex is in the complex"""
        raise NotImplementedError('containsSimplex')

    def getAttributes(self, s: Simplex) -> Attributes:
        """Return the attributes associated with the given simplex.

        :param s: the simplex
        :returns: a dict of attributes"""
        raise NotImplementedError('getAttributes')

    def setAttributes(self, s: Simplex, attr: Attributes):
        """Set the attributes associated with a simplex.

        :param s: the simplex
        :param attr: a dict of attributes"""
        raise NotImplementedError('setAttributes')

    def faces(self, s: Simplex) -> Set[Simplex]:
        """Return the faces of a simplex.

        :param s: the simplex
        :returns: a set of faces"""
        raise NotImplementedError('faces')

    def cofaces(self, s: Simplex) -> Set[Simplex]:
        '''Return the simplices the given simnplex is a face of.

        :param s: the simplex
        :returns: a list of simplices'''
        raise NotImplementedError('cofaces')

    def boundaryOperator(self, k: int) -> numpy.ndarray:
        """Return the boundary operator of the k-simplices.

        :param k: the order of simplices
        :returns: the boundary matrix

        """
        raise NotImplementedError('boundaryOperator')
