# Tests of simplicial complex class
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
import copy
from simplicial import *

class SimplicialComplexTests(unittest.TestCase):

    def _checkIntegrity( self, c ):
        """Check the integrity of the complex, making sure that all faces of
        all higher simplices are contained in the complex."""
        kmax = c.maxOrder()

        # run through simplices from highest order downwards, checking faces
        for k in range(kmax, 0, -1):
            ss = c.simplicesOfOrder(k)
            for s in ss:
                # check that the simplex has all its faces
                fs = c.faces(s)
                if len(fs) != k + 1:
                    # not enough faces
                    raise Exception('Simplex {s} needs {nf} faces, got {lf}'.format(s = s,
                                                                                    nf = k + 1,
                                                                                    lf = len(fs)))
                for f in fs:
                    # check all the faces exist in the complex
                    if f not in c.simplices():
                        # a face that's not a simplex
                        raise Exception('Simplex {s} has a face {f} that isn\'t in the complex'.format(s = s,
                                                                                                        f = f))

        # run up simplices from lowest order up, checking parts membership
        for k in range(kmax + 1):
            ss = c.simplicesOfOrder(k)
            for s in ss:
                # extract all the simplices we're part of
                ps = c.partOf(s, exclude_self = True)
                for p in ps:
                    # make sure we're a a face of every simplx we're part of
                    if s not in c.faces(p):
                        # we're part of something we're not a face of
                        raise Exception('Simplex {s} is part of {p} but not a face of it'.format(s = s,
                                                                                                 p = p))
                

    def test0simplex( self ):
        """Test the creation of a single 0-simplex complex."""
        c = SimplicialComplex()
        c.addSimplex(id = 0)
        six.assertCountEqual(self, c.simplices(), [ 0 ])
        self.assertEqual(c.orderOf(0), 0)
        os = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(os), 1)
        self.assertEqual(os[0], 1)
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 0 ])
        self.assertEqual(c.maxOrder(), 0)
        self.assertEqual(c.eulerCharacteristic(), 1)
        
    def test1simplex( self ):
        """Test the creation of a single 1-simplex complex."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        six.assertCountEqual(self, c.simplices(), [ 1, 2, 12 ])
        self.assertEqual(c.orderOf(1), 0)
        self.assertEqual(c.orderOf(2), 0)
        self.assertEqual(c.orderOf(12), 1)
        os = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(os), 2)
        self.assertEqual(os[0], 2)
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2 ])
        self.assertEqual(os[1], 1)
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 12 ])
        six.assertCountEqual(self, c.faces(12), [ 1, 2 ])
        self.assertEqual(c.maxOrder(), 1)
        self.assertEqual(c.eulerCharacteristic(), 1)
        
    def test2simplex( self ):
        """Test the creation of a single 2-simplex complex."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ]) 
        six.assertCountEqual(self, c.simplices(), [ 1, 2, 3, 12, 13, 23, 123 ])
        self.assertEqual(c.orderOf(1), 0)
        self.assertEqual(c.orderOf(2), 0)
        self.assertEqual(c.orderOf(3), 0)
        self.assertEqual(c.orderOf(12), 1)
        self.assertEqual(c.orderOf(13), 1)
        self.assertEqual(c.orderOf(23), 1)
        self.assertEqual(c.orderOf(123), 2)
        os = c.numberOfSimplicesOfOrder()
        self.assertEqual(len(os), 3)
        self.assertEqual(os[0], 3)
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2, 3 ])
        self.assertEqual(os[1], 3)
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 12, 13, 23 ])
        six.assertCountEqual(self, c.faces(12), [ 1, 2 ])
        self.assertEqual(os[2], 1)
        six.assertCountEqual(self, c.simplicesOfOrder(2), [ 123 ])
        self.assertEqual(c.maxOrder(), 2)
        self.assertEqual(c.eulerCharacteristic(), 1)

    def testSimplexOutOfOrder(self):
        """Test that we can't create simplex of too large an order."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        with self.assertRaises(Exception):
            c.addSimplex(fs = [ 1, 2, 3 ])

    def testOrder(self):
        """Test we can gtet simplex orders properly."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 13, fs = [ 1, 3 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        self.assertEqual(c.orderOf(1), 0)
        self.assertEqual(c.orderOf(12), 1)
        self.assertEqual(c.orderOf(123), 2)
        with self.assertRaises(Exception):
            c.orderOf(4)

    def testIndex(self):
        """Test we get unique indices."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 13, fs = [ 1, 3 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        for k in range(3):
            iis = set()
            ss = c.simplicesOfOrder(k)
            for s in ss:
                iis.add(c.indexOf(s))
            self.assertEqual(len(iis), len(ss))
        with self.assertRaises(Exception):
            c.indexOf(4)

    def testAttributes(self):
        """Test we can get and set individual simplex attributes."""
        c = SimplicialComplex()
        c.addSimplex(id = 1, attr = dict(test = 3))
        c.addSimplex(id = 2)
        self.assertDictEqual(c[1], dict(test = 3))
        self.assertDictEqual(c[2], dict())
        c[1]['test2'] = 4
        self.assertDictEqual(c[1], dict(test = 3, test2 = 4))
        self.assertDictEqual(c[2], dict())
        c[1]['test'] = 4
        self.assertDictEqual(c[1], dict(test = 4, test2 = 4))
        self.assertDictEqual(c[2], dict())
        c[2]['test'] = 16
        self.assertDictEqual(c[1], dict(test = 4, test2 = 4))
        self.assertDictEqual(c[2], dict(test = 16))

    # add tests of boundary operators when we add and remove simplices
    # including when we add a simplex of order < maxk (add empty rows)
    
    def testOneFace( self ):
        """Test that we fail if we try to ad a simplex with a single face."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        with self.assertRaises(Exception):
            c.addSimplex(id = 2, fs = [ 1 ])

    def testDuplicateBasis( self ):
        """Test we can't add two simplices with the same basis."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        with self.assertRaises(Exception):
            c.addSimplex(id = 21, fs = [ 1, 2 ])

    def testName( self ):
        """Test we get the name of a simplex back."""
        c = SimplicialComplex()
        n = c.addSimplex(id = 1)
        self.assertEqual(n, 1)

    def testNameGeneration( self ):
        """Test we generate unique simplex names correctly."""
        c = SimplicialComplex()
        n = c.addSimplex()
        self.assertIn(n, c.simplices())
        self.assertEqual(len(c.simplices()), 1)

    def testCopy( self ):
        """Test copying simplices from one complex to another."""
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
        six.assertCountEqual(self, c.simplices(),
                              [ 1, 2, 3, 4, 5, 6,
                                12, 13, 23, 45, 46, 56,
                                123, 456 ])

    def testCopyRenameCollision( self ):
        """Test that we fail if we try to re-use a simplex name when copying."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        d = SimplicialComplex()
        d.addSimplex(id = 1)
        d.addSimplex(id = 5)
        d.addSimplex(id = 6)
        d.addSimplex(id = 15, fs = [ 1, 5 ]) 
        d.addSimplex(id = 16, fs = [ 1, 6 ]) 
        d.addSimplex(id = 56, fs = [ 5, 6 ]) 
        d.addSimplex(id = 156, fs = [ 15, 16, 56 ])

        with self.assertRaises(Exception):
            c.addSimplicesFrom(d)
        
    def testCopyRenameFunction( self ):
        """Test copying simplices from one complex to another, with a renaming
        function for the simplices."""
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
        six.assertCountEqual(self, c.simplices(),
                              [ 1, 2, 3, 1001, 1002, 1003,
                                12, 13, 23, 1004, 1005, 1006,
                                123, 1007 ])
        six.assertCountEqual(self, list(c.faces(1004)), [ 1001, 1002 ])
        six.assertCountEqual(self, list(c.faces(1007)), [ 1004, 1005, 1006 ])
        
    def testCopyRenameMap( self ):
        """Test copying simplices from one complex to another, with a renaming
        map for the simplices."""
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
        for i in range(1, 8):
            r[i] = i + 1000
        c.addSimplicesFrom(d, rename = r)
        six.assertCountEqual(self, c.simplices(),
                              [ 1, 2, 3, 1001, 1002, 1003,
                                12, 13, 23, 1004, 1005, 1006,
                                123, 1007 ])
        six.assertCountEqual(self, c.faces(1004), [ 1001, 1002 ])
        six.assertCountEqual(self, c.faces(1007), [ 1004, 1005, 1006 ])

    def testCopyRenameMapCollision( self ):
        """Test that we fail if we try to re-use a simplex name when copying and renaming."""
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

        r = dict()
        for i in range(1, 8):
            r[i] = i + 1000
        r[4] = 1
        with self.assertRaises(Exception):
            c.addSimplicesFrom(d, rename = r)

    def testIsBasis( self ):
        """Test we can correctly test for a basis."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        self.assertTrue(c.isBasis([]))
        self.assertTrue(c.isBasis([ 3 ]))
        self.assertTrue(c.isBasis([ 1, 2, 3 ]))
        self.assertFalse(c.isBasis([ 1, 23, 3 ]))
        with self.assertRaises(Exception):
            c.isBasis([ 123 ], fatal = True)
        self.assertFalse(c.isBasis([ 1, 2, 3, 4 ]))
        with self.assertRaises(Exception):
            c.isBasis([ 1, 2, 3, 4 ], fatal = True)

    def testEnsureBasis( self ):
        """Test we can correctly identify what is and isn't a basis."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.ensureBasis([ 1, 2, 3 ])
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.ensureBasis([ 1, 2, 3 ])
        with self.assertRaises(Exception):
            c.ensureBasis([ 1, 2, 12, 3 ])

    def testEnsureBasisAddSuccess( self ):
        """Test we can correctly create only the new simplices we need."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.ensureBasis([ 1, 4 ])
        six.assertCountEqual(self, c.simplices(), [ 1, 2, 3, 4 ])
        
    def testEnsureBasisAddWithAttributes( self ):
        """Test we add the same attributes to created simplices."""
        c = SimplicialComplex()
        c.addSimplex(id = 1, attr = dict(a = 1))
        c.addSimplex(id = 2, attr = dict(a = 2))
        c.addSimplex(id = 3, attr = dict(a = 3))
        c.ensureBasis([ 1, 4, 5 ], attr = dict(a = 10))
        six.assertCountEqual(self, c.simplices(), [ 1, 2, 3, 4, 5 ])
        self.assertEqual(c[1]['a'], 1)
        self.assertEqual(c[2]['a'], 2)
        self.assertEqual(c[3]['a'], 3)
        self.assertEqual(c[4]['a'], 10)
        self.assertEqual(c[5]['a'], 10)
        
    def testAddWithBasis0New( self ):
        """Check adding a 0-simplex."""
        c = SimplicialComplex()
        c.addSimplexWithBasis([ 1 ])
        self.assertEqual(len(c.simplicesOfOrder(0)), 1)

    def testAddWithBasis1AllExist( self ):
        """Check adding a 1-simplex by its basis, where all the basis simplices exist."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplexWithBasis([ 1, 2 ])

    def testAddWithBasis1NoneExist( self ):
        """Check adding a 1-simplex by its basis, where none of the basis simplices exist."""
        c = SimplicialComplex()
        c.addSimplexWithBasis([ 1, 2 ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2 ])
        self.assertEqual(len(c.simplicesOfOrder(1)), 1)

    def testAddWithBasis1AllExistNamed( self ):
        """Check adding a named 1-simplex by its basis, where all the basis simplices exist."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplexWithBasis([ 1, 2 ], id = 'line')
        six.assertCountEqual(self, c.simplices(), [ 1, 2, 'line' ])

    def testAddWithBasis2Exist( self ):
        """Check adding a 2-simplex by its basis, where all the basis simplices exist."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplexWithBasis([ 1, 2, 3])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2, 3 ])
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 12, 13, 23 ])
        self.assertEqual(len(c.simplicesOfOrder(2)), 1)
        
    def testAddWithBasis4( self ):
        """Check adding a 3-simplex to an empty complex"""
        c = SimplicialComplex()
        c.addSimplexWithBasis([ 1, 2, 3, 4 ])
        
        nos = c.numberOfSimplicesOfOrder()
        self.assertEqual(nos[0], 4)
        self.assertEqual(nos[1], 6)
        self.assertEqual(nos[2], 4)
        self.assertEqual(nos[3], 1)

        tri = c.simplicesOfOrder(3).pop()
        six.assertCountEqual(self, c.basisOf(tri), [ 1, 2, 3, 4 ])
                         
    def testAddWithBasis2Exists( self ):
        """Check adding a named 2-simplex by its basis when it already exists."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        with self.assertRaises(Exception):
            c.addSimplexWithBasis([ 1, 2, 3])

    def testAddSimplexOrder0( self ):
        """ Test we can create a new simplex of order 0."""
        c = SimplicialComplex()
        s = c.addSimplexOfOrder(0)
        six.assertCountEqual(self, c.simplices(), [ s ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ s ])

    def testAddSimplexOrder0Named( self ):
        """ Test we can create a named new simplex of order 0."""
        c = SimplicialComplex()
        s = c.addSimplexOfOrder(0, id = 'point')
        self.assertEqual(s, 'point')
        six.assertCountEqual(self, c.simplices(), [ s ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ s ])

    def testAddSimplexOrder0NamedDontMatch( self ):
        """ Test we can create a named new simplex of order 0 when there's
        already a different-order simplex with that name."""
        c = SimplicialComplex()
        c.addSimplexOfOrder(0, id = 'point')
        with self.assertRaises(Exception):
            c.addSimplexOfOrder(0, id = 'point')

    def testAddSimplexOrder1( self ):
        """ Test we can create a new simplex of order 1."""
        c = SimplicialComplex()
        s = c.addSimplexOfOrder(1)
        self.assertEqual(len(c.simplicesOfOrder(0)), 2)
        self.assertEqual(len(c.simplices()), 3)
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ s ])

    def testAddSimplexOrder1Named( self ):
        """ Test we can create a named new simplex of order 1."""
        c = SimplicialComplex()
        s = c.addSimplexOfOrder(1, id = 'line')
        self.assertEqual(s, 'line')
        self.assertEqual(len(c.simplicesOfOrder(0)), 2)
        self.assertEqual(len(c.simplices()), 3)
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ s ])

    def testSimplexWithFacesSuccess( self ):
        """Test we can retrieve a simplex from its faces."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 31, fs = [ 3, 1 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 31 ])
        self.assertEqual(c.simplexWithFaces([ 1, 2 ]), 12)
        self.assertEqual(c.simplexWithFaces([ 12, 31, 23 ]), 123)
        with self.assertRaises(Exception):
            self.assertEqual(c.simplexWithFaces([1, 2, 3]))

    def testSimplexWithFacesNoSimplex( self ):
        """Test we don't retrieve a simplex that isn't there."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 31, fs = [ 3, 1 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 31 ])
        self.assertEqual(c.simplexWithFaces([ 3, 4 ]), None)

    def testSimplicesInOrder(self):
        """Test we retrieve simplices in order of their order."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 31, fs = [ 3, 1 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 31 ])

        k = -1
        for s in c.simplices():
            sk = c.orderOf(s)
            if sk == k:
                # another one of the same order
                pass
            else:
                if sk == k + 1:
                    # order has increased, record the new order
                    k = sk
                else:
                    self.fail("Simplices not in order order")

    def testSimplicesInReverseOrder(self):
        """Test we retrieve simplices in reverse order of their order."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 31, fs = [ 3, 1 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 31 ])

        k = c.maxOrder() + 1
        for s in c.simplices(reverse = True):
            sk = c.orderOf(s)
            if sk == k:
                # another one of the same order
                pass
            else:
                if sk == k - 1:
                    # order has increased, record the new order
                    k = sk
                else:
                    self.fail("Simplices not in reverse-order order")

    def testContains(self):
        """Test we can check containment correctly."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 31, fs = [ 3, 1 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 31 ])
        for s in c.simplices():
            self.assertTrue(c.containsSimplex(s))
        self.assertFalse(c.containsSimplex(5))

    def testContainsBasis(self):
        """Test we can check containment of a basis correctly."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 31, fs = [ 3, 1 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 31 ])
        self.assertTrue(c.containsSimplexWithBasis([ 1, 2 ]))
        self.assertFalse(c.containsSimplexWithBasis([1, 4]))

    def testRelabelFunction( self ):
        """Test relabelling with a function."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        ns = c.relabel(lambda s: s + 1000)
        six.assertCountEqual(self, ns, [ 1001, 1002, 1003,
                                    1012, 1013, 1023,
                                    1123 ])
        six.assertCountEqual(self, ns, c.simplices())
        six.assertCountEqual(self, c.faces(1123), [ 1012, 1013, 1023 ])
        six.assertCountEqual(self, c.faces(1012), [ 1001, 1002 ])
        six.assertCountEqual(self, c.faces(1013), [ 1001, 1003 ])
        six.assertCountEqual(self, c.faces(1023), [ 1002, 1003 ])
        six.assertCountEqual(self, c.partOf(1001), [ 1001, 1012, 1013, 1123 ])
        six.assertCountEqual(self, c.partOf(1002), [ 1002, 1012, 1023, 1123 ])
        six.assertCountEqual(self, c.partOf(1003), [ 1003, 1013, 1023, 1123 ])

    def testRelabelMap( self ):
        """Test relabelling with a dict."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        rename = dict()
        for i in c.simplices():
            rename[i] = i + 1000
        ns = c.relabel(rename)
        six.assertCountEqual(self, ns, [ 1001, 1002, 1003,
                                    1012, 1013, 1023,
                                    1123 ])
        six.assertCountEqual(self, ns, c.simplices())
        six.assertCountEqual(self, c.faces(1123), [ 1012, 1013, 1023 ])
        six.assertCountEqual(self, c.faces(1012), [ 1001, 1002 ])
        six.assertCountEqual(self, c.faces(1013), [ 1001, 1003 ])
        six.assertCountEqual(self, c.faces(1023), [ 1002, 1003 ])
        six.assertCountEqual(self, c.partOf(1001), [ 1001, 1012, 1013, 1123 ])
        six.assertCountEqual(self, c.partOf(1002), [ 1002, 1012, 1023, 1123 ])
        six.assertCountEqual(self, c.partOf(1003), [ 1003, 1013, 1023, 1123 ])

    def testRelabelIncomplete( self ):
        """Test relabelling with a dict that doesn't cover all simplices."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        rename = dict()
        for i in c.simplices():
            rename[i] = i + 1000
        del rename[1]
        del rename[123]
        ns = c.relabel(rename)
        six.assertCountEqual(self, ns, [ 1, 1002, 1003,
                                    1012, 1013, 1023,
                                    123 ])
        six.assertCountEqual(self, ns, c.simplices())
        six.assertCountEqual(self, c.faces(123), [ 1012, 1013, 1023 ])
        six.assertCountEqual(self, c.faces(1012), [ 1, 1002 ])
        six.assertCountEqual(self, c.faces(1013), [ 1, 1003 ])
        six.assertCountEqual(self, c.faces(1023), [ 1002, 1003 ])
        six.assertCountEqual(self, c.partOf(1), [ 1, 1012, 1013, 123 ])
        six.assertCountEqual(self, c.partOf(1002), [ 1002, 1012, 1023, 123 ])
        six.assertCountEqual(self, c.partOf(1003), [ 1003, 1013, 1023, 123 ])

    def testRelabelCollision( self ):
        """Test relabelling with a collision in the names."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        rename = dict()
        for i in c.simplices():
            rename[i] = i + 1000
        rename[1] = 2
        with self.assertRaises(Exception):
            ns = c.relabel(rename)

    def testOrderViolation( self ):
        """Test that we throw an exception if we try to add a face with the wrong order."""
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
        """Test that we fail if we try to add a duplicate simplex."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        with self.assertRaises(Exception):
            c.addSimplex(id = 1)
        with self.assertRaises(Exception):
            c.addSimplex(id = 1, fs = [ 1, 2 ])

    def testCanonical( self ):
        """Test we can pull out simplices in a canonical order."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ]) 
        six.assertCountEqual(self, c.faces(123), [ 12, 13, 23 ])

    def testSelectByBasis( self ):
        """Test retrieving a simplex by its basis."""
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
        self.assertEqual(c.simplexWithBasis([ 1, 2, 3, 4 ]), None)
        with self.assertRaises(Exception):
            c.simplexWithBasis([ 1, 2, 12 ], fatal = True)
        with self.assertRaises(Exception):
            c.simplexWithBasis([ 1, 2, 4 ], fatal = True)
        with self.assertRaises(Exception):
            c.simplexWithBasis([ 1, 2, 3, 4 ], fatal = True)

    def testClosure( self ):
        """Test that we correctly form the closures of various simplices"""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ]) 
        six.assertCountEqual(self, c.closureOf(1), [ 1 ])
        six.assertCountEqual(self, c.closureOf(2), [ 2 ])
        six.assertCountEqual(self, c.closureOf(3), [ 3 ])
        six.assertCountEqual(self, c.closureOf(12), [ 1, 2, 12 ])
        six.assertCountEqual(self, c.closureOf(13), [ 1, 3, 13 ])
        six.assertCountEqual(self, c.closureOf(23), [ 2, 3, 23 ])
        six.assertCountEqual(self, c.closureOf(123), [ 1, 2, 3, 12, 13, 23, 123 ])
        six.assertCountEqual(self, c.closureOf(23, reverse = True), [ 23, 2, 3 ])
        six.assertCountEqual(self, c.closureOf(123, reverse = True), [ 123, 12, 13, 23, 1, 2, 3 ])

    def testClosureExclude( self ):
        """Test that we correctly exclude the simplex itself from its closure when requested."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ]) 
        six.assertCountEqual(self, c.closureOf(1, exclude_self = True), [ ])
        six.assertCountEqual(self, c.closureOf(2, exclude_self = True), [ ])
        six.assertCountEqual(self, c.closureOf(3, exclude_self = True), [ ])
        six.assertCountEqual(self, c.closureOf(12, exclude_self = True), [ 1, 2 ])
        six.assertCountEqual(self, c.closureOf(13, exclude_self = True), [ 1, 3 ])
        six.assertCountEqual(self, c.closureOf(23, exclude_self = True), [ 2, 3 ])
        six.assertCountEqual(self, c.closureOf(123, exclude_self = True), [ 1, 2, 3, 12, 13, 23 ])

    def testFace( self ):
        """Test we can extract the faces of a simplex."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        six.assertCountEqual(self, c.faceOf(1), [ 12, 13 ])
        six.assertCountEqual(self, c.faceOf(2), [ 12, 23 ])
        six.assertCountEqual(self, c.faceOf(3), [ 13, 23 ])
        six.assertCountEqual(self, c.faceOf(12), [ 123 ])
        six.assertCountEqual(self, c.faceOf(23), [ 123 ])
        six.assertCountEqual(self, c.faceOf(13), [ 123 ])
        six.assertCountEqual(self, c.faceOf(123), [])
        
    def testPart( self ):
        """Test that we correctly form the part-of (co-closure) of various simplices"""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        six.assertCountEqual(self, c.partOf(1), [ 1, 12, 13, 123 ])
        six.assertCountEqual(self, c.partOf(2), [ 2, 23, 12, 123 ])
        six.assertCountEqual(self, c.partOf(3), [ 3, 13, 23, 123 ])
        six.assertCountEqual(self, c.partOf(12), [ 12, 123 ])
        six.assertCountEqual(self, c.partOf(13), [ 13, 123 ])
        six.assertCountEqual(self, c.partOf(23), [ 23, 123 ])
        six.assertCountEqual(self, c.partOf(123), [ 123 ])

    def testPartExcludeSelf( self ):
        """Test that we correctly exclud the simplex itself when requested."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        six.assertCountEqual(self, c.partOf(1, exclude_self = True), [ 12, 13, 123 ])
        six.assertCountEqual(self, c.partOf(2, exclude_self = True), [ 23, 12, 123 ])
        six.assertCountEqual(self, c.partOf(3, exclude_self = True), [ 13, 23, 123 ])
        six.assertCountEqual(self, c.partOf(12, exclude_self = True), [ 123 ])
        six.assertCountEqual(self, c.partOf(13, exclude_self = True), [ 123 ])
        six.assertCountEqual(self, c.partOf(23, exclude_self = True), [ 123 ])
        six.assertCountEqual(self, c.partOf(123, exclude_self = True), [])

    def testPartOrder( self ):
        """Test we get simplices in the desired order."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        fs = c.partOf(1)
        for i in range(len(fs) - 1):
            self.assertTrue(c.orderOf(fs[i]) <= c.orderOf(fs[i + 1]))
        fs = c.partOf(1, reverse = True)
        for i in range(len(fs) - 1):
            self.assertTrue(c.orderOf(fs[i]) >= c.orderOf(fs[i + 1]))

    def testPartDuplicated( self ):
        """Test we only retiurn a common simplex once."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 14, fs = [ 1, 4 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.addSimplex(id = 124, fs = [ 12, 23, 14 ])
        fs = c.partOf(1)
        six.assertCountEqual(self, fs, set(fs))
        
    def testBasis( self ):
        """Test that we correctly form the basis of various simplices"""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        six.assertCountEqual(self, c.basisOf(123), [ 1, 2, 3 ])
        six.assertCountEqual(self, c.basisOf(12), [ 1, 2 ])
        six.assertCountEqual(self, c.basisOf(13), [ 1, 3 ])
        six.assertCountEqual(self, c.basisOf(23), [ 2, 3 ])
        six.assertCountEqual(self, c.basisOf(1), [ 1 ])
        six.assertCountEqual(self, c.basisOf(2), [ 2 ])
        six.assertCountEqual(self, c.basisOf(3), [ 3 ])

    def testRestrictBasis( self ):
        """Test that we correctly restrict the basis of a complex to the right sub-space."""
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
        six.assertCountEqual(self, cprime.simplices(), [ 1 ])

        cprime = copy.deepcopy(c)
        cprime.restrictBasisTo([ 1, 2 ])
        six.assertCountEqual(self, cprime.simplices(), [ 1, 2, 12 ])

        cprime = copy.deepcopy(c)
        cprime.restrictBasisTo([ 1, 2, 3 ])
        six.assertCountEqual(self, cprime.simplices(), c.simplices())

    def testRestrictBasisIsBasis( self ):
        """Test that we correctly require a basis to be 0-simplices."""
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
        """Test that we correctly delete a single simplex."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.deleteSimplex(123)
        six.assertCountEqual(self, c.simplicesOfOrder(2), [])
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 12, 13, 23 ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2, 3])

    def testDeleteLots( self ):
        """Test that we correctly delete multiple simplices, without any cascade."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 13, fs = [ 1, 3 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.deleteSimplices([ 12, 23 ])
        six.assertCountEqual(self, c.simplicesOfOrder(2), [])
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 13 ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2, 3])

    def testDeleteOperator( self ):
        """Test that the delete operator works as expected."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 13, fs = [ 1, 3 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        del c[123]
        six.assertCountEqual(self, c.simplicesOfOrder(2), [])
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 12, 13, 23 ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2, 3])

    def testDeleteWithParts( self ):
        """Test that we correctly cascade deletion to all the simplices
        that the requested simplex is part of."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 13, fs = [ 1, 3 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.deleteSimplex(12)
        six.assertCountEqual(self, c.simplicesOfOrder(2), [])
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 13, 23 ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2, 3])

    def testDeleteLotsWithParts( self ):
        """Test that we correctly cascade deletion to all the simplices
        that the deleted simplices were part of."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 13, fs = [ 1, 3 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.deleteSimplices([ 12, 23 ])
        six.assertCountEqual(self, c.simplicesOfOrder(2), [])
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 13 ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2, 3])

    def testDeleteByBasis( self ):
        """Test we can delete a simplex by its basis."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.deleteSimplexWithBasis([ 1, 2 ])
        six.assertCountEqual(self, c.simplicesOfOrder(2), [])
        six.assertCountEqual(self, c.simplicesOfOrder(1), [ 13, 23 ])
        six.assertCountEqual(self, c.simplicesOfOrder(0), [ 1, 2, 3])
        
    def testOrdering( self ):
        """Test that we can order simplices in order of order."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        ios = c.simplices()
        for i in range(len(ios) - 1):
            self.assertTrue(c.orderOf(ios[i]) <= c.orderOf(ios[i + 1]))
        dos = c.simplices(reverse = True)
        for i in range(len(dos) - 1):
            self.assertTrue(c.orderOf(dos[i]) >= c.orderOf(dos[i + 1]))

    def testDeleteWithFaces( self ):
        """Test that we correctly delete face list elements."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        c.deleteSimplex(12)
        six.assertCountEqual(self, c.partOf(1), [ 1, 13 ])
        self._checkIntegrity(c)

    def testEuler1hole( self ):
        """Test that the Euler characteristic for a simplex with an unfilled triangle."""
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
        """Test that the Euler characteristic for a simplex with two unconnected triangles."""
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


        
