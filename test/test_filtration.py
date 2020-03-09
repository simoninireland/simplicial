# Tests of filtrations
#
# Copyright (C) 2017--2020 Simon Dobson
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
import six
from simplicial import *

class FiltrationTests(unittest.TestCase):

    def testSimple(self):
        '''Test basic behaviour.'''
        f = Filtration()
        f.addSimplex(id = 1)
        f.addSimplex(id = 2)
        six.assertCountEqual(self, f.simplices(), [ 1, 2 ])
        f.setIndex(0.5)
        six.assertCountEqual(self, f.simplices(), [ 1, 2 ])
        
