# Tests of simplicial functions and representations
#
# Copyright (C) 2024 Simon Dobson
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
        SimplicialFunction(self._c, default=10)


    def testLiteralAdd(self):
        '''Test we can add and retrieve values.'''
        f = SimplicialFunction(self._c, default=10)
        self._c.addSimplex(id='b')
        self._c.addSimplex(id='c')
        f['b'] = 20
        f['c'] = 30
        self.assertEqual(f['b'], 20)
        self.assertEqual(f['c'], 30)


    def testLiteralMissingSimplex(self):
        '''Test we can't assign a value to, or retrieve a value from, a non-simplex.'''
        f = SimplicialFunction(self._c, default=10)
        self._c.addSimplex(id='b')
        with self.assertRaises(ValueError):
            f['c'] = 20
        with self.assertRaises(ValueError):
            f['c']


    # ---------- Attribute representation ----------

    def testAttributeEmpty(self):
        '''Test an empty representation.'''
        SimplicialFunction(self._c, attr='test', default=10)


    def testAttributeAdd(self):
        '''Test we can retrieve values from attributes.'''
        f = SimplicialFunction(self._c, attr='test', default=10)
        self._c.addSimplex(id='a', attr={'test': 30})
        self._c.addSimplex(id='b')
        self.assertEqual(f['a'], 30)
        self.assertEqual(f['b'], 10)   # default


    def testAttributeAdd(self):
        '''Test we can'd add values.'''
        f = SimplicialFunction(self._c,attr='test', default=10)
        self._c.addSimplex(id='b')
        with self.assertRaises(ValueError):
            f['b'] = 30


    def testAttributeMissingSimplex(self):
        '''Test we can't retrieve a value from a non-simplex.'''
        f = SimplicialFunction(self._c, default=10)
        self._c.addSimplex(id='b')
        with self.assertRaises(ValueError):
            f['c']


    # ---------- Computed representation ----------

    def testComputedEmpty(self):
        '''Test an empty representation.'''
        SimplicialFunction(self._c, f=self._f)


    def testComputedRetrieve(self):
        '''Test we can retrieve values using the function.'''
        f = SimplicialFunction(self._c, f=self._f)
        self._c.addSimplex(id='a')
        self._c.addSimplex(id='b')
        self.asfsertEqual(f['a'], 'a')
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


if __name__ == '__main__':
    unittest.main()
