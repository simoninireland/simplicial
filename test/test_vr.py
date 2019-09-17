# Tests of construction of Vietoris-Rips complexes
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

class VietorisRipsTests(unittest.TestCase):

    def testBasis( self ):
        """Test we get the right basis."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplexWithBasis([1, 2, 3])
        em = Embedding(c)
        em[1] = [0, 0]
        em[2] = [0, 3]
        em[3] = [4, 0]

        vr = em.vietorisRipsComplex(0)

        self.assertEqual(len(vr.simplices()), 3)
        self.assertEqual(len(vr.simplicesOfOrder(0)), 3)
        
    def testNoHigherSimplices( self ):
        """Test we don't add any higher simplices for too small a scale."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplexWithBasis([1, 2, 3])
        em = Embedding(c)
        em[1] = [0, 0]
        em[2] = [0, 3]
        em[3] = [4, 0]

        vr = em.vietorisRipsComplex(1)

        self.assertEqual(len(vr.simplices()), 3)
        self.assertEqual(len(vr.simplicesOfOrder(0)), 3)

    def testOneNotBoth( self ):
        """Test we capture the right structure at a slightly larger scale."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplexWithBasis([1, 2, 3])
        em = Embedding(c)
        em[1] = [0, 0]
        em[2] = [0, 3]
        em[3] = [4, 0]

        vr = em.vietorisRipsComplex(3)
        
        self.assertEqual(len(vr.simplices()), 4)
        self.assertEqual(len(vr.simplicesOfOrder(0)), 3)
        self.assertEqual(len(vr.simplicesOfOrder(1)), 1)
        six.assertCountEqual(self, vr.faces(list(vr.simplicesOfOrder(1))[0]), [ 1, 2 ])

    def testTwoEdges( self ):
        """Test we capture the right structure when we should get two simplices but not the triangle."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplexWithBasis([1, 2, 3])
        em = Embedding(c)
        em[1] = [0, 0]
        em[2] = [0, 3]
        em[3] = [4, 0]

        vr = em.vietorisRipsComplex(4)
        
        self.assertEqual(len(vr.simplices()), 5)
        self.assertEqual(len(vr.simplicesOfOrder(0)), 3)
        self.assertEqual(len(vr.simplicesOfOrder(1)), 2)


