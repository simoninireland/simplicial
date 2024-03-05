# Discrete simplicial vector fields
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

from typing import Tuple, Callable, Final
from simplicial import SimplicialComplex, Simplex, SimplicialFunction, SFRepresentation


# Type aliases
DiscreteVector = Tuple[Simplex, float]  #: A discrete vector with a direction (simplex) and magnitude.


class DiscreteVectorField(SimplicialFunction[DiscreteVector]):
    '''A discrete vector field over a simplicial complex.

    A discrete vector field assigns a discrete vector to each simplex.
    A discrete vector consists of a direction, represented by a
    simplex, and a magnitude, represented by a float. Taking a simplex
    as the attachment point of a discrete vector, the vector's
    direction must be a face or coface of the attachment point. Each
    attachment point has exactly one attached vector, which may be
    zero.

    One way to visualise a discrete vector field is as an arrow
    attached to each simplex, pointing in the direction of a face or
    coface of that simplex, with the magnitude of the vector defining
    the length of the arrow.

    The default constructor takes a range of parameters to cover the
    different common cases as with :class:`SimplicialFunction`, or an
    explicitly-chosen representation.

    No checks are made on the sense of the attribute or functional
    cases, for example ensuring that the vector points in the right
    direction. For the literal case, however, a check is made on
    direction when a vector is added. (The field can also be rendered
    invalid by removing simplicies from the underlying complex.)

    :param c: (optional) the simplicial complex
    :param f: (optional) a function to determine vector values
    :param attr: (optional) an attribute name
    :param default: (optional) default value (defaults to a null vector)
    :param rep: (optional) representation

    '''

    NULL_VECTOR: Final[DiscreteVector] = (None, 0.0)     #: The discrete null vector.


    @staticmethod
    def isNullVector(dv: DiscreteVector):
        '''Test if the given vector is the null vector, having a
        direction of None and magnitude of 0.0.

        :param dv: the vector
        :returns: True if the vector is null'''
        return (dv[0] is None and dv[1] == 0.0)


    def __init__(self, c: SimplicialComplex = None,
                 f: Callable[[SimplicialComplex, Simplex], DiscreteVector] = None,
                 attr: str = None,
                 default: DiscreteVector = NULL_VECTOR,
                 rep: SFRepresentation[DiscreteVector] = None):
        super().__init__(c, f, attr, default, rep)


    # ---------- Access ----------

    def __setitem__(self, s: Simplex, v: DiscreteVector):
        '''If setting is allowed, ensure that the new value is
        sensible. "Sensible" in this case means that the discrete
        vector is either the null vector or its direction is a face or
        coface of the simplex to which it is being attached,

        :param s: the simplex
        :param v: the vector

        '''

        # check for sense
        c = self.complex()
        if not (self.isNullVector(v) or (s in c.faces(s)) or (s in c.cofaces(s))):
            raise ValueError(f'Vector is non-null and does not point in a legal direction for {s}')

        # if we get here, do the assignment
        super()[s] = v


    # ---------- Tests ----------

    def isMorseField(self) -> bool:
        '''A Morse field is a discrete vector field induced by a Morse
        function over a complex.

        '''
        pass
