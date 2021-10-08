# Tests of reading and writing in JSON format
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
from simplicial.file import *
import json

class JSONTests(unittest.TestCase):

    def testEmpty( self ):
        """Test we can write and read an empty complex."""
        c = SimplicialComplex()
        d = json.loads(as_json(c), object_hook = as_simplicial_complex)

        self.assertEqual(len(d.simplices()), 0)
        self.assertEqual(len(c.simplices()), 0)

    def test0( self ):
        """Test we can write and read a complex with a single 0-simplex."""
        c = SimplicialComplex()
        c.addSimplex(id = 1, attr = dict(name = 'me', pos = [ 1, 2 ]))
        d = json.loads(as_json(c), object_hook = as_simplicial_complex)

        self.assertCountEqual(d.simplices(), c.simplices())
        self.assertCountEqual(d[1].keys(), c[1].keys())
        for k in d[1].keys():
            self.assertEqual(d[1][k], c[1][k])

    def test0s( self ):
        """Test we can write and read a complex with multiple 0-simplices."""
        c = SimplicialComplex()
        c.addSimplex(id = 1, attr = dict(name = 'me', pos = [ 1, 2 ]))
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 4, attr = dict(name = 'him', pos = [ 1, 4 ]))
        d = json.loads(as_json(c), object_hook = as_simplicial_complex)

        self.assertCountEqual(d.simplices(), c.simplices())
        self.assertCountEqual(d[1].keys(), c[1].keys())
        for s in d.simplices():
            for k in d[s].keys():
                self.assertEqual(d[1][k], c[1][k])


    def test1s( self ):
        """Test we can write and read a complex with multiple 1-simplices."""
        c = SimplicialComplex()
        c.addSimplexWithBasis(bs = [ 1, 2 ], id = 12)
        c.addSimplexWithBasis(bs = [ 2, 3 ], id = 23)
        c.addSimplexWithBasis(bs = [ 1, 3 ], id = 13)
        d = json.loads(as_json(c), object_hook = as_simplicial_complex)

        self.assertCountEqual(d.simplices(), c.simplices())
        for s in d.simplicesOfOrder(1):
            self.assertCountEqual(d.faces(s), d.faces(s))


if __name__ == '__main__':
    unittest.main()
