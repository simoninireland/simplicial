# Tests of Euler computations over large random planar complexes
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
import numpy
import copy
from simplicial import *

class RandomPlanesTests(unittest.TestCase):

    SizeOfRandomPlanes = 100
    
    def setUp( self ):
        """Create a large randomly-triangulated planar complex."""
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
        boundary = list(copy.copy(c.simplicesOfOrder(1)))
        
        # add random triangles
        for n in range(self.SizeOfRandomPlanes):
            # choose a random boundary edge
            i = (int) (numpy.random.random() * len(boundary))
            e0 = boundary[i]

            # add a new triangle to that edge
            vs = list(c.faces(e0))
            self.assertEqual(len(vs), 2)
            v2 = c.addSimplex()
            e1 = c.addSimplex(fs = [ vs[0], v2 ])
            e2 = c.addSimplex(fs = [ vs[1], v2 ])
            t1 = c.addSimplex(fs = [ e0, e1, e2 ])

            # update the boundary
            del boundary[i]
            boundary.extend([ e1, e2 ])

        # store the complex and the final boundary
        self._complex = c
        self._boundary = boundary
            
    def testCreation( self ):
        """Test the setup routine."""
        pass

    def _isInternalTriangle(self, t):
        """Check whether the given 2-simplex is internal to the plane"""
        for f in list(self._complex.faces(t)):
            if len(self._complex.faceOf(f)) == 1:
                # face is an edge of the entire place
                #print("face was outside edge")
                return False
        return True

    def testEuler( self ):
        """Test the Euler characteristic calculations on large planes."""
        
        # plane
        self.assertEqual(self._complex.eulerCharacteristic(), 1)

        # plane with a random triangle removed from the middle
        ts = list(self._complex.simplicesOfOrder(2))
        while True:
            # pick a random triangle
            t = ts[int(numpy.random.random() * len(ts))]
            if not self._isInternalTriangle(t):
                # triangle isn't internal, try again
                continue

            # if we get here, we've picked an interior triangle
            break

        fs = list(self._complex.faces(t))
        self.assertEqual(len(fs), 3)
        self._complex.deleteSimplex(t)
        self.assertEqual(self._complex.eulerCharacteristic(), 0)

        # plane with another adjacent triangle removed
        f = fs[int(numpy.random.random() * len(fs))]
        ts = list(self._complex.faceOf(f))
        self.assertEqual(len(ts), 1)
        t = ts[0]

        self._complex.deleteSimplex(t)
        self.assertEqual(self._complex.eulerCharacteristic(), -1)

        # plane with the "strut" removed between the two adjacent triangles,
        # thereby collapsing the two holes into one
        self._complex.deleteSimplex(f)
        self.assertEqual(self._complex.eulerCharacteristic(), 0)
