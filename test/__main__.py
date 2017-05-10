# Test suite
#
# Copyright (C) 2017 Simon Dobson
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

from .simplicialcomplex import SimplicialComplexTests
from .randomplanes import RandomPlanesTests
from .triangularlattice import TriangularLatticeTests
from .json_simplicial import JSONTests

simplicialcomplexSuite = unittest.TestLoader().loadTestsFromTestCase(SimplicialComplexTests)
randomplanesSuite = unittest.TestLoader().loadTestsFromTestCase(RandomPlanesTests)
triangularlatticeSuite = unittest.TestLoader().loadTestsFromTestCase(TriangularLatticeTests)
jsonSuite = unittest.TestLoader().loadTestsFromTestCase(JSONTests)

suite = unittest.TestSuite([ simplicialcomplexSuite,
                             randomplanesSuite,
                             triangularlatticeSuite,
                             jsonSuite
                           ])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite)
