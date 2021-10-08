# Tests of filtrations
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

class FiltrationTests(unittest.TestCase):

    def testSimple(self):
        '''Test basic behaviour.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        self.assertCountEqual(f.simplices(), [ 1, 2 ])
        f.setIndex(0.5)
        self.assertCountEqual(f.simplices(), [ 1, 2 ])
        f.addSimplex([1, 2], id = 12)
        self.assertCountEqual(f.simplices(), [ 1, 2, 12 ])
        f.setIndex(0)
        self.assertCountEqual(f.simplices(), [ 1, 2 ])

    def testAddDuplicateSimplex(self):
        '''Test we can't duplicate simplices at the same or different indices.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        with self.assertRaises(Exception):
            f.addSimplex(id = 2)
        f.setIndex(1.0)
        with self.assertRaises(Exception):
            f.addSimplex(id = 2)

    def testAddWithBasis(self):
        '''Test we can add a simplex by basis.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplexWithBasis(bs = [1, 2, 3], id = 123)
        self.assertTrue(f.numberOfSimplices(), 7)
        for s in [ 1, 2, 3, 12, 123 ]:   # there are auto-named simplices too
            self.assertTrue(s in f)

    def testAddComplexSimple(self):
        '''Test we can add a complete complex in one operation.'''
        f = Filtration()
        f.addSimplex(id = 100)
        f.addSimplex(id = 200)
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex([1, 2], id = 12)
        c.addSimplex(id = 3)
        c.addSimplex([1, 3], id = 13)
        c.addSimplex([2, 3], id = 23)
        c.addSimplex([12, 23, 13], id = 123)
        f.addSimplicesFrom(c)
        self.assertEqual(f.indices(), [ 0.0 ])
        self.assertCountEqual(f.simplices(), [ 100, 200, 1, 2, 3, 12, 23, 13, 123 ])

    def testAddComplexLater(self):
        '''Test we can add a complete complex at the right index.'''
        f = Filtration()
        f.addSimplex(id = 100)
        f.addSimplex(id = 200)
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex([1, 2], id = 12)
        c.addSimplex(id = 3)
        c.addSimplex([1, 3], id = 13)
        c.addSimplex([2, 3], id = 23)
        c.addSimplex([12, 23, 13], id = 123)
        f.setIndex(1.0)
        f.addSimplicesFrom(c)
        self.assertEqual(f.indices(), [ 0.0, 1.0 ])
        f.setIndex(0.0)
        self.assertCountEqual(f.simplices(), [ 100, 200 ])
        f.setIndex(1.0)
        self.assertCountEqual(f.simplices(), [ 100, 200, 1, 2, 3, 12, 23, 13, 123 ])

    def testAddComplexDuplicateSimplex(self):
        '''Test we detect duplicate simplices.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex([1, 2], id = 12)
        with self.assertRaises(Exception):
            f.addSimplicesFrom(c)

    def testAddComplexRenaming(self):
        '''Test we can rename as we copy.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex([1, 2], id = 12)
        r = dict()
        r[1] = 4
        r[2] = 5
        f.addSimplicesFrom(c, rename = r)
        self.assertCountEqual(f.simplices(), [ 1, 2, 4, 5, 12  ])
        self.assertCountEqual(f.faces(12), [ 4, 5 ])

    def testAddFiltration(self):
        '''Test that adding a filtration  works, and flattens the index structure of the one added.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplex([1, 3], id = 13)
        f.addSimplex([2, 3], id = 23)
        f.addSimplex([12, 23, 13], id = 123)

        g = Filtration()
        g.addSimplex(id = 4)
        g.setIndex(0.7)
        g.addSimplex(id = 5)
        g.addSimplex([4, 5], id = 45)

        f.addSimplicesFrom(g)
        f.setIndex(0)
        self.assertCountEqual(f.simplices(), [ 1, 2 ])
        f.setIndex(0.5)
        self.assertCountEqual(f.simplices(), [ 1, 2, 12])
        self.assertFalse(f.isIndex(0.7))
        f.setIndex(1.0)
        self.assertCountEqual(f.simplices(), [ 1, 2, 12, 3, 23, 13, 123, 4, 5, 45])

    def testExtremeIndices(self):
        '''Test we can move to the ends of the filtration.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplexWithBasis(bs = [1, 2, 3], id = 123)
        f.setMinimumIndex()
        self.assertEqual(f.getIndex(), 0)
        self.assertCountEqual(f.simplices(), [ 1, 2 ])
        f.setMaximumIndex()
        self.assertEqual(f.getIndex(), 1.0)
        self.assertTrue(f.numberOfSimplices(), 7)
        for s in [ 1, 2, 3, 12, 123 ]:   # there are auto-named simplices too
            self.assertTrue(s in f)

    def testIndices(self):
        '''Test we can extract the indices.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplex([1, 3], id = 13)
        f.addSimplex([2, 3], id = 23)
        f.addSimplex([12, 23, 13], id = 123)
        self.assertEqual(f.indices(), [ 0.0, 0.5, 1.0 ])

    def testCopyFiltration(self):
        '''Test we can copy the filtration.'''
        f = Filtration(0.1)
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplex([1, 3], id = 13)
        f.addSimplex([2, 3], id = 23)
        f.addSimplex([12, 23, 13], id = 123)
        f[2]['name'] = 'hello'

        g = f.copy()
        self.assertEqual(g.indices(), [ 0.1, 0.5, 1.0 ])
        self.assertEqual(g[2]['name'], 'hello')
        g.setIndex(0.1)
        self.assertCountEqual(g.simplices(), [ 1, 2 ])
        g.setIndex(0.5)
        self.assertCountEqual(g.simplices(), [ 1, 2, 12 ])
        g.setIndex(1.0)
        self.assertCountEqual(g.simplices(), [ 1, 2, 3, 12, 23, 13, 123 ])

    def testSnapComplex(self):
        '''Test we extract the complex at the right index when copying.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplex([1, 3], id = 13)
        f.addSimplex([2, 3], id = 23)
        f.addSimplex([12, 23, 13], id = 123)
        f[2]['name'] = 'hello'

        f.setIndex(0.5)
        c = f.snap()
        self.assertCountEqual(c.simplices(), [ 1, 2, 12 ])
        self.assertEqual(c[2]['name'], f[2]['name'])
        f[2]['name'] = 'goodbye'
        self.assertEqual(c[2]['name'], 'hello')
        self.assertEqual(f[2]['name'], 'goodbye')

    def testIterateComplexes(self):
        '''Test we iterate over the complxes correctly.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplex([1, 3], id = 13)
        f.addSimplex([2, 3], id = 23)
        f.addSimplex([12, 23, 13], id = 123)

        cs = list(f.complexes())
        self.assertCountEqual(cs[0].simplices(), [ 1, 2 ])
        self.assertCountEqual(cs[1].simplices(), [ 1, 2, 12 ])
        self.assertCountEqual(cs[2].simplices(), [ 1, 2, 3, 12, 23, 13, 123 ])

    def testInclusion(self):
        '''Test the filtration forms a valid sequence of inclusions.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(0.7)
        # leave this index blank
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplex([1, 3], id = 13)
        f.addSimplex([2, 3], id = 23)
        f.addSimplex([12, 23, 13], id = 123)

        cs = list(f.complexes())
        for i in range(len(cs) - 1):
            self.assertTrue(cs[i] <= cs[i + 1])

    def testDeletionPreservesInclusion(self):
        '''Test the deletions cascade properly.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(1.0)
        f.addSimplex(id = 3)
        f.addSimplex([1, 3], id = 13)
        f.addSimplex([2, 3], id = 23)
        f.addSimplex([12, 23, 13], id = 123)

        f.deleteSimplex(2)
        self.assertCountEqual(f.simplices(), [ 1, 3, 13 ])

        cs = list(f.complexes())
        for i in range(len(cs) - 1):
            self.assertTrue(cs[i] <= cs[i + 1])

    def testAdded(self):
        '''Test we can retrieve birth times.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.setIndex(0.7)
        self.assertEqual(f.addedAtIndex(12), 0.5)
        self.assertEqual(f.addedAtIndex(1), 0.0)
        self.assertCountEqual(f.simplicesAddedAtIndex(0.0), [ 1, 2])
        self.assertCountEqual(f.simplicesAddedAtIndex(0.5), [ 12])
        self.assertCountEqual(f.simplicesAddedAtIndex(0.7), [])

    def testDeleteionDeletesBirthTime(self):
        '''Test that deletion destroys the birth time.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        f.setIndex(0.5)
        f.addSimplex([1, 2], id = 12)
        f.deleteSimplex(1)
        with self.assertRaises(Exception):
            self.assertEqual(f.addedAtIndex(1), 0.0)
        self.assertEqual(f.addedAtIndex(2), 0.0)
        with self.assertRaises(Exception):
            self.assertEqual(f.addedAtIndex(12), 0.5)


if __name__ == '__main__':
    unittest.main()
