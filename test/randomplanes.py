# Tests of Euler computations over large random planar complexes
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
import copy
import numpy
from simplicial import *

class RandomPlanesTests(unittest.TestCase):

    SizeOfRandomPlanes = 1000
    
    def setUp( self ):
        '''Create a large random triangulated planar complex.'''
        c = SimplicialComplex()

        # create the first triangle
        c.addSimplex(id = 1)
        c.addSimplex(id = 2)
        c.addSimplex(id = 3)
        c.addSimplex(id = 12, fs = [ 1, 2 ]) 
        c.addSimplex(id = 13, fs = [ 1, 3 ]) 
        c.addSimplex(id = 23, fs = [ 2, 3 ])
        c.addSimplex(id = 123, fs = [ 12, 23, 13 ])

        # the initial boundary is the set of edges
        boundary = copy.copy(c.simplicesOfOrder(1))
        
        # add random triangles
        for n in xrange(self.SizeOfRandomPlanes):
            # choose a random boundary edge
            i = int(numpy.random.random() * len(boundary))
            e0 = boundary[i]

            # add a new triangle to that edge
            vs = c.faces(e0)
            v2 = c.addSimplex()
            e1 = c.addSimplex(fs = [ vs[0], v2 ])
            e2 = c.addSimplex(fs = [ vs[1], v2 ])
            t1 = c.addSimplex(fs = [ e0, e1, e2 ])

            # update the boundary
            del boundary[i]
            boundary = boundary + [ e1, e2 ]

        # store the complex and the final boundary
        self._complex = c
        self._boundary = boundary
            
    def testCreation( self ):
        '''Test the setup routine.'''
        pass

    def testEuler( self ):
        '''Test the Euler characteristic calculations on large planes.'''
        
        # plane
        self.assertEqual(self._complex.eulerCharacteristic(), 1)

        # plane with a random triangle removed
        ts = self._complex.simplicesOfOrder(2)
        i = int(numpy.random.random() * len(ts))
        fs = self._complex.faces(ts[i])    # for next test
        self._complex.deleteSimplex(ts[i])
        self.assertEqual(self._complex.eulerCharacteristic(), 0)

        # plane with another adjacent triangle removed
        i = int(numpy.random.random() * len(fs))
        ts = self._complex.partOf(fs[i])
        self.assertEqual(len(ts), 2)
        self._complex.deleteSimplex(ts[1])
        self.assertEqual(self._complex.eulerCharacteristic(), -1)

        # plane with the "strut" removed between the two adjacent triangles
        self._complex.deleteSimplex(ts[0])
        self.assertEqual(self._complex.eulerCharacteristic(), 0)
        
        # plane with a random number of non-adjacent triangles removed
        # TBD
