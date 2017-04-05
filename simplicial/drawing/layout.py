# Layout routines for simplicial complexes
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

from simplicial import *

def triangular_lattice_positions( l ):
    '''Return a dictionary of positions for nodes (0-simplices) laid out in a 
    triangular lattice. Positions are normalised in the range [0, 1].
    
    :param l: the lattice
    :returns: a dict of positions'''
    r = l.rows()
    c = l.columns()
    
    pos = dict()
    rh = 1.0 / r                 # row height
    cw = 1.0 / (2 * c)           # column width
    
    ids = list(l.simplicesOfOrder(0))
    for i in xrange(r):
        for j in xrange(c):
            # compute position
            y = 1.0 - rh * i
            if i % 2 == 0:
                x = cw * (j * 2)
            else:
                # shift along for odd-numbered rows
                x = cw * ((j * 2) + 1)

            id = ids[0]
            ids = ids[1:]
            pos[id] = (x, y)
    return pos
