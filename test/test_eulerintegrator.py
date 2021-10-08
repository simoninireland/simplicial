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

class EulerIntegratorTests(unittest.TestCase):

    def test0simplex(self):
        """Test we can integrate a single simplex with no height attribute."""
        c = SimplicialComplex()
        c.addSimplex(id = 1)
        i = EulerIntegrator('height')
        self.assertEqual(i.integrate(c), 0)

    def test1simplex0(self):
        """Test we can integrate a single simplex with height zero."""
        c = SimplicialComplex()
        c.addSimplex(id = 1, attr = dict(height = 0))
        i = EulerIntegrator('height')
        self.assertEqual(i.integrate(c), 0)

    def test1simplex1(self):
        """Test we can integrate a single simplex with height one."""
        c = SimplicialComplex()
        c.addSimplex(id = 1, attr = dict(height = 1))
        i = EulerIntegrator('height')
        self.assertEqual(i.integrate(c), 1)


if __name__ == '__main__':
    unittest.main()
