# Chains
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

from typing import TypeVar, Optional
from simplicial import SimplicialComplex, SimplicialFunction, SFRepresentation, LiteralSFRepresentation, Homology


# Type variables
A = TypeVar('A')


class Chain(SimplicialFunction[A]):
    '''The base class of chains.

    A p-chain maps simplices of order p to values taken from some set A,
    called the coefficients of the chain. The value set is typically taken
    from a homology theory.

    Chains are simplicial functions that use the
    :class:`LiteralSFRepresentation` by default. It may or may not be
    possible to add and remove mappings.

    :param c: the simplicial complex
    :param p: the order of simplices in the chain
    :param rep: (optional) representation

    '''

    def __init__(self, c: SimplicialComplex, p: int, rep: Optional[SFRepresentation] = None):
        if rep is None:
            rep = LiteralSFRepresentation()
        super().__init__(c, rep=rep)
        self._order: int = p


    # ---------- Access ----------

    def order(self) -> int:
        '''Return the order of simplices in the chain.

        :returns: the order'''
        return self._order


    def isChain(self, homology: Optional[Homology] = None, fatal: Optional[bool] = False) -> bool:
        '''Test whether this is a legal chain.

        All the simplices in a p-chain must have order p, which is
        set when the chain is created. If homology is given, the
        coefficients of the chain must lie in the coefficient set of this
        homology theory (tested using :meth:`Homology.isValidCoefficient`).
        This involves evaluating the function for every simplex in its domain,
        and so may be expensive.

        If fatal is True a ValueError is raised if the chain isn't legal.

        :param homology: (optional) the homology theory of this chain
        :param fatal: (optional) raise a ValueError for illegal chains (defaults to False)
        '''
        c = self.complex()

        # check the orders of all simplices
        p = self.order()
        allOrder = all({c.orderOf(s) == p for s in self.domain()})

        # check the coefficients if we have a homology
        if homology is not None:
            allCoefficients = all({homology.isValidCoefficient(self[s]) for s in self.domain()})
        else:
            allCoefficients = True

        if allOrder and allCoefficients:
            return True
        else:
            if fatal:
                if not allOrder:
                    raise ValueError(f'Chain contains simplices not of order {p}')
                else:
                    raise ValueError('Chain contains invalid coefficients')
            else:
                return False
