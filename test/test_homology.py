# Tests of homology operations in simplicial complex class
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
import numpy
from simplicial import *

class HomologyTests(unittest.TestCase):

    def testChain( self ):
        '''Test we can recognise p-chains correctly.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ]) 
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        self.assertTrue(c.isChain([]))
        self.assertTrue(c.isChain([ 1 ]))
        self.assertTrue(c.isChain([ 1, 2, 3 ]))
        self.assertTrue(c.isChain([ 1, 3, 2 ]))
        self.assertTrue(c.isChain([ 12, 13, 23 ]))
        self.assertFalse(c.isChain([ 1, 3, 12 ]))
        self.assertFalse(c.isChain([ 1, 3, 4 ]))
        self.assertTrue(c.isChain([ 1, 2, 3 ], p = 0))
        self.assertFalse(c.isChain([ 1, 2, 3 ], p = 2))
        self.assertFalse(c.isChain([ 12, 1, 3 ], p = 1))
        with self.assertRaises(Exception):
            c.isChain([ 1, 3, 12 ], fatal = True)

    def testBoundaryMissing(self):
        """Test the boundary of an empty p-chain."""
        c = SimplicialComplex()
        self.assertEqual(len(c.boundary([])), 0)

    def testBoundary0( self ):
        '''Test the boundary operator for a 0-simplex.'''
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        bs = c.boundary([ 1 ])
        six.assertCountEqual(self, bs, set())

    def testBoundary1( self ):
        '''Test the boundary operator for a 1-simplex.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis(bs = [ 1, 2 ], id = 12)
        bs = c.boundary([ 12 ])
        six.assertCountEqual(self, bs, set([ 1, 2 ]))

    def testBoundary2( self ):
        '''Test the boundary operator for a 2-simplex.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis(bs = [ 1, 2, 3 ], id = 123)
        bs = c.boundary([ 123 ])
        six.assertCountEqual(self, bs, c.simplicesOfOrder(1))

    def testBoundary1linked( self ):
        '''Test the boundary operator for two linked 1-simplices.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis(bs = [ 1, 2 ], id = 12)
        c.addSimplexWithBasis(bs = [ 2, 3 ], id = 23)
        bs = c.boundary([ 12, 23 ])
        six.assertCountEqual(self, bs, set([ 1, 3 ]))

    def testBoundary2linked( self ):
        '''Test the boundary operator for two linked 2-simplices.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis(bs = [ 1, 2 ], id = 12)
        c.addSimplexWithBasis(bs = [ 2, 3 ], id = 23)
        c.addSimplexWithBasis(bs = [ 1, 3 ], id = 13)
        c.addSimplexWithBasis(bs = [ 1, 4 ], id = 14)
        c.addSimplexWithBasis(bs = [ 4, 2 ], id = 24)
        c.addSimplex(fs = [ 12, 23, 13 ], id = 123)
        c.addSimplex(fs = [ 12, 14, 24 ], id = 124)
        bs = c.boundary([ 123, 124 ])
        six.assertCountEqual(self, bs, set([ 23, 13, 24, 14 ]))

    def testBoundary2unlinked( self ):
        '''Test the boundary operator for two disconnected 2-simplices.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis(bs = [ 1, 2 ], id = 12)
        c.addSimplexWithBasis(bs = [ 2, 3 ], id = 23)
        c.addSimplexWithBasis(bs = [ 1, 3 ], id = 13)
        c.addSimplexWithBasis(bs = [ 4, 5 ], id = 45)
        c.addSimplexWithBasis(bs = [ 5, 6 ], id = 56)
        c.addSimplexWithBasis(bs = [ 4, 6 ], id = 46)
        c.addSimplex(fs = [ 12, 23, 13 ], id = 123)
        c.addSimplex(fs = [ 45, 56, 46 ], id = 124)
        bs = c.boundary([ 123, 124 ])
        six.assertCountEqual(self, bs, c.simplicesOfOrder(1))

    def testBoundary2boundary( self ):
        '''Test the boundary of a boundary is empty.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis(bs = [ 1, 2 ], id = 12)
        c.addSimplexWithBasis(bs = [ 2, 3 ], id = 23)
        c.addSimplexWithBasis(bs = [ 1, 3 ], id = 13)
        c.addSimplexWithBasis(bs = [ 1, 4 ], id = 14)
        c.addSimplexWithBasis(bs = [ 4, 2 ], id = 24)
        c.addSimplex(fs = [ 12, 23, 13 ], id = 123)
        c.addSimplex(fs = [ 12, 14, 24 ], id = 124)
        bs = c.boundary(c.boundary([ 123, 124 ]))
        six.assertCountEqual(self, bs, set())

    def testBoundaryMatrix0( self ):
        '''Test that the boundary at order 0 is just a zero matrix with a single row.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis([ 1, 2, 3 ])
        b0 = c.boundaryMatrix(0)
        self.assertEqual(b0.shape, (1, 3))
        self.assertTrue((b0 == 0).all())
        
    def testBoundaryMatrixProperties( self ):
        '''Test algebraic properties of boundary operator.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis([ 1, 2, 3 ])
        b2 = c.boundaryMatrix(2)
        b1 = c.boundaryMatrix(1)
        b = numpy.dot(b1, b2) % 2         # boundary matrix composition over underlying binary field
        self.assertTrue((b == 0).all())

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
        
    def testReduce( self ):
        '''Test we reduce matrices correctly to Smith Normal Form.'''
        c = SimplicialComplex()
        A = numpy.array([[-1, -1, -1, -1,  0,  0,  0,  0],
                         [ 1,  0,  0,  0, -1, -1,  0,  0],
                         [ 0,  1,  0,  0,  1,  0, -1, -1],
                         [ 0,  0,  1,  0,  0,  1,  1,  0],
                         [ 0,  0,  0,  1,  0,  0,  0,  1]])
        Ar = c.smithNormalForm(abs(A))

        (ra, ca) = Ar.shape
        rank = min([ ra, ca ])
        onDiagonal = True
        for i in range(rank):
            for j in range(rank):
                if i == j:
                    if onDiagonal:
                        self.assertTrue(Ar[i, j] in [ 0, 1 ])
                        if Ar[i, j] == 0:
                            onDiagonal = False
                    else:
                        self.assertEqual(Ar[i, j], 0)
                else:
                    self.assertEqual(Ar[i, j], 0)
        for i in range(ra):
            for j in range(rank, ca):
                self.assertEqual(Ar[i, j], 0)
        for j in range(ca):
            for i in range(rank, ra):
                self.assertEqual(Ar[i, j], 0)
                
    def testBettiSmall( self ):
        '''Test computation of Betti numbers on a small complex.'''
        c = SimplicialComplex()
        c.addSimplex(id = "0d0")
        c.addSimplex(id = "0d1")
        c.addSimplex(id = "0d2")
        c.addSimplex(id = "0d3")
        c.addSimplex(id = "0d4")
        c.addSimplex(["0d0", "0d1"], id = "1d01")
        c.addSimplex(["0d0", "0d2"], id = "1d02")
        c.addSimplex(["0d0", "0d3"], id = "1d03")
        c.addSimplex(["0d0", "0d4"], id = "1d04")
        c.addSimplex(["0d1", "0d2"], id = "1d12")
        c.addSimplex(["0d1", "0d3"], id = "1d13")
        c.addSimplex(["0d2", "0d3"], id = "1d23")
        c.addSimplex(["0d2", "0d4"], id = "1d24")
        c.addSimplex(["1d01", "1d02", "1d12"], id = "2d012")
        c.addSimplex(["1d01", "1d03", "1d13"], id = "2d013")
        c.addSimplex(["1d02", "1d03", "1d23"], id = "2d023")
        c.addSimplex(["1d12", "1d13", "1d23"], id = "2d123")
        betti = c.bettiNumbers(ks = [1])
        self.assertEqual(betti[1], 1)
        
    def testBettiSmallFromBasis( self ):
        '''Test computation of Betti numbers on a small complex created just from its basis.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis([0, 1, 2])
        c.addSimplexWithBasis([0, 1, 3])
        c.addSimplexWithBasis([0, 2, 3])
        c.addSimplexWithBasis([1, 2, 3])
        c.addSimplexWithBasis([0, 4])
        c.addSimplexWithBasis([4, 2])
        betti = c.bettiNumbers(ks = [1, 2])
        six.assertCountEqual(self, betti.keys(), [ 1, 2 ])
        self.assertEqual(betti[1], 1)
        self.assertEqual(betti[2], 1)

    def testBettiPlane( self ):
        '''Test Betti numbers for a plane.'''
        c = TriangularLattice(10, 10)
        betti = c.bettiNumbers(ks = [1])
        self.assertEqual(betti[1], 0)

    def testBettiHoledPlane( self ):
        '''Test Betti numbers for a plane with one 2-simplex removed.'''
        c = TriangularLattice(10, 10)
        c.deleteSimplex("2d284")         # a simplex we know is central-ish 
        betti = c.bettiNumbers(ks = [1])
        self.assertEqual(betti[1], 1)

    def testBettiDoubleHoledPlane( self ):
        '''Test Betti numbers for a plane with two 2-simplices removed.'''
        c = TriangularLattice(10, 10)
        c.deleteSimplex("2d284")         # simplices we know are central-ish 
        c.deleteSimplex("2d257")
        betti = c.bettiNumbers(ks = [1])
        self.assertEqual(betti[1], 2)
        
    def testBettiZeroConnected( self ):
        '''Test the zero'th Betti number of a connected complex'''
        c = TriangularLattice(10, 10)
        betti = c.bettiNumbers(ks = [0])
        self.assertEqual(betti[0], 1)
        
    def testBettiZeroDisconnected( self ):
        '''Test the zero'th Betti number of a complex of two "islands"'''
        c = TriangularLattice(10, 10)
        c.addSimplexOfOrder(2)
        betti = c.bettiNumbers(ks = [0])
        self.assertEqual(betti[0], 2)

    def testBettiAll( self ):
        '''Test computing the Betti numbers for all simplex orders.'''
        c = TriangularLattice(10, 10)
        betti = c.bettiNumbers()
        six.assertCountEqual(self, betti.keys(), [ 0, 1, 2 ])
        self.assertEqual(betti[0], 1)
        self.assertEqual(betti[1], 0)
        self.assertEqual(betti[2], 0)
        
    def testBettiHigh( self ):
        '''Test that we get a Betti number of 0 for any order higher than the maximum.'''
        c = TriangularLattice(10, 10)
        betti = c.bettiNumbers(ks = [ 3, 7 ])
        six.assertCountEqual(self, betti.keys(), [ 3, 7 ])
        self.assertEqual(betti[3], 0)
        self.assertEqual(betti[7], 0)
        
