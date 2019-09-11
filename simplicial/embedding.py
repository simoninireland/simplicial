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

import math
import itertools

from simplicial import *


class Embedding(object):
    """The abstract embedding of a simplicial complex into a space. An embedding
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
    for complexes with irregular embeddings, while the latter is better-suited to
    regular embeddings. Explicit positions override computed positions, which allows
    small distortions to be applied easily to otherwise regular embeddings.

    It is also possible to override the distance metric to construct different ways
    of metricating a space. The default is n-dimensional Euclidean.

    Note that in most cases an embedding is based on simplex names, and so care needs to
    be taken when relabeling simplices in the underlying complex.

    :param c: the complex
    :param dim: the dimension of the embedding space (defaults to 2)

    """

    def __init__( self, c, dim = 2 ):
        self._complex = c          # underlying complicial complex
        self._dim = dim            # dimension of embedding space
        self._position = dict()    # cache of positions

    def dimension( self ):
        """Return the dimension of the embedding space.

        :returns: the dimension of the embedding space"""
        return self._dim
    
    def origin( self ):
        """Return the position of the origin of the embedding space.

        :returns: the origin as a list of zero co-ordinates"""
        return [ 0.0 ] * self.dimension()

    def complex( self ):
        """Return the underlying simplicial complex.

        :returns: the complex"""
        return self._complex
    
    def distance(self, p, q ):
        """Compute the distance between two points. This implementation
        returns the normal n-dimensional Euclidean distance.

        :param p: one point
        :param q: the other point
        :returns: the distance between them"""
        sumsq = 0.0
        for d in range(self.dimension()):
            sumsq = sumsq + math.pow(q[d] - p[d], 2)
        return math.sqrt(sumsq)


    # ----- Positioning simplices -----

    def positionSimplex( self, s, pos ):
        """Define an explicit position for a simplex.

        :param s: the simplex
        :param pos: the position"""

        # check dimensions of position
        if len(pos) != self.dimension():
            raise ValueError("Providing a {pd}-dimensional position for an {ed}-dimensional embedding space".format(pd = len(pos),
                                                                                                                    ed = self.dimension()))
        self._position[s] = pos

    def positionOf( self, s ):
        """Return the position of a simplex in the complex when mapped through this
        embedding. Locations are only available for 0-simplices.

        :param s: the simplex
        :returns: the position of the simplex"""

        # check that we're being asked for an 0-simplex
        if self.complex().orderOf(s) > 0:
            raise ValueError("Can only embed 0-simplices")

        if s not in self._position.keys():
            # no explicit position, so compute it and cache the result            
            self._position[s] = self.computePositionOf(s)
        return self._position[s]

    def computePositionOf( self, s ):
        """Compute the position of the given 0-simplex under this embedding.
        The position returned should have the same dimensions as the
        embedding space. This method should be overridden by sub-classes:
        the default returns the origin for all 0-simplices.

        :param s: the simplex
        :returns: the position of the simplex"""
        return self.origin()
    
    def positionsOf( self, ss = None ):
        """Return a dict of positions for a given set of 0-simplices
        in the complex. The default is to return the positions of all
        0-simplices.

        :param ss: the simplices (defaults to all 0-simplices)
        :returns: a dict of positions"""

        # fill in default
        if ss is None:
            ss = self.complex().simplicesOfOrder(0)

        # retrieve positions and return
        pos = dict()
        for s in ss:
            pos[s] = self.positionOf(s)
        return pos

    def clearPositions( self ):
        """Clear the cache of simplex positions, forcing them all to be re-computed
        and/or re-specified. Use this if the underlying complex is changed."""
        self._position = dict()
        

    # ----- dict-like interface -----

    def __len__( self ):
        """The length of the embedding is the number of 0-simplices in the underlying
        simplicial complex, i.e., the number of simplices we can return positions for.

        :returns: the size of the embedding"""
        return self.complex().simplicesOfOrder(0)
    
    def __setitem__( self, s, pos ):
        """Dict-like interface to define an explicit position for a simplex.
        Equivalent to :meth:`positionSimplex`.

        :param s: the simplex
        :param pos: the position"""
        self.positionSimplex(s, pos)
        
    def __getitem__( self, s ):
        """Dict-like interface to return the position of a simplex in the
        complex when mapped through this embedding. Equivalent to :meth:`positionOf`.

        :param s: the simplex
        :returns: the position of the simplex"""
        return self.positionOf(s)

    def __contains__( self, s ):
        """Test if the embedding will embed the given simplex. Checks against the
        underlying simplicial complex.

        :param s: the simplex
        :returns: True if the embedding comtains the simplex"""
        return s in self.complex().simplicesOfOrder(0)


    # ----- Spatial constructions -----
    # sd: will be re-written to use M-trees
    
    def vietorisRipsComplex( self, eps ):
        """Construct the :term:`Vietoris-Rips complex` at scale eps corresponding to the
        given embedding. The resulting complex has the same 0-simplices as the
        embedding, with a simplex constructed between every collection of simplices
        that are mutually a distance eps or less apart.

        :param eps: the scale parameter
        :returns: the Vietoris-Rips complex at the given scale"""

        # create a new complex with the same 0-simplices as ourselves
        c = self.complex()
        vr = SimplicialComplex()
        ss = list(c.simplicesOfOrder(0))
        for s in ss:
            vr.addSimplex(id = s)

        # work out all pairs of 0-simplices within eps, adding a
        # 1-simplex between them
        n = len(ss)
        for i in range(n - 1):
            p = ss[i]
            for j in range(i + 1, n):
                q = ss[j]
                if self.distance(self.positionOf(p), self.positionOf(q)) <= eps:
                    # pair of 0-simplices within eps, add 1-simplex
                    vr.addSimplexWithBasis([p, q])

        # add higher simplices for collections of 0-simplices
        # mutally within eps, which is simply the flag complex
        # derived from the pairwise distances
        vr2 = vr.flagComplex()
        
        # return the populated complex
        return vr2
