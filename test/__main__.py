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
from .homology import HomologyTests
from .flag import FlagTests
from .randomplanes import RandomPlanesTests
from .triangularlattice import TriangularLatticeTests
#from .drawing import DrawingTests
from .json_simplicial import JSONTests
from .mtree import MTreeTests
from .mtree_whitebox import MTreeWhiteboxTests
from .vr import VietorisRipsTests

simplicialcomplexSuite = unittest.TestLoader().loadTestsFromTestCase(SimplicialComplexTests)
homologySuite = unittest.TestLoader().loadTestsFromTestCase(HomologyTests)
flagSuite = unittest.TestLoader().loadTestsFromTestCase(FlagTests)
randomplanesSuite = unittest.TestLoader().loadTestsFromTestCase(RandomPlanesTests)
triangularlatticeSuite = unittest.TestLoader().loadTestsFromTestCase(TriangularLatticeTests)
#drawingSuite = unittest.TestLoader().loadTestsFromTestCase(DrawingTests)
jsonSuite = unittest.TestLoader().loadTestsFromTestCase(JSONTests)
#mtreeSuite = unittest.TestLoader().loadTestsFromTestCase(MTreeWhiteboxTests)
#mtreeSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(MTreeTests))
vrSuite = unittest.TestLoader().loadTestsFromTestCase(VietorisRipsTests)

suite = unittest.TestSuite([ simplicialcomplexSuite,
                             homologySuite,
                             flagSuite,
                             randomplanesSuite,
                             triangularlatticeSuite,
                             #drawingSuite,
                             jsonSuite,
                             #mtreeSuite,
                             vrSuite,
                           ])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite)
