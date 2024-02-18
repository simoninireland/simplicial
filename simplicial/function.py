# Simplicial functions
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

from typing import TypeVar, Callable
from simplicial import SimplicialComplex, Simplex


# Type variables
A = TypeVar('A')


class SimplicialFunction:
    '''A total function from simplices to values.

    Simplicial functions can be used to capture a range of operations
    on complxes, each with particular constraints on the range of values
    produced.

    :param c: the simplicial complex
    '''

    def __init__(self, c: SimplicialComplex):
        self._c = c


    # ---------- Access ----------

    def complex(self) -> SimplicialComplex:
        '''Return the underlying complex trhat is the domain
        of the function.

        :returns: the complex'''
        return self._c


    # ---------- Sub-class interface ----------

    def valueForSimplex(self, s: Simplex) -> A:
        '''Retrieve the value associated with a simplex.

        :param s: the simplex
        :returns the value'''
        raise NotImplementedError('valueForSimplex')


    # ---------- Callable interface ----------

    def __call__(self, s: Simplex) -> A:
        '''Retrieve the value associated with a simplex.

        This is equivalent to calling :meth:`valueForSimplex`.

        :param s: the simplex
        :returns the value'''
        return self.valueForSimplex(s)


# ---------- Implementations ----------

class AttributeSF(SimplicialFunction):
    '''A simplicial function based on an attribute of simplices
    in a complex.

    Since the function needs to be total over the simplices, a default
    value can be provided to be returned for simplices without the
    given attribute.

    :param attr: the attribute
    :param default: (optional) default value (defaults to None)

    '''

    def __init__(self, c: SimplicialComplex, attr: str, default: A = None):
        super().__init__(c)
        self._attr = attr
        self._default = default


    def valueForSimplex(self, s: Simplex) -> A:
        '''Extract the attribute associated with the simplex.
        If there is no such attribute, return the default value.

        :param s: the simplex
        :returns: the attribute valuye on that simlex or the default value'''
        return self.complex().getAttributes(s).get(self._attr, self._default)


class ComputedSF(SimplicialFunction):
    '''A simplicial function computed for each simplex.

    The functionc an be provided as an argument or by sub-classing and
    ovrriding the :meth:`valueForSimplex` method.

    :param f: (optional) function from complex and simplex to value
    '''

    def __init__(self, c: SimplicialComplex, f: Callable[[SimplicialComplex, Simplex], A]):
        super().__init__(c)
        self._f = f


    # ---------- Access ----------

    def f(self) -> Callable[[SimplicialComplex, Simplex], A]:
        '''Return the underlying function

        :returns: the function'''
        return self._f


    def valueForSimplex(self, s: Simplex) -> A:
        '''Return the value of the function on the givem simplex.

        :param s: the simplex
        :returns: the value for that simplex'''
        self.f()(self.complex(), s)
