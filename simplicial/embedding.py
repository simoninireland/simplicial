# An embedding of a simplicial complex into a space
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

import numpy
import copy
import itertools


class Embedding(object):
    '''The abstract embedding of a simplicial complex into a space. An embedding
    associates a position with each 0-simplex in the complex, allowing spatial calculations
    to be performed.

    Embeddings serve two distinct purposes. Firstly, they admit spatial calculations
    as well as purely topological ones, which broadens the application areas to which
    we can apply simplicial ideas. Secondly, embeddings form the basis for visualisation,
    as they allow points (0-simplices) in a complex to be associated with points in
    an n-dimensional embedding space. This can result in more meaingful diagrams.

    An embedding can be specified in two distinct ways. Positions can be supplied
    explicitly for simplices by name. Alternatively, sub-clases can provide positioning
    functions that map simplices to positions using arbitrary code. The former is useful
    for comploexes with irregular embeddings, while the latter is better-suited to
    regular embeddings. Explicit positions override computed positions, which allows
    small distortions to be applied easily to otherwise regular embeddings.

    Note that in most cases an embedding is based on simplex names, and so care needs to
    be taken when relabeling simplices in a complex.

    :param dim: the dimension of the embedding space (defaults to 2)

    '''

    def __init__( self, dim = 2 ):
        self._dim = dim
        self._position = dict()

    def dimension( self ):
        '''Return the dimension of the embedding space.

        :retirns: the dimension of the embedding space'''
        return self._dim
    
    def origin( self ):
        '''Return the position of the origin of the embedding space.

        :returns: the origin as a list of zero co-ordinates'''
        return [ 0.0 ] * self.dimension()


    # ----- Positioning simplices -----

    def positionSimplex( self, s, pos ):
        '''Define an explicit position for a simplex.

        :param s: the simplex
        :param pos: the position'''

        # check dimensions of position
        if len(pos) != self.dimension():
            raise ValueError("Providing a {pd}-dimensional position for an {ed}-dimensional embedding space".format(pd = len(pos),
                                                                                                                    ed = self.dimension()))
        self._position[s] = pos

    def positionOf( self, s, c ):
        '''Return the position of a simplex when a complex is mapped through this
        embedding. Locations are only available for 0-simplices.

        :param s: the simplex
        :param c: the complex
        :returns: the position of the simplex'''

        # check that we're being asked for an 0-simplex
        if c.orderOf(s) > 0:
            raise ValueError("Can only embed 0-simplices")

        if s in self._position.keys():
            # simplex has an explicit position, return it
            return self._position[s]
        else:
            # no explicit position, so compute it
            return self.computePositionOf(s, c)

    def computePositionOf( self, s, c ):
        '''Compute the position of the given 0-simplex under this embedding.
        This method defaults to returning the origin for all 0-simplices.

        :param s: the simplex
        :param c: the complex
        :returns: the position of the simplex'''
        return self.origin()
    
    def positionsOf( self, c, ss = None ):
        '''Return a dict of positions for a given set oif 0-simplices
        in the complex. The default is to return the positions of all
        0-simplices.

        :param c: the complex
        :param ss: the simplices (defaults to all 0-simplices)
        :returns: a dict of positions'''

        # fill in default
        if ss is None:
            ss = c.simplicesOfOrder(0)

        # retrieve positions and return
        pos = dict()
        for s in ss:
            pos[s] = self.positionOf(s, c)
        return pos
    
