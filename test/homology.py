# Tests of homology operations in simplicial complex class
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
import numpy
import copy
from simplicial import *

class HomologyTests(unittest.TestCase):

    def testBoundary( self ):
        '''Test algebraic properties of boundary operator.'''
        c = SimplicialComplex()
        c.addSimplexWithBasis([ 1, 2, 3 ])
        b2 = c.boundaryMatrix(2)
        b1 = c.boundaryMatrix(1)
        b = numpy.dot(b1, b2) % 2         # boundary composition over underlying binary field
        self.assertTrue((b == 0).all())

    def testReduce( self ):
        '''Test we reduce matrices correctly.'''
        c = SimplicialComplex()
        A = numpy.array([[-1, -1, -1, -1,  0,  0,  0,  0],
                         [ 1,  0,  0,  0, -1, -1,  0,  0],
                         [ 0,  1,  0,  0,  1,  0, -1, -1],
                         [ 0,  0,  1,  0,  0,  1,  1,  0],
                         [ 0,  0,  0,  1,  0,  0,  0,  1]])
        B = numpy.array([[ 1,  1,  0,  0],
                         [-1,  0,  1,  0],
                         [ 0, -1, -1,  0],
                         [ 0,  0,  0,  0],
                         [ 1,  0,  0,  1],
                         [ 0,  1,  0, -1],
                         [ 0,  0,  1,  1],
                         [ 0,  0,  0,  0]])
        Ar, Br = c._reduce(abs(A), abs(B))

        (ra, ca) = Ar.shape
        (rb, cb) = Br.shape            
        zc = numpy.zeros(ra)
        pivotC = [ numpy.all(Ar[:, j] == zc) for j in range(ca) ].count(False)
        zr = numpy.zeros(cb)
        pivotR = [ numpy.all(Br[i, :] == zr) for i in range(rb) ].count(False)

        kDim = ca
        kernelDim = kDim - pivotC
        imageDim = pivotR
        self.assertEqual(kDim, 8)
        self.assertEqual(kernelDim, 4)
        self.assertEqual(imageDim, 3)
        
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
        betti = c.bettiNumbers(ks = [1])
        self.assertEqual(betti[1], 1)

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
        print c.simplicesOfOrder(2)
        c.deleteSimplex("2d284")         # simplices we know are central-ish 
        c.deleteSimplex("2d257")
        betti = c.bettiNumbers(ks = [1])
        self.assertEqual(betti[1], 2)
        
