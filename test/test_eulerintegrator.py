# Tests of Euler integration
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
from simplicial import *


class FaceMin(SimplicialFunction):

    @staticmethod
    def minimumValueOfFaces(sf, c, s):
        '''Return the minimum of the values assigned face of the given simplex.

        :param sf: the function (self)
        :param c: the complex
        :param s: the simlex
        :returns: the value'''
        return min([sf[f] for f in c.faces(s)])

    # We use an inferred representation to let us set explicit values
    # for simplices, with an inference function that fills-in the
    # values not explicitly set for other simplces.

    def __init__(self, c):
        rep = InferredSFRepresentation(FaceMin.minimumValueOfFaces)
        super().__init__(c, rep=rep)


class EulerIntegratorTests(unittest.TestCase):

    def testMetric(self):
        '''Test our metric behaves itself.'''
        c = SimplicialComplex()
        n1 = c.addSimplex()
        n2 = c.addSimplex()
        e1 = c.addSimplex(fs=[n1, n2])
        height = FaceMin(c)
        height[n1] = 1
        height[n2] = 2
        self.assertEqual(height(n1), 1)
        self.assertEqual(height(n2), 2)
        self.assertEqual(height(e1), 1)
        with self.assertRaises(ValueError):
            height[3]


    def test1simplex0(self):
        """Test we can integrate a single simplex with height zero."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        height = FaceMin(c)
        height[1] = 0
        i = EulerIntegrator()
        self.assertEqual(i.integrate(c, height), 0)


    def test1simplex1(self):
        """Test we can integrate a single simplex with height one."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        height = FaceMin(c)
        height[1] = 1
        i = EulerIntegrator()
        self.assertEqual(i.integrate(c, height), 1)


    def test1edge(self):
        '''Test we can integrate an edge.'''
        c = SimplicialComplex()
        n1 = c.addSimplex()
        n2 = c.addSimplex()
        e1 = c.addSimplex(fs=[n1, n2])
        height = FaceMin(c)
        height[n1] = 1
        height[n2] = 0
        i = EulerIntegrator()
        self.assertEqual(i.integrate(c, height), 1)


    def test1tri(self):
        '''Test we can integrate a triangle.'''
        c = SimplicialComplex()
        n1 = c.addSimplex()
        n2 = c.addSimplex()
        n3 = c.addSimplex()
        e1 = c.addSimplex(fs=[n1, n2])
        e2 = c.addSimplex(fs=[n1, n3])
        e3 = c.addSimplex(fs=[n2, n3])
        t1 = c.addSimplex(fs=[e1, e2, e3])
        height = FaceMin(c)
        height[n1] = 1
        height[n2] = 0
        height[n3] = 1
        i = EulerIntegrator()
        self.assertEqual(i.integrate(c, height), 1)


if __name__ == '__main__':
    unittest.main()
