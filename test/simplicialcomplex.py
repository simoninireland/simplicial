# Tests of simplicial complex class
#
# Copyright (C) 2014-2017 Simon Dobson
# 
# This file is part of Complex networks, complex processes (CNCP).
#
# CNCP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CNCP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CNCP. If not, see <http://www.gnu.org/licenses/gpl.html>.

import unittest
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
        
    def testDimplucateSimplices( self ):
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
