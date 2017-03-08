# Tests of simplicial complex class
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
import copy
from simplicial import *

class SimplicialComplexTests(unittest.TestCase):

    def test0simplex( self ):
        '''Test the creation of a single 0-simplex complex.'''
        c = SimplicialComplex()
        c.addSimplex(id = 0)
        self.assertItemsEqual(c.simplices(), [ 0 ])
        self.assertEqual(c.order(0), 0)
        os = c.numberOfSimplicesOfOrder()
        self.assertItemsEqual(os, [ 0 ])
        self.assertEqual(os[0], 1)
        self.assertEqual(c.simplicesOfOrder(0), [ 0 ])
        self.assertEqual(c.maxOrder(), 0)
        self.assertEqual(c.eulerCharacteristic(), 1)
        
    def test1simplex( self ):
        '''Test the creation of a single 1-simplex complex.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        self.assertItemsEqual(c.simplices(), [ 1, 2, 12 ])
        self.assertEqual(c.order(1), 0)
        self.assertEqual(c.order(2), 0)
        self.assertEqual(c.order(12), 1)
        os = c.numberOfSimplicesOfOrder()
        self.assertItemsEqual(os, [ 0, 1 ])
        self.assertEqual(os[0], 2)
        self.assertEqual(c.simplicesOfOrder(0), [ 1, 2 ])
        self.assertEqual(os[1], 1)
        self.assertEqual(c.simplicesOfOrder(1), [ 12 ])
        self.assertEqual(c.faces(12), [ 1, 2 ])
        self.assertEqual(c.maxOrder(), 1)
        self.assertEqual(c.eulerCharacteristic(), 1)
        
    def test2simplex( self ):
        '''Test the creation of a single 2-simplex complex.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ]) 
        self.assertItemsEqual(c.simplices(), [ 1, 2, 3, 12, 13, 23, 123 ])
        self.assertEqual(c.order(1), 0)
        self.assertEqual(c.order(2), 0)
        self.assertEqual(c.order(3), 0)
        self.assertEqual(c.order(12), 1)
        self.assertEqual(c.order(13), 1)
        self.assertEqual(c.order(23), 1)
        self.assertEqual(c.order(123), 2)
        os = c.numberOfSimplicesOfOrder()
        self.assertItemsEqual(os, [ 0, 1, 2 ])
        self.assertEqual(os[0], 3)
        self.assertEqual(c.simplicesOfOrder(0), [ 1, 2, 3 ])
        self.assertEqual(os[1], 3)
        self.assertEqual(c.simplicesOfOrder(1), [ 12, 13, 23 ])
        self.assertEqual(c.faces(12), [ 1, 2 ])
        self.assertEqual(os[2], 1)
        self.assertEqual(c.simplicesOfOrder(2), [ 123 ])
        self.assertEqual(c.maxOrder(), 2)
        self.assertEqual(c.eulerCharacteristic(), 1)

    def testOneFace( self ):
        '''Test that we fail if we try to ad a simplex with a single face.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        with self.assertRaises(Exception):
            c.addSimplex(id = 2, fs = [ 1 ])

    def testName( self ):
        '''Test we get the name of a simplex back.'''
        c = SimplicialComplex()
        n = c.addSimplex(id = 1)
        self.assertEqual(n, 1)

    def testNameGeneration( self ):
        '''Test we generate unique simplex names correctly.'''
        c = SimplicialComplex()
        n = c.addSimplex()
        self.assertIn(n, c.simplices())
        self.assertEqual(len(c.simplices()), 1)

    def testCopy( self ):
        '''Test copying simplices from one complex to another.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        d = SimplicialComplex()
        d.addSimplex(id = 4)
        d.addSimplex(id = 5)
        d.addSimplex(id = 6)
        d.addSimplex(id = 45, fs = [ 4, 5 ]) 
        d.addSimplex(id = 46, fs = [ 4, 6 ]) 
        d.addSimplex(id = 56, fs = [ 5, 6 ]) 
        d.addSimplex(id = 456, fs = [ 45, 46, 56 ])

        c.addSimplicesFrom(d)
        self.assertItemsEqual(c.simplices(),
                              [ 1, 2, 3, 4, 5, 6,
                                12, 13, 23, 45, 46, 56,
                                123, 456 ])

    def testCopyRename( self ):
        '''Test copying simplices from one complex to another, with a renaming
        mapping for the simplices.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        d = SimplicialComplex()
        d.addSimplex(id = 1)    # these will collide unless renamed
        d.addSimplex(id = 2)
        d.addSimplex(id = 3)
        d.addSimplex(id = 4, fs = [ 1, 2 ]) 
        d.addSimplex(id = 5, fs = [ 1, 3 ]) 
        d.addSimplex(id = 6, fs = [ 2, 3 ]) 
        d.addSimplex(id = 7, fs = [ 4, 5, 6 ])

        c.addSimplicesFrom(d, rename = lambda s: s + 1000)
        self.assertItemsEqual(c.simplices(),
                              [ 1, 2, 3, 1001, 1002, 1003,
                                12, 13, 23, 1004, 1005, 1006,
                                123, 1007 ])
        self.assertItemsEqual(c.faces(1004), [ 1001, 1002 ])
        self.assertItemsEqual(c.faces(1007), [ 1004, 1005, 1006 ])
        
    def testOrderViolation( self ):
        '''Test that we throw an exception if we try to add a face with the wrong order.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        with self.assertRaises(Exception):
            c.addSimplex(id = bad1, fs = [ 2, 13 ])
        with self.assertRaises(Exception):
            c.addSimplex(id = bad2, fs = [ 13 ])
        with self.assertRaises(Exception):
            c.addSimplex(id = bad3, fs = [ 1, 2, 3 ])
        
    def testDuplicateSimplices( self ):
        '''Test that we fail if we try to add a duplicate simplex.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        with self.assertRaises(Exception):
            c.addSimplex(id = 1)
        with self.assertRaises(Exception):
            c.addSimplex(id = 1, fs = [ 1, 2 ])

    def testCanonical( self ):
        '''Test we can pull out simplices in a canonical order.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ]) 
        self.assertEqual(c.faces(123), [ 12, 13, 23 ])

    def testClosure( self ):
        '''Test that we correctly form the closures of various simplices'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ]) 
        self.assertItemsEqual(c.closureOf(1), [ 1 ])
        self.assertItemsEqual(c.closureOf(2), [ 2 ])
        self.assertItemsEqual(c.closureOf(3), [ 3 ])
        self.assertItemsEqual(c.closureOf(12), [ 1, 2, 12 ])
        self.assertItemsEqual(c.closureOf(13), [ 1, 3, 13 ])
        self.assertItemsEqual(c.closureOf(23), [ 2, 3, 23 ])
        self.assertItemsEqual(c.closureOf(123), [ 1, 2, 3, 12, 13, 23, 123 ])

    def testPart( self ):
        '''Test that we correctly form the part-of (co-closure) of various simplices'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        self.assertItemsEqual(c.partOf(1), [ 1, 12, 13, 123 ])
        self.assertItemsEqual(c.partOf(2), [ 2, 23, 12, 123 ])
        self.assertItemsEqual(c.partOf(3), [ 3, 13, 23, 123 ])
        self.assertItemsEqual(c.partOf(12), [ 12, 123 ])
        self.assertItemsEqual(c.partOf(13), [ 13, 123 ])
        self.assertItemsEqual(c.partOf(23), [ 23, 123 ])
        self.assertItemsEqual(c.partOf(123), [ 123 ])

    def testBasis( self ):
        '''Test that we correctly form the basis of various simplices'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        self.assertItemsEqual(c.basisOf(123), [ 1, 2, 3 ])
        self.assertItemsEqual(c.basisOf(12), [ 1, 2 ])
        self.assertItemsEqual(c.basisOf(13), [ 1, 3 ])
        self.assertItemsEqual(c.basisOf(23), [ 2, 3 ])
        self.assertItemsEqual(c.basisOf(1), [ 1 ])
        self.assertItemsEqual(c.basisOf(2), [ 2 ])
        self.assertItemsEqual(c.basisOf(3), [ 3 ])

    def testRestrictBasis( self ):
        '''Test that we correctly restrict the basis of a complex to the right sub-space.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        cprime = copy.deepcopy(c)
        cprime.restrictBasisTo([ 1 ])
        self.assertItemsEqual(cprime.simplices(), [ 1 ])

        cprime = copy.deepcopy(c)
        cprime.restrictBasisTo([ 1, 2 ])
        self.assertItemsEqual(cprime.simplices(), [ 1, 2, 12 ])

        cprime = copy.deepcopy(c)
        cprime.restrictBasisTo([ 1, 2, 3 ])
        self.assertItemsEqual(cprime.simplices(), c.simplices())

    def testRestrictBasisIsBasis( self ):
        '''Test that we correctly require a basis to be 0-simplices.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        cprime = copy.deepcopy(c)
        with self.assertRaises(Exception):
            cprime.restrictBasisTo([ 12 ])

    def testEuler1hole( self ):
        '''Test that the Euler characteristic for a simplex with an unfilled triangle.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.addSimplex(id = 4)
        c.addSimplex(id = 24, fs = [ 2, 4 ]) 
        c.addSimplex(id = 34, fs = [ 3, 4 ])
        self.assertEqual(c.eulerCharacteristic(), 0)

        c.addSimplex(id = 234, fs = [ 24, 34, 23 ])
        self.assertEqual(c.eulerCharacteristic(), 1)
        
    def testEuler2islands( self ):
        '''Test that the Euler characteristic for a simplex with two unconnected triangles.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.addSimplex(id = 4)
        c.addSimplex(id = 5)
        c.addSimplex(id = 6)
        c.addSimplex(id = 45, fs = [ 4, 5 ]) 
        c.addSimplex(id = 46, fs = [ 4, 6 ]) 
        c.addSimplex(id = 56, fs = [ 5, 6 ]) 
        c.addSimplex(id = 456, fs = [ 45, 46, 56 ])
        self.assertEqual(c.eulerCharacteristic(), 2)

        c.addSimplex(id = 14, fs = [ 1, 4 ]) 
        self.assertEqual(c.eulerCharacteristic(), 1)


        
