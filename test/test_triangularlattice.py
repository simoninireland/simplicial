# Tests of triangular lattices
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

import unittest
import six
from simplicial import *
import math
import numpy.random

class TriangularLatticeTests(unittest.TestCase):

    def _simplexCounts( self, r, c ):
        """Check we have the right numbers of simplices."""
        self._complex = TriangularLattice(r, c)

        ntriperr = 2 * (c - 1) + 1

        ns = self._complex.numberOfSimplicesOfOrder()
        self.assertEqual(ns[0], r * c)
        if len(ns) > 1:
            self.assertEqual(ns[1], (r - 1) * (2 * c - 1) + (r - 2) * c)
        if len(ns) > 2:
            self.assertEqual(ns[2], (r - 2) * ntriperr)

    def testSimplest(self):
        """Test simplest triangular lattice."""
        self._simplexCounts(2, 2)

    def testNextSimplest(self):
        """Test the next simplest lattice."""
        self._simplexCounts(3, 3)

    def testEvenEven( self ):
        """Test a lattice with even rows and columns."""
        self._simplexCounts(10, 10)

    def testEvenOdd( self ):
        """Test a lattice with even rows and odd columns."""
        self._simplexCounts(10, 11)

    def testOddEven( self ):
        """Test a lattice with odd rows and even columns."""
        self._simplexCounts(11, 10)

    def testOddOdd( self ):
        """Test a lattice with odd rows and columns."""
        self._simplexCounts(11, 10)

    def testEuler( self ):
        """Test the Euler characteristic calculations."""
        self._complex = TriangularLattice(20, 20)
        self.assertEqual(self._complex.eulerCharacteristic(), 1)

    def testRegularEmbedding( self ):
        """Test that the embedding is regular."""
        self._complex = TriangularLattice(10, 10)
        e = TriangularLatticeEmbedding(self._complex, 11, 11)
        pos = e.positionsOf()
        eps = 0.0001

        # all columns equidistant
        for i in range(10):
            for j in range(9):
                s1 = self._complex._indexOfVertex(i, j)
                s2 = self._complex._indexOfVertex(i, j + 1)
                self.assertTrue(pos[s2][0] - pos[s1][0] < (11.0 / 10) + eps)

        # all rows equidistant
        for i in range(9):
            for j in range(10):
                s1 = self._complex._indexOfVertex(i, j)
                s2 = self._complex._indexOfVertex(i + 1, j)
                self.assertTrue(pos[s2][1] - pos[s1][1] < (11.0 / 10) + eps)

        # odd rows are offset
        for i in range(9):
            for j in range(9):
                s1 = self._complex._indexOfVertex(i, j)
                s2 = self._complex._indexOfVertex(i + 1, j)
                if i % 2 == 0:
                    self.assertTrue(pos[s2][0] > pos[s1][0])
                else:
                    self.assertTrue(pos[s2][0] < pos[s1][0])

    def testPerturbedEmbedding( self ):
        """Test that we can perturb the embedding with explicit new positions."""
        self._complex = TriangularLattice(10, 10)
        e = TriangularLatticeEmbedding(self._complex, 11, 11)
        ss = list(self._complex.simplicesOfOrder(0))
        pos = e.positionsOf()

        # choose a random simplex
        i = int(numpy.random.random() * len(ss))
        s = ss[i]

        # re-position simplex
        e.positionSimplex(s, [ 12, 13 ])

        # make sure position is preserved
        pos1 = e.positionsOf()
        six.assertCountEqual(self, pos1[s], [ 12, 13 ])
