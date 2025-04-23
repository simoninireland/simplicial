# Tests of simplicial functions and representations
#
# Copyright (C) 2024--2025 Simon Dobson
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


class SFTests(unittest.TestCase):

    def setUp(self):
        self._c = SimplicialComplex()

        # default function returns the name of the simplex
        self._f = lambda sf, c, s: s


    # ---------- Literal representation ----------

    def testLiteralEmpty(self):
        '''Test an empty representation.'''
        f = SimplicialFunction(self._c)
        self.assertTrue(isinstance(f.representation(), LiteralSFRepresentation))


    def testLiteralAdd(self):
        '''Test we can add and retrieve values.'''
        f = SimplicialFunction(self._c)
        self._c.addSimplex(id='b')
        self._c.addSimplex(id='c')
        f['b'] = 20
        f['c'] = 30
        self.assertEqual(f['b'], 20)
        self.assertEqual(f['c'], 30)


    def testLiteralAddMulti(self):
        '''Test we can add simplcies from a dict.'''
        f = SimplicialFunction(self._c)
        self._c.addSimplex(id='b')
        self._c.addSimplex(id='c')
        f.setValuesForSimplices(dict(b=20, c=30))
        self.assertEqual(f['b'], 20)
        self.assertEqual(f['c'], 30)


    def testLiteralMissingSimplex(self):
        '''Test we can't assign a value to, or retrieve a value from, a non-simplex.'''
        f = SimplicialFunction(self._c)
        self._c.addSimplex(id='b')
        with self.assertRaises(ValueError):
            f['c'] = 20
        with self.assertRaises(ValueError):
            f['c']


    def testLiteralRemove(self):
        '''Test we can remove a simplex.'''
        f = SimplicialFunction(self._c)
        self._c.addSimplex(id='b')
        self._c.addSimplex(id='c')
        f['b'] = 20
        f['c'] = 30
        self.assertEqual(f['b'], 20)
        self.assertEqual(f['c'], 30)
        f.removeSimplex('c')
        self.assertEqual(f['b'], 20)


    def testLiteralDomain(self):
        '''Test we can extract the domain.'''
        f = SimplicialFunction(self._c)
        self._c.addSimplex(id='b')
        self._c.addSimplex(id='c')
        f['b'] = 20
        f['c'] = 30
        self.assertCountEqual(f.domain(), ['b', 'c'])
        self.assertIn('b', f)
        self.assertNotIn('d', f)


    # ---------- Attribute representation ----------

    def testAttributeEmpty(self):
        '''Test an empty representation.'''
        f = SimplicialFunction(self._c, attr='test')
        self.assertTrue(isinstance(f.representation(), AttributeSFRepresentation))


    def testAttributeAdd(self):
        '''Test we can retrieve values from attributes.'''
        f = SimplicialFunction(self._c, attr='test')
        self._c.addSimplex(id='a', attr={'test': 30})
        self._c.addSimplex(id='b')
        self.assertEqual(f['a'], 30)


    def testAttributeAdd(self):
        '''Test we can'd add values.'''
        f = SimplicialFunction(self._c,attr='test')
        self._c.addSimplex(id='b')
        with self.assertRaises(ValueError):
            f['b'] = 30


    def testAttributeMissingSimplex(self):
        '''Test we can't retrieve a value from a non-simplex.'''
        f = SimplicialFunction(self._c)
        self._c.addSimplex(id='b')
        with self.assertRaises(ValueError):
            f['c']


    def testAttributeDomain(self):
        '''Test we can extract the domain.'''
        f = SimplicialFunction(self._c, attr='test')
        self._c.addSimplex(id='a', attr={'test': 30})
        self._c.addSimplex(id='b')
        self.assertCountEqual(f.domain(), ['a'])
        self.assertIn('a', f)
        self.assertNotIn('b', f)


    # ---------- Computed representation ----------

    def testComputedEmpty(self):
        '''Test an empty representation.'''
        f = SimplicialFunction(self._c, f=self._f)
        self.assertTrue(isinstance(f.representation(), ComputedSFRepresentation))


    def testComputedRetrieve(self):
        '''Test we can retrieve values using the function.'''
        f = SimplicialFunction(self._c, f=self._f)
        self._c.addSimplex(id='a')
        self._c.addSimplex(id='b')
        self.assertEqual(f['a'], 'a')
        self.assertEqual(f['b'], 'b')


    def testComputedAdd(self):
        '''Test we can't add values.'''
        f = SimplicialFunction(self._c, f=self._f)
        self._c.addSimplex(id='b')
        with self.assertRaises(ValueError):
            f['b'] = 30


    def testComputedMissingSimplex(self):
        '''Testr we can't retrieve values for a missing simplex.'''
        f = SimplicialFunction(self._c, f=self._f)
        self._c.addSimplex(id='a')
        self._c.addSimplex(id='b')
        with self.assertRaises(ValueError):
            f['c']


    # ---------- Inferred representastion ----------

    def testInferredEmpty(self):
        '''Test we can create a representation.'''
        SimplicialFunction(self._c, rep=InferredSFRepresentation(self._f))


    def testInferredLiterals(self):
        '''Test we can retrieve literal values.'''
        rep = InferredSFRepresentation(self._f)
        f = SimplicialFunction(self._c, rep=rep)
        self._c.addSimplex(id='a')
        self._c.addSimplex(id='b')
        rep.setValueForSimplex('a', 1)
        self.assertEqual(f['a'], 1)
        self.assertEqual(f['b'], 'b')


    def testInferCorrect(self):
        '''Test we can define an inference function that depends on the values of set simplices.'''

        def sumOfFaceValues(sf, c, s):
            '''Return the sum of values at the faces.'''
            return sum([sf(f) for f in c.faces(s)])

        rep = InferredSFRepresentation(sumOfFaceValues)
        f = SimplicialFunction(self._c, rep=rep)
        self._c.addSimplex(id='a')
        self._c.addSimplex(id='b')
        self._c.addSimplex(fs=['a', 'b'], id='ab')
        rep.setValueForSimplex('a', 1)
        rep.setValueForSimplex('b', 2)
        self.assertEqual(f['ab'], 3)


    # ---------- High-level functions ----------

    def testFunctionFilter(self):
        '''Test we can filter simplcies by predicate.'''
        f = SimplicialFunction(self._c)
        self._c.addSimplex(id='b')
        self._c.addSimplex(id='c')
        f['b'] = 20
        f['c'] = 30
        self.assertCountEqual(f.allSimplices(lambda sf, c, s: sf[s] > 25), ['c'])


    def testFunctionIterator(self):
        '''Test we can iterate over simplices in a funmction.'''
        f = SimplicialFunction(self._c)
        self._c.addSimplex(id='b')
        self._c.addSimplex(id='c')
        self._c.addSimplex(id='d')
        f['b'] = 20
        f['c'] = 30
        self.assertCountEqual(list(f), ['b', 'c'])


if __name__ == '__main__':
    unittest.main()
