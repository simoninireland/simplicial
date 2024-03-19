# Tests of discrete Morse theory
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


class MorseTests(unittest.TestCase):

    def setUp(self):
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ])
        c.addSimplex(id = 13, fs = [ 1, 3 ])
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])
        self._c =c


    # ---------- Morse functions ----------

    def testConstant(self):
        '''Test a constant function is not Morse.'''
        f = SimplicialFunction(self._c, lambda sf, c, s: 10)
        self.assertFalse(f.isMorse())


    def testOrder(self):
        '''Test a simplex order function is Morse.'''
        f = SimplicialFunction(self._c, lambda sf, c, s: c.orderOf(s))
        self.assertTrue(f.isMorse())


    def testOrderOneOff(self):
        '''Test we can have one direction of anti-sense.'''
        f = SimplicialFunction(self._c, lambda sf, c, s: c.orderOf(s) if s != 23 else 10)
        self.assertTrue(f.isMorse())


    def testOrderTwoOff(self):
        '''Test we can't have more than one direction of anti-sense.'''
        f = SimplicialFunction(self._c, lambda sf, c, s: c.orderOf(s) if s not in [23, 13] else 10)
        self.assertFalse(f.isMorse())


if __name__ == '__main__':
    unittest.main()
