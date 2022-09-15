# Generator functions for common complexes
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

import itertools
from typing import Optional, Any
from simplicial import SimplicialComplex, Attributes


# ---------- Basic structures ----------

def k_skeleton(k: int, c: Optional[SimplicialComplex] = None) -> SimplicialComplex:
    '''Create the skeleton of a k-simplex, consisting
    of (k + 1) 0-simplices for the basis and k(k - 1)/2 1-simplices
    for the skeleton. Note that this doesn't create the k-simplex
    itself, just a skeleton of points and lines: to get the simplex itself
    use :func:`k_simplex`. If no complex is provided, a new one is created.

    :param k: the order of simplex to create
    :param c: (optional) the complex to create into
    :returns: a complex containing the skeleton'''

    # fill in defaults
    if c is None:
        c = SimplicialComplex()

    # construct the 0-simplices
    ss = []
    for i in range(k + 1):
        ss.append(c.addSimplex())

    # construct the 1-simplices
    for p in itertools.combinations(ss, 2):
        c.addSimplex(fs=list(p))

    # return the complex we added into
    return c


def k_simplex(k: int, id: Any = None,
              attr: Optional[Attributes] = None,
              c: Optional[SimplicialComplex] = None) -> SimplicialComplex:
    '''Create a k-simplex. If no complex is provided, a new one is created.
    The top-level simplex can be named and given attributes; its faces
    will be "anonymous" and have names created for them.

    :param k: the order of simplex to create
    :param id: (optional) the name of the simplex created
    :param attr: (optional) attributes ot the top-level simplex
    :param c: (optional) the complex to create into
    :returns: the complex containing the new simplex'''

    # fill in defaults
    if c is None:
        c = SimplicialComplex()

    if k == 0:
        # it's an 0-simplex, just create a new one
        c.addSimplex(id=id, attr=attr)
    else:
        # create a basis of new simplices
        bs = []
        for i in range(k + 1):
            bs.append(c.addSimplex())

        # create the new simplex with this basis, which
        # will automatically create all the faces
        c.addSimplexWithBasis(bs, id=id, attr=attr)

    # return the complex we added into
    return c


def k_void(k: int, c: SimplicialComplex = None) -> SimplicialComplex:
    '''Create a (k + 1)-dimensional void or hole with a k-dimensional boundary -- or
    in other words all the faces of a (k + 1)-simplex without filling in the
    (k + 1) simplex itself.

    The numbering of holes is a bit confusing, but a cycle of edges
    (1-simplices) creates what is referred to as a 1-hole, even though
    it's a 2-dimensional structure.

    :param k: the order of simplex to create
    :param c: (optional) the complex to create into
    :returns: the complex containing the skeleton'''

    # this probably isn't the optimal way to do this, but it
    # maximises code reuse from the rest of the code base
    d = k_simplex(k + 1, c=c)
    sos = list(d.simplicesOfOrder(k + 1))
    d.deleteSimplex(sos[0])
    return d


# ---------- Larger example structures ----------

def ring(n: int, c: Optional[SimplicialComplex] = None) -> SimplicialComplex:
    '''Create a closed ring of n lines (1-simplices), where
    n is strictly greater than 2.

    :param n: the number of lines in the ring
    :param c: (optional) the complex to create into
    :returns: the complex containing the skeleton'''
    if n <= 2:
        raise ValueError(f'Can\'t create a ring of {n} <= 2 lines')

    # fill in defaults
    if c is None:
        c = SimplicialComplex()

    # construct the 0-simplices
    ss = []
    for i in range(n + 1):
        ss.append(c.addSimplex())

    # construct the 1-simplices
    for i in range(n - 1):
        c.addSimplex(fs=[ss[i], ss[i + 1]])
    c.addSimplex(fs=[ss[n - 1], ss[0]])

    # return the complex we added into
    return c
