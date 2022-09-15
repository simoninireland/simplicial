# Tests of composing complexes
#
# Copyright (C) 2017--2022 Simon Dobson
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
import itertools
from simplicial import *

class ComposeTests(unittest.TestCase):

    def testDisjointPoints(self):
        '''Test we can add two one-point disjoint complexes.'''
        c1 = SimplicialComplex()
        c1.addSimplex(id=1)
        c2 = SimplicialComplex()
        c2.addSimplex(id=2)

        # check composition
        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2])
        self.assertEqual(d.maxOrder(), 0)

        # check the original complexes are left undisturbed
        self.assertCountEqual(c1.simplicesOfOrder(0), [1])
        self.assertEqual(c1.maxOrder(), 0)
        self.assertCountEqual(c2.simplicesOfOrder(0), [2])
        self.assertEqual(c2.maxOrder(), 0)

    def testConjointPoints(self):
        '''Test we can add two one-point complexes with the same label.'''
        c1 = SimplicialComplex()
        c1.addSimplex(id=1)
        c2 = SimplicialComplex()
        c2.addSimplex(id=1)

        d = c1.compose(c2)
        s0 = d.simplicesOfOrder(0)
        self.assertEqual(len(s0), 1)
        self.assertIn(1, s0)

    def testDisjointLines(self):
        '''Test we can form disjoint lines.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='a')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([3, 4], id='b')

        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2, 3, 4])
        self.assertEqual(len(d.simplicesOfOrder(1)), 2)
        self.assertCountEqual(d.basisOf('a'), [1, 2])
        self.assertCountEqual(d.basisOf('b'), [3, 4])
        self.assertEqual(d.maxOrder(), 1)

    def testElbowLines(self):
        '''Test we can form an elbow of two lines.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='a')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 3], id='b')

        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2, 3])
        self.assertEqual(len(d.simplicesOfOrder(1)), 2)
        self.assertCountEqual(d.basisOf('a'), [1, 2])
        self.assertCountEqual(d.basisOf('b'), [1, 3])
        self.assertEqual(d.maxOrder(), 1)

    def testMergeLines(self):
        '''Test we can merge two lines.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='a')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 2], id='a')

        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2])
        self.assertEqual(len(d.simplicesOfOrder(1)), 1)
        self.assertCountEqual(d.basisOf('a'), [1, 2])
        self.assertEqual(d.maxOrder(), 1)

    def testFailMergeLines(self):
        '''Test we can't merge two lines with the same basis but different labels.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='a')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 2], id='b')

        with self.assertRaises(ValueError):
            d = c1.compose(c2)

    def testFailMergeLinesDifferentBases(self):
        '''Test we can't merge two lines with the same labels but different bases.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='a')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([4, 3], id='a')

        with self.assertRaises(ValueError):
            d = c1.compose(c2)

    def testFailMergeLinesDifferentLabels(self):
        '''Test we can't merge two lines with the different labels and the same bases.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='a')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([4, 3], id='a')

        with self.assertRaises(ValueError):
            d = c1.compose(c2)

    def testMergeTriangles(self):
        '''Test we can merge triangles.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='12')
        c1.addSimplexWithBasis([2, 3], id='23')
        c1.addSimplexWithBasis([3, 1], id='31')
        c1.addSimplex(['12', '23', '31'], id='123')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 2], id='12')
        c2.addSimplexWithBasis([2, 3], id='23')
        c2.addSimplexWithBasis([3, 1], id='31')
        c2.addSimplex(['12', '23', '31'], id='123')

        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2, 3])
        self.assertEqual(len(d.simplicesOfOrder(1)), 3)
        self.assertEqual(len(d.simplicesOfOrder(2)), 1)
        self.assertCountEqual(d.faces('123'), ['12', '31', '23'])
        self.assertEqual(d.maxOrder(), 2)

    def testMergeTrianglesOneEdge(self):
        '''Test we can merge triangles that share an edge.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='12')
        c1.addSimplexWithBasis([2, 3], id='23')
        c1.addSimplexWithBasis([3, 1], id='31')
        c1.addSimplex(['12', '23', '31'], id='123')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 4], id='14')
        c2.addSimplexWithBasis([4, 2], id='42')
        c2.addSimplexWithBasis([1, 2], id='12')
        c2.addSimplex(['14', '42', '12'], id='124')

        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2, 3, 4])
        self.assertEqual(len(d.simplicesOfOrder(1)), 5)
        self.assertEqual(len(d.simplicesOfOrder(2)), 2)
        self.assertCountEqual(d.faces('123'), ['12', '31', '23'])
        self.assertCountEqual(d.faces('124'), ['12', '42', '14'])
        self.assertEqual(d.maxOrder(), 2)

    def testFailMergeTrianglesTwoEdges(self):
        '''Test we can't merge triangles with one mis-labelled edge.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='12')
        c1.addSimplexWithBasis([2, 3], id='23')
        c1.addSimplexWithBasis([3, 1], id='31')
        c1.addSimplex(['12', '23', '31'], id='123')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 2], id='12')
        c2.addSimplexWithBasis([2, 3], id='***')
        c2.addSimplexWithBasis([3, 1], id='31')
        c2.addSimplex(['12', '***', '31'], id='124')

        with self.assertRaises(ValueError):
            d = c1.compose(c2)

    def testFailMergeDifferentOrders(self):
        '''Test we can't merge simplices of different orders.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='12')
        c2 = SimplicialComplex()
        c2.addSimplex(id='12')

        with self.assertRaises(ValueError):
            d = c1.compose(c2)

    def testFillTriangleVoid(self,):
        '''Check we can fill a void.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='12')
        c1.addSimplexWithBasis([2, 3], id='23')
        c1.addSimplexWithBasis([3, 1], id='31')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 2], id='12')
        c2.addSimplexWithBasis([2, 3], id='23')
        c2.addSimplexWithBasis([3, 1], id='31')
        c2.addSimplex(['12', '23', '31'], id='123')

        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2, 3])
        self.assertEqual(len(d.simplicesOfOrder(1)), 3)
        self.assertEqual(len(d.simplicesOfOrder(2)), 1)
        self.assertCountEqual(d.faces('123'), ['12', '31', '23'])

    def testLeaveTriangle(self,):
        '''Check that a triangle isn't disturbed by its faces being merged.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='12')
        c1.addSimplexWithBasis([2, 3], id='23')
        c1.addSimplexWithBasis([3, 1], id='31')
        c1.addSimplex(['12', '23', '31'], id='123')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 2], id='12')
        c2.addSimplexWithBasis([2, 3], id='23')
        c2.addSimplexWithBasis([3, 1], id='31')

        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2, 3])
        self.assertEqual(len(d.simplicesOfOrder(1)), 3)
        self.assertEqual(len(d.simplicesOfOrder(2)), 1)
        self.assertCountEqual(d.faces('123'), ['12', '31', '23'])
        self.assertEqual(d.maxOrder(), 2)

    def testIntersectTriangles(self):
        '''Test we can build an "hourglass" from two triangles.'''
        c1 = SimplicialComplex()
        c1.addSimplexWithBasis([1, 2], id='12')
        c1.addSimplexWithBasis([2, 3], id='23')
        c1.addSimplexWithBasis([3, 1], id='31')
        c1.addSimplex(['12', '23', '31'], id='123')
        c2 = SimplicialComplex()
        c2.addSimplexWithBasis([1, 5], id='15')
        c2.addSimplexWithBasis([5, 6], id='56')
        c2.addSimplexWithBasis([6, 1], id='61')
        c2.addSimplex(['15', '56', '61'], id='156')

        d = c1.compose(c2)
        self.assertCountEqual(d.simplicesOfOrder(0), [1, 2, 3, 5, 6])
        self.assertEqual(len(d.simplicesOfOrder(1)), 6)
        self.assertEqual(len(d.simplicesOfOrder(2)), 2)
        self.assertCountEqual(d.faces('12'), [1, 2])
        self.assertCountEqual(d.faces('15'), [1, 5])
        self.assertCountEqual(d.faces('123'), ['12', '31', '23'])
        self.assertCountEqual(d.faces('156'), ['15', '61', '56'])
        self.assertEqual(d.maxOrder(), 2)

    def testMergeAttributes(self):
        '''Test we merge atributes when we merge simplices.'''
        c1 = SimplicialComplex()
        c1.addSimplex(id=1, attr=dict(a=1, b=4, c='hello'))
        c2 = SimplicialComplex()
        c2.addSimplex(id=1, attr=dict(b=10, d='goodbye'))
        c2.addSimplex(id=2, attr=dict(a=45))

        # check merge
        d = c1.compose(c2)
        attr1 = d[1]
        self.assertEqual(attr1['a'], 1)
        self.assertEqual(attr1['b'], 10)
        self.assertEqual(attr1['c'], 'hello')
        self.assertEqual(attr1['d'], 'goodbye')
        attr2 = d[2]
        self.assertEqual(attr2['a'], 45)

        # check originals are unchanged
        attr1 = c1[1]
        self.assertCountEqual(attr1.keys(), set(['a', 'b', 'c']))
        self.assertEqual(attr1['a'], 1)
        self.assertEqual(attr1['b'], 4)
        self.assertEqual(attr1['c'], 'hello')
        attr1 = c2[1]
        self.assertEqual(attr1['b'], 10)
        self.assertEqual(attr1['d'], 'goodbye')
        self.assertCountEqual(attr1.keys(), set(['d', 'b']))
        attr2 = c2[2]
        self.assertEqual(attr2['a'], 45)
        self.assertCountEqual(attr2.keys(), set(['a']))

    def testIntersectRings(self):
        '''Test we can intersect two rings at a point.'''

        # first ring
        r1 = ring(10)
        r2 = ring(15)
        r2.relabelDisjointFrom(r1)

        # give two nodes the same label
        s = list(r1.simplicesOfOrder(0))[0]
        q = list(r2.simplicesOfOrder(0))[0]
        r1r = dict()
        r1r[s] = '*'
        r1.relabel(r1r)
        r2r = dict()
        r2r[q] = '*'
        r2.relabel(r2r)

        # compose the rings
        d = r1.compose(r2)
        self.assertEqual(len(d.simplicesOfOrder(0)),
                         len(r1.simplicesOfOrder(0)) + len(r2.simplicesOfOrder(0)) - 1)
        self.assertEqual(d.maxOrder(), 1)


if __name__ == '__main__':
    unittest.main()
