# Tests of sheaves
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


class SheafTests(unittest.TestCase):

    def testConstantSheaf(self):
        '''Test we can construct a constant sheaf.'''
        c = SimplicialComplex()
        n1 = c.addSimplex(id=1)
        n2 = c.addSimplex(id=2)
        n3 = c.addSimplex(id=3)
        e1 = c.addSimplex(fs=[n1, n2], id=12)
        e2 = c.addSimplex(fs=[n1, n3], id=13)
        e3 = c.addSimplex(fs=[n2, n3], id=23)
        t1 = c.addSimplex(fs=[e1, e2, e3], id=123)

        F = Sheaf(c, f=lambda sf, c, s: 1)  # constant function
        for s in c.simplices():
            self.assertEqual(F[s], 1)

    def testNonConstantSheaf(self):
        '''Test a non-constant sheaf fails.'''
        c = SimplicialComplex()
        n1 = c.addSimplex(id=1)
        n2 = c.addSimplex(id=2)
        n3 = c.addSimplex(id=3)
        e1 = c.addSimplex(fs=[n1, n2], id=12)
        e2 = c.addSimplex(fs=[n1, n3], id=13)
        e3 = c.addSimplex(fs=[n2, n3], id=23)
        t1 = c.addSimplex(fs=[e1, e2, e3], id=123)

        F = Sheaf(c, f=lambda sf, c, s: s)   # identity on the simplex name, not constant
        with self.assertRaises(ValueError):
            # default equality reduction map will fail
            F[e1]


if __name__ == '__main__':
    unittest.main()
