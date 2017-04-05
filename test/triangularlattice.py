# Tests of triangular lattices
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

import unittest
from simplicial import *

class TriangularLatticeTests(unittest.TestCase):

    def _simplexCounts( self, r, c ):
        '''Check we have the right numbers of simplices.'''
        self._complex = TriangularLattice(r, c)

        # compute numbers of odd and even rows, for computing simplex totals
        nevenr = (r - 1) / 2
        noddr = nevenr
        if (r - 1) % 2 != 0:
            noddr = noddr + 1
        neventri = (r - 2) / 2
        noddtri = neventri
        if (r - 2) % 2 != 0:
            noddtri = noddtri + 1

        ns = self._complex.numberOfSimplicesOfOrder()
        self.assertEquals(ns[0], r * c) 
        self.assertEquals(ns[1], (r - 2) * c +            # NS
                                 (r - 1) * c - nevenr +   # SW
                                 (r - 1) * c - noddr)     # SE
        self.assertEquals(ns[2], (r - 2) * c - neventri + # SW
                                 (r - 2) * c - noddtri)   # SE

    def testEvenEven( self ):
        '''Test a lattice with even rows and columns.'''
        self._simplexCounts(10, 10)

    def testEvenOdd( self ):
        '''Test a lattice with even rows and odd columns.'''
        self._simplexCounts(10, 11)

    def testOddEven( self ):
        '''Test a lattice with odd rows and even columns.'''
        self._simplexCounts(11, 10)

    def testOddOdd( self ):
        '''Test a lattice with odd rows and columns.'''
        self._simplexCounts(11, 10)

    def testEuler( self ):
        '''Test the Euler characteristic calculations.'''
        self._complex = TriangularLattice(20, 20)
        self.assertEqual(self._complex.eulerCharacteristic(), 1)

