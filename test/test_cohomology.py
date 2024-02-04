# Tests of cohomology operations
#
# Copyright (C) 2017--2024 Simon Dobson
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
from simplicial import *

class CoomologyTests(unittest.TestCase):

    def testEdgeCohomology(self):
        '''Test we can compute the cohomology of an edge.'''
        c = SimplicialComplex()
        c.addSimplex(id='a')
        c.addSimplex(id='b')
        c.addSimplex(['a', 'b'], 'ab')

        delta = c.coboundaryOperator(0)
        self.assertEqual(delta.shape, (1, 2))
        endpoints = numpy.array([1, 1]).T
        cb = (delta @ endpoints) % 2               # over Z_2 field
        self.assertEqual(cb, numpy.array([0]))


if __name__ == '__main__':
    unittest.main()
