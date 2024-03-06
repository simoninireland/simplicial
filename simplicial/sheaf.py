# Sheaves
#
# Copyright (C) 2024 Simon Dobson
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

from typing import TypeVar, Callable, List
from simplicial import SimplicialComplex, Simplex, SimplicialFunction, SFRepresentation

# Type variables
A = TypeVar('A')


# Type aliases
RestrictionMap = Callable[[SimplicialComplex, Simplex], A]         #: A restriction map from the stalk at a simplex to the stalk at its coface.
ReductionMap = Callable[[SimplicialComplex, Simplex, List[A]], A]  #: A reduction map for selecting values from a stalk based on the values of its faces.


class Sheaf(SimplicialFunction[A]):
    '''A sheaf over a simplicial complex.

    A sheaf is a simplicial function with values provided explicitly for
    0-simplices. Values for higher simplices are computed using two maps:

    - a *restriction map* that selects a value at each simplex; and
    - a *reduction map* that takes the values selected for the faces
      of a simplex and returns a single composite value.

    By default the restriction map is the identity over the underlying
    function representation, and the reduction map forces the values at
    all faces to be equal.

    :param c: (optional) the simplicial complex
    :param f: (optional) a function to determine values
    :param attr: (optional) an attribute name
    :param default: (optional) default value
    :param rep: (optional) representation
    :param restrict: (optional) the restriction map
    :param reduce: (optional) the reduction map
    '''

    def __init__(self, c: SimplicialComplex = None,
                 f:  Callable[[SimplicialComplex, Simplex], A] = None,
                 attr: str = None,
                 default: A = None,
                 rep: SFRepresentation[A] = None,
                 restrict: RestrictionMap = None,
                 reduce: ReductionMap = None):
        # fill in default maps
        if restrict is None:
            # use an identity map if none is provided
            restrict = self.identity
        if reduce is None:
            # by default all restricted values must be equal
            reduce = self.equality

        # create the sheaf
        super().__init__(c, f, attr, default, rep)
        self._restrict = restrict
        self._reduce = reduce


    # ---------- Default restriction and reduction maps ----------

    def identity(self, c: SimplicialComplex, s: Simplex) -> A:
        '''The identity restriction map simply passes a value through.

        :param c: the complex
        :param s: the simplex
        :returns: the value from the stalk of the sheaf at s'''
        return self.representation().valueForSimplex(s)


    def equality(self, c: SimplicialComplex, s: Simplex, vs: List[A]) -> A:
        '''Reduce face stalk values by equality. Each value must be the
        same (equal), and this value is then used as the value in
        the stalk at s.

        If all values are not equal, and exception is raised.

        :param c: the complex
        :param s: the simplex
        :param vs: the list of values from the faces of s
        :returns: the value from the stalk of the sheaf at s
        '''
        v0 = vs[0]
        for i in range(1, len(vs)):
            if v0 != vs[i]:
                raise ValueError(f'Values of face stalks of simplex {s} are not equal: {v0} and {vs[i]}')
        return v0


    # ---------- Values at stalks ----------

    def _valueAt(self, c: SimplicialComplex, s: Simplex) -> A:
        '''Compute the value of the sheaf at s.

        This recursively descends from s to its basis, the values of
        which are given directly by the repesentation. At higher
        simplices the values of the faces are restricted using the
        restriction map, and then all reduced using the reduction map
        to yield a value at s.

        :param c: the complex
        :param s: the simplex
        :returns: the value from the stalk at s

        '''

        # for 0-simplices, get the value
        if c.orderOf(s) == 0:
            return self.representation().valueForSimplex(s)

        # for higher simplices, recursively restrict and reduce
        vs = [self._restrict(c, t) for t in c.faces(s)]
        v = self._reduce(c, s, vs)
        print(f'{s} -> {v}')
        return v


    def __getitem__(self, s: Simplex) -> A:
        '''Retrieve the value from the section at s.

        :param s: the simplex
        :returns the value

        '''
        return self._valueAt(self.complex(), s)


    def __setitem__(self, s: Simplex, v: A):
        '''Set the value associated with a simplex.

        Sheaves only allow values to be set at the 0-simplices.

        :param s: the simplex
        :param v: the value

        '''
        if self.complex().orderOf(s) != 0:
            o = self.complex().orderOf(s)
            raise ValueError(f'Can\'t assign a value to simplex {s} in a sheaf (order={o})')
        else:
            self._representation.setValueForSimplex(s, v)
