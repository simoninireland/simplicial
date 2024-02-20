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

from typing import TypeVar, Callable, Dict, Generic
from simplicial import SimplicialComplex, Simplex


# Type variables
A = TypeVar('A')


# ---------- Representation ----------

class SFRepresentation(Generic[A]):

    def __init__(self):
        self._complex = None


    # ---------- Access ----------

    def setComplex(self, c: SimplicialComplex):
        '''Set the underlying complex that is the domain
        of the function.

        :params c: the complex'''
        self._complex = c


    def complex(self) -> SimplicialComplex:
        '''Return the underlying complex that is the domain
        of the function.

        :returns: the complex'''
        return self._complex


     # ---------- Sub-class interface ----------

    def setValueForSimplex(self, s: Simplex, v: A):
        '''Set the value associated with a simplex.

        A representation may not allow values to be explicitly set, in
        which case this method should raise ValueError. (This is the
        default behaviour.)

        :param s: the simplex
        :param a: the value

        '''
        raise ValueError('Can\'t set explicit values in simplicial function')


    def valueForSimplex(self, s: Simplex) -> A:
        '''Retrieve the value associated with a simplex.

        This method must be overridden by sub-classes.

        :param s: the simplex
        :returns the value'''
        raise NotImplementedError('valueForSimplex')


    def reset(self):
        '''Reset the function.

        Many functions are expensive to compute. This method should be
        called whenever the underlying simplicial complex is changed,
        to allow functions to recompute themselves or flush cached
        values.

        The default does nothing.

        '''
        pass


class AttributeSFRepresentation(SFRepresentation[A]):
    '''A simplicial function representation based on an attribute of simplices
    in a complex.

    Since the function needs to be total over the simplices, a default
    value can be provided to be returned for simplices without the
    given attribute.

    The simplex must be part of the complex.

    :param attr: the attribute
    :param default: (optional) default value (defaults to None)

    '''

    def __init__(self, attr: str, default: A = None):
        super().__init__()
        self._attr = attr
        self._default = default


    def valueForSimplex(self, s: Simplex) -> A:
        '''Extract the attribute associated with the simplex.
        If there is no such attribute, return the default value.

        :param s: the simplex
        :returns: the attribute value on that simplex or the default value'''
        self.complex().containsSimplex(s, fatal=True)
        return self.complex().getAttributes(s).get(self._attr, self._default)


class LiteralSFRepresentation(SFRepresentation[A]):
    '''A simplicial function representation that stores arbitrary values
    associated with simples.

    Since the function needs to be total over the simplices, a default
    value can be provided to be returned for simplices without the
    given attribute.

    The simplex must be part of the complex.

    :param default: (optional) default value (defaults to None)

    '''

    def __init__(self, default: A = None):
        super().__init__()
        self._default = default
        self._dict: Dict[Simplex, A] = dict()


    def setValueForSimplex(self, s: Simplex, v: A):
        '''Set the value associated with a simplex.

        :param s: the simplex
        :param a: the value'''
        self.complex().containsSimplex(s, fatal=True)
        self._dict[s] = v


    def valueForSimplex(self, s: Simplex) -> A:
        '''Extract the attribute associated with the simplex.
        If there is no such attribute, return the default value.

        :param s: the simplex
        :returns: the attribute valuye on that simlex or the default value'''
        self.complex().containsSimplex(s, fatal=True)
        return self._dict.get(s, self._default)


class ComputedSFRepresentation(SFRepresentation[A]):
    '''A simplicial function representation computed for each simplex.

    This representation has no default value: the function passed
    must therefore be total.

    The simplex must be part of the complex. This is checked before
    calling the function.

    :param f: function from complex and simplex to value
    '''

    def __init__(self, f: Callable[[SimplicialComplex, Simplex], A]):
        super().__init__()
        self._f = f


    # ---------- Access ----------

    def f(self) -> Callable[[SimplicialComplex, Simplex], A]:
        '''Return the underlying function

        :returns: the function'''
        return self._f


    def valueForSimplex(self, s: Simplex) -> A:
        '''Return the value of the function on the given simplex.

        :param s: the simplex
        :returns: the value for that simplex'''
        self.complex().containsSimplex(s, fatal=True)
        return self.f()(self.complex(), s)


# ---------- Top-level class ----------

class SimplicialFunction(Generic[A]):
    '''A total function from simplices to values.

    Simplicial functions can be used to capture a range of operations
    on complexes, each with particular constraints on the range of values
    produced.

    The default constructor takes a range of parameters to cover the
    different common cases:

    - a function from complex and simplex to value
    - a string, representing an attribute on simplices
    - a default value

    These are used to choose an appropriate representation,
    repectively using the funciton, the attributes, or a literal
    function where youn provide the mapping manually. It is also
    possible to provide a specific representation. (This approach is
    awkward, but it saves exposing all the representations in
    application code.)

    :param c: the simplicial complex
    :param f: (optional) a function to determine values
    :param attr: (optional) an attribute name
    :param default: (optional) default value
    :param rep: (optional) representation

    '''

    def __init__(self, c: SimplicialComplex,
                 f:  Callable[[SimplicialComplex, Simplex], A] = None,
                 attr: str = None,
                 default: A = None,
                 rep: SFRepresentation[A] = None):
        if rep is None:
            # choose a representation
            if f is not None:
                rep = ComputedSFRepresentation(f)
            elif attr is not None:
                rep = AttributeSFRepresentation(attr, default=default)
            else:
                rep = LiteralSFRepresentation(default=default)
        self._representation = rep
        rep.setComplex(c)


    # ---------- Access ----------

    def complex(self) -> SimplicialComplex:
        '''Return the underlying complex that is the domain
        of the function.

        :returns: the complex'''
        return self._representation.complex()


    def reset(self):
        '''Reset the function if the underlying simplicial complex is changed.
        This allows representations to re-compute themselves, clear caches,
        or take any other action. It is passed directly to the representation
        for action.
        '''
        self._representation.reset()


    # ---------- Callable and dict interfaces ----------

    def __call__(self, s: Simplex) -> A:
        '''Retrieve the value associated with a simplex. This method
        makes trhe simplicial function behave like any other Python
        function.

        All simplicial functions are total, so a value will
        alweays be returned for all simplices. Different representations
        may have different defaults.

        :param s: the simplex
        :returns the value

        '''
        return self._representation.valueForSimplex(s)


    def __getitem__(self, s: Simplex) -> A:
        '''Retrieve the value associated with a simplex. This method
        allows the simplicial function to behave more like a Python
        dict.

        All simplicial functions are total, so a value will
        alweays be returned for all simplices. Different representations
        may have different defaults.

        :param s: the simplex
        :returns the value

        '''
        return self._representation.valueForSimplex(s)


    def __setitem__(self, s: Simplex, v: A):
        '''Retrieve the value associated with a simplex.

        Not all representations allow explicit values to be set. If
        not, ValueError is raised.

        :param s: the simplex
        :param v: the value

        '''
        self._representation.setValueForSimplex(s, v)
