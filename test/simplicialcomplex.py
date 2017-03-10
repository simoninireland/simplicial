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
        self.assertItemsEqual(c.simplicesOfOrder(0), [ 0 ])
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
        self.assertItemsEqual(c.simplicesOfOrder(0), [ 1, 2 ])
        self.assertEqual(os[1], 1)
        self.assertItemsEqual(c.simplicesOfOrder(1), [ 12 ])
        self.assertItemsEqual(c.faces(12), [ 1, 2 ])
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
        self.assertItemsEqual(c.simplicesOfOrder(0), [ 1, 2, 3 ])
        self.assertEqual(os[1], 3)
        self.assertItemsEqual(c.simplicesOfOrder(1), [ 12, 13, 23 ])
        self.assertItemsEqual(c.faces(12), [ 1, 2 ])
        self.assertEqual(os[2], 1)
        self.assertItemsEqual(c.simplicesOfOrder(2), [ 123 ])
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

    def testCopyRenameFunction( self ):
        '''Test copying simplices from one complex to another, with a renaming
        function for the simplices.'''
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
        
    def testCopyRenameMap( self ):
        '''Test copying simplices from one complex to another, with a renaming
        map for the simplices.'''
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

        r = dict()
        for i in xrange(1, 8):
            r[i] = i + 1000
        c.addSimplicesFrom(d, rename = r)
        self.assertItemsEqual(c.simplices(),
                              [ 1, 2, 3, 1001, 1002, 1003,
                                12, 13, 23, 1004, 1005, 1006,
                                123, 1007 ])
        self.assertItemsEqual(c.faces(1004), [ 1001, 1002 ])
        self.assertItemsEqual(c.faces(1007), [ 1004, 1005, 1006 ])

    def testAddWithBasis0New( self ):
        '''Check adding a 0-simplex.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis([ 1 ])
        self.assertEqual(len(c.simplicesOfOrder(0)), 1)

    def testAddWithBasis1AllExist( self ):
        '''Check adding a 1-simplex by its basis, where all the basis simplices exist.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplexWithBasis([ 1, 2 ])
        self.assertEqual(len(c.simplicesOfOrder(1)), 1)

    def testAddWithBasis1NoneExist( self ):
        '''Check adding a 1-simplex by its basis, where none of the basis simplices exist.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis([ 1, 2 ])
        self.assertItemsEqual(c.simplicesOfOrder(0), [ 1, 2 ])
        self.assertEqual(len(c.simplicesOfOrder(1)), 1)

    def testAddWithBasis1AllExistNamed( self ):
        '''Check adding a named 1-simplex by its basis, where all the basis simplices exist.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplexWithBasis([ 1, 2 ], id = 'line')
        self.assertItemsEqual(c.simplices(), [ 1, 2, 'line' ])

    def testAddWithBasis1Duplicate( self ):
        '''Check adding a 1-simplex by its basis where a simplex like this already exists.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex([ 1, 2 ])
        c.addSimplexWithBasis([ 1, 2 ])
        self.assertEqual(len(c.simplicesOfOrder(0)), 2)
        self.assertEqual(len(c.simplicesOfOrder(1)), 1)

    def testAddWithBasis2Exist( self ):
        '''Check adding a 2-simplex by its basis, where all the basis simplices exist.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplexWithBasis([ 1, 2, 3])
        self.assertItemsEqual(c.simplicesOfOrder(0), [ 1, 2, 3 ])
        self.assertItemsEqual(c.simplicesOfOrder(1), [ 12, 13, 23 ])
        self.assertEqual(len(c.simplicesOfOrder(2)), 1)
        
    def testAddWithBasis2ExistNamesMatch( self ):
        '''Check adding a named 2-simplex by its basis when it already exists with that name.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 'tri', fs = [ 12, 23, 13 ])
        c.addSimplexWithBasis([ 1, 2, 3], id = 'tri')
        self.assertItemsEqual(c.simplicesOfOrder(0), [ 1, 2, 3 ])
        self.assertItemsEqual(c.simplicesOfOrder(1), [ 12, 13, 23 ])
        self.assertItemsEqual(c.simplicesOfOrder(2), [ 'tri' ])
        
    def testAddWithBasis2ExistNamesDontMatch( self ):
        '''Check adding a named 2-simplex by its basis when it already exists with a different name.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        with self.assertRaises(Exception):
            c.addSimplexWithBasis([ 1, 2, 3], id = 'tri')

    def testAddSimplexOrder0( self ):
        ''' Test we can create a new simplex of order 0.'''
        c = SimplicialComplex()
        s = c.addSimplexOfOrder(0)
        self.assertItemsEqual(c.simplices(), [ s ])
        self.assertItemsEqual(c.simplicesOfOrder(0), [ s ])

    def testAddSimplexOrder0Named( self ):
        ''' Test we can create a named new simplex of order 0.'''
        c = SimplicialComplex()
        s = c.addSimplexOfOrder(0, id = 'point')
        self.assertEqual(s, 'point')
        self.assertItemsEqual(c.simplices(), [ s ])
        self.assertItemsEqual(c.simplicesOfOrder(0), [ s ])

    def testAddSimplexOrder0NamedDontMatch( self ):
        ''' Test we can create a named new simplex of order 0 when there's
        already a different-order simplex with that name.'''
        c = SimplicialComplex()
        c.addSimplexOfOrder(2, id = 'point')
        with self.assertRaises(Exception):
            c.addSimplexOfOrder(0, id = 'point')

    def testAddSimplexOrder1( self ):
        ''' Test we can create a new simplex of order 1.'''
        c = SimplicialComplex()
        s = c.addSimplexOfOrder(1)
        self.assertEqual(len(c.simplicesOfOrder(0)), 2)
        self.assertEqual(len(c.simplices()), 3)
        self.assertItemsEqual(c.simplicesOfOrder(1), [ s ])

    def testAddSimplexOrder1Named( self ):
        ''' Test we can create a named new simplex of order 1.'''
        c = SimplicialComplex()
        s = c.addSimplexOfOrder(1, id = 'line')
        self.assertEqual(s, 'line')
        self.assertEqual(len(c.simplicesOfOrder(0)), 2)
        self.assertEqual(len(c.simplices()), 3)
        self.assertItemsEqual(c.simplicesOfOrder(1), [ s ])

    def testRelabelFunction( self ):
        '''Test relabelling with a function.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        ns = c.relabel(lambda s: s + 1000)
        self.assertItemsEqual(ns, [ 1001, 1002, 1003,
                                    1012, 1013, 1023,
                                    1123 ])
        self.assertItemsEqual(ns, c.simplices())
        self.assertItemsEqual(c.faces(1123), [ 1012, 1013, 1023 ])
        self.assertItemsEqual(c.faces(1012), [ 1001, 1002 ])
        self.assertItemsEqual(c.faces(1013), [ 1001, 1003 ])
        self.assertItemsEqual(c.faces(1023), [ 1002, 1003 ])
        self.assertItemsEqual(c.partOf(1001), [ 1001, 1012, 1013, 1123 ])
        self.assertItemsEqual(c.partOf(1002), [ 1002, 1012, 1023, 1123 ])
        self.assertItemsEqual(c.partOf(1003), [ 1003, 1013, 1023, 1123 ])
                              
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
        self.assertItemsEqual(c.faces(123), [ 12, 13, 23 ])

    def testSelectByBasis( self ):
        '''Test retrieving a simplex by its basis.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 24, fs = [ 2, 4 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ]) 
        self.assertEqual(c.simplexWithBasis([ 1, 2 ]), 12)
        self.assertEqual(c.simplexWithBasis([ 3, 1, 2 ]), 123)
        self.assertIsNone(c.simplexWithBasis([ 4, 1, 2 ]))
        self.assertEqual(c.simplexWithBasis([ 4, 2 ]), 24)
        self.assertEqual(c.simplexWithBasis([ 4 ]), 4)
        with self.assertRaises(Exception):
            c.simplexWithBasis([ 1, 2, 12 ])
            
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

    def testDisjoint( self ):
        '''Test we can detect disjoint simplices.'''
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
        self.assertTrue(c.disjoint([1, 2]))
        self.assertTrue(c.disjoint([1, 23]))
        self.assertTrue(c.disjoint([12, 45]))
        self.assertTrue(c.disjoint([4, 123]))
        self.assertFalse(c.disjoint([1, 1]))
        self.assertFalse(c.disjoint([1, 123]))
        self.assertFalse(c.disjoint([1, 13]))
        self.assertTrue(c.disjoint([456, 123]))
        
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
        print cprime.simplices()
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

    def testDelete1( self ):
        '''Test that we correctly delete a single simplex.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.deleteSimplex(123)
        self.assertItemsEqual(c.simplicesOfOrder(2), [])
        self.assertItemsEqual(c.simplicesOfOrder(1), [ 12, 13, 23 ])
        self.assertItemsEqual(c.simplicesOfOrder(0), [ 1, 2, 3])

    def testDeleteWithParts( self ):
        '''Test that we correctly cascade deletion to all the simplices
        that the requested simplex is part of.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.deleteSimplex(12)
        self.assertItemsEqual(c.simplicesOfOrder(2), [])
        self.assertItemsEqual(c.simplicesOfOrder(1), [ 13, 23 ])
        self.assertItemsEqual(c.simplicesOfOrder(0), [ 1, 2, 3])

    def testOrdering( self ):
        '''Test that we can order simplices in order of order.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        ios = c.simplices()
        for i in xrange(len(ios) - 1):
            self.assertTrue(c.order(ios[i]) <= c.order(ios[i + 1]))
        dos = c.simplices(reverse = True)
        for i in xrange(len(dos) - 1):
            self.assertTrue(c.order(dos[i]) >= c.order(dos[i + 1]))

    def testDeleteWithFaces( self ):
        '''Test that we correctly delete face list elements.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.deleteSimplex(12)
        self.assertItemsEqual(c.partOf(1), [ 1, 13 ])

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


        
