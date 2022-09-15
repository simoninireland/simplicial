# Tests of generators
#
# Copyright (C) 2017--2020 Simon Dobson
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


class GeneratorTests(unittest.TestCase):

    def testSkeleton1simplex(self):
        '''Test construction of a 1-simplex skeleton (a line).'''
        c = k_skeleton(1)
        ns = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(ns), 2)
        self.assertTrue(ns[0], 2)
        self.assertTrue(ns[1], 1)

    def testSkeleton2simplex(self):
        '''Test construction of a 2-simplex skeleton (a triangle).'''
        c = k_skeleton(2)
        ns = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(ns), 2)
        self.assertTrue(ns[0], 3)
        self.assertTrue(ns[1], 3)

    def testSkeletonLargeSimplex(self):
        '''Build the skeleton of a high-dimensional simplex, mainly as a soak test.'''
        c = k_skeleton(10)
        ns = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(ns), 2)

    def test1simplex(self):
        '''Test construction of a 1-simplex (a line).'''
        c = k_simplex(1)
        ns = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(ns), 2)
        self.assertTrue(ns[0], 2)
        self.assertTrue(ns[1], 1)

    def test2simplex(self):
        '''Test construction of a 2-simplex (a filled triangle).'''
        c = k_simplex(2)
        ns = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(ns), 3)
        self.assertTrue(ns[0], 3)
        self.assertTrue(ns[1], 3)
        self.assertTrue(ns[2], 1)

    def testLargeSimplex(self):
        '''Test construction of a high-dimensional simplex, mainly as a soak test.'''
        c = k_simplex(10)
        ns = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(ns), 11)

    def test2void(self):
        '''Test construction of a 2-void (an empty tetrahedron).'''
        c = k_void(2)
        ns = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(ns), 3)
        self.assertTrue(ns[0], 4)
        self.assertTrue(ns[1], 6)
        self.assertTrue(ns[2], 4)

    def testTwoVoids(self):
        '''Test we can create two voids.'''
        c = SimplicialComplex()
        c0 = k_simplex(4, c=c)
        c1 = k_void(2, c=c)
        c2 = k_void(2, c=c)

        self.assertEqual(c, c0)
        self.assertEqual(c, c1)
        self.assertEqual(c, c1)

    def testRing(self):
        '''Test the construction of a ring.'''
        c = ring(10)
        ns = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(ns), 2)
        self.assertTrue(ns[0], 10)
        self.assertTrue(ns[1], 10)
        betti = c.bettiNumbers([0, 1])
        self.assertTrue(betti[0], 1)
        self.assertTrue(betti[1], 1)


if __name__ == '__main__':
    unittest.main()
