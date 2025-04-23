# Abstract base class of homology theories
#
# Copyright (C) 2024--2025 Simon Dobson
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

from typing import TypeVar, Generic

# There is a circular import between Homology and Chain at the typing level#
# (but not at the execution level)
# (See https://www.stefaanlippens.net/circular-imports-type-hints-python.html)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simplicial import Chain


# Type variables
A = TypeVar('A')


class Homology(Generic[A]):
    '''The base class of homology theories.

    Homology is usually referred to as "hole detector": it finds
    missing simplices (at different dimensions) in a complex. Homology
    is intimately tied to the idea of a :class:`Chain` of simplices
    that form a path (at a particular dimension) through the complex.
    '''

    def __init__(self):
        pass


    def isValidCoefficient(self, c) -> bool:
        '''Test whether a coefficient is valid under this homology theory.

        This method must be overridden by sub-classes.

        :param c: the coefficient
        :returns: True if the coefficient is valid'''
        raise NotImplementedError("isValidCoefficient")


    def boundary(self, ss: 'Chain[int]') -> 'Chain[int]':
        '''Return the :term:`boundary` of the given :term:`p-chain`.

        This will be a (p - 1)-chain of simplices from the complex.

        :param ss: a chain of simplices
        :returns: the boundary of the chain

        '''
        raise NotImplementedError("boundary")


# ---------- Standard homology theories ----------

class HomologyZ2(Homology[int]):
    '''Homology over a group {0, 1}.

    This is the simplest homology theory, with chains consisting
    of simplices that are either present (mapped to 1) or not (mapped to 0).
    This makes the operations a lot easier and faster to implement.'''


    # ---------- Coefficient checking ----------

    def isValidCoefficient(self, c) -> bool:
        '''Test whether a coefficient is valid under this homology theory.

        The coefficient must be either 0 or 1.

        :param c: the coefficient
        :returns: True if the coefficient is valid'''
        return isinstance(c, int) and (c == 0 or c == 1)


    # ---------- Boundaries ----------

    def boundary(self, ss: 'Chain[int]') -> 'Chain[int]':
        '''Return the :term:`boundary` of the given :term:`p-chain`.

        :param ss: a chain of simplices
        :returns: the boundary of the chain

        '''
        p = ss.order()
        bs = Chain(ss.complex(), p - 1)

        # an empty p-chain has no boundary
        if len(ss) == 0:
            return bs

        # check we have a valid chain
        ss.isChain(homology=self, fatal=True)

        # extract the boundary
        for s in ss:
            # extract the boundary of this simplex
            fs = self.faces(s)

            # any simplices in both sets aren't in the boundary; any not
            # in the boundary should be added
            for f in fs:
                if f in bs:
                    bs.removeSimplex(f)
                else:
                    bs.setValueForSimplex(f, 1)
        return bs
