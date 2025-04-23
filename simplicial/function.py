# Simplicial functions
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

from typing import TypeVar, Callable, Dict, Generic, Iterable, Optional
from simplicial import SimplicialComplex, Simplex


# Type variables
A = TypeVar('A')


# Helper types
SFValueFunction = Callable[['SimplicialFunction', SimplicialComplex, Simplex], A]  #: Function for computing the value at a simplex.
SFPredicate = Callable[['SimplicialFunction', SimplicialComplex, Simplex], bool]  #: Predicate for filtering simplices based on the value assigned to the by the function.


# ---------- Abstract representation  ----------

class SFRepresentation(Generic[A]):
    '''The abstract base class of simplicial function representations.

    The function being represented can be partial, and not return
    a value for every simplex in the complex.

    Some functions are expensive to compute, so it's entirely
    permissible to cache values. In this case, the function should
    also provide a :meth:`reset` method to clear the cache. Reset is
    called automatically if the underlying complex is re-assigned.

    '''

    def __init__(self):
        self._complex = None
        self._function = None


    # ---------- Access ----------

    def setComplex(self, c: SimplicialComplex):
        '''Set the underlying complex that is the domain
        of the function.

        This automatically calls :meth:`reset` to reset any cached
        values.

        :params c: the complex'''
        self._complex = c
        self.reset()


    def complex(self) -> Optional[SimplicialComplex]:
        '''Return the underlying complex that is the domain
        of the function.

        :returns: the complex'''
        return self._complex


    def setFunction(self, sf: 'SimplicialFunction'):
        '''Set the simplicial function being represented.

        :params sf: the function'''
        self._function = sf


    def function(self) -> 'SimplicialFunction':
        '''Return the simplicial function being represented.

        :returns: the function'''
        return self._function


     # ---------- Sub-class interface ----------

    def setValueForSimplex(self, s: Simplex, v: A):
        '''Set the value associated with a simplex.

        A representation may not allow values to be explicitly set, in
        which case this method should raise ValueError. (This is the
        default behaviour.)

        :param s: the simplex
        :param a: the value

        '''
        raise ValueError('Can\'t set explicit values in simplicial function representation')


    def domain(self) -> Iterable[Simplex]:
        '''Return the domain of the represented function.

        This method must be overridden by sub-classes.

        :returns: a set of simplices
        '''
        raise NotImplementedError('domain')


    def inDomain(self, s: Simplex) -> bool:
        '''Test whether a simplex is defined under the function.

        The default simply enumerates the domain and checks for the simplex.
        Representations may define more efficient approaches.

        :param s: the simplex
        :returns: True if the simplex is in the domain of the function
        '''
        return s in self.domain()


    def size(self) -> int:
        '''Return the size of the function's domain.

        The default simply enumerates the domain and computes its length.
        Representations may define more efficient approaches.

        :returns: the number of simplices in the domain'''
        return len(list(self.domain()))



    def removeSimplex(self, s: Simplex, fatal: bool = False):
        '''Remove the value associated with a simplex.

        This method must be overridden by sub-classes.

        :param s: the simplex
        :param fatal:  (optional) if True, raise an exception for non-chain values (defaults to False)'''
        raise NotImplementedError('valueForSimplex')


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


    def allSimplices(self, pred: SFPredicate) -> Iterable[Simplex]:
        '''Return all the simplices matching a given predicate.

        The set returned will be a (possibly equal) sub-set of the
        simplices in the function's :meth:`domain`.

        The default does a traverse of all the simplices: some
        representations may have a more efficient approach.

        :param pred: the predicate
        :returns: a set of simplices

        '''
        sf = self.function()
        c = self.complex()
        return {s for s in self.domain() if pred(sf, c, s)}



# ---------- Concrete representations  ----------

class AttributeSFRepresentation(SFRepresentation[A]):
    '''A simplicial function representation based on an attribute of simplices
    in a complex.

    The domain of the function is the simplcies with the given attribute.

    :param attr: the attribute
    :param default: (optional) default value (defaults to None)

    '''

    def __init__(self, attr: str):
        super().__init__()
        self._attr = attr


    def domain(self) -> Iterable[Simplex]:
        '''Return the domain of the function, the simplices with the attribute.

        :returns: all the simplices in the complex'''
        return self.complex().allSimplices(lambda c, s: self._attr in c.getAttributes(s))


    def valueForSimplex(self, s: Simplex) -> A:
        '''Extract the attribute associated with the simplex.

        If there is no such attribute, return the default value.

        :param s: the simplex
        :returns: the attribute value on that simplex or the default value'''
        return self.complex().getAttributes(s).get(self._attr, self._default)


class LiteralSFRepresentation(SFRepresentation[A]):
    '''A simplicial function representation that stores arbitrary values
    associated with simplices.

    :param default: (optional) default value (defaults to None)

    '''

    def __init__(self):
        super().__init__()
        self._dict: Dict[Simplex, A] = dict()


    def domain(self) -> Iterable[Simplex]:
        '''Return the domain of the function, all the simplices with values assigned.

        :returns: all the simplices in the complex'''
        return self._dict.keys()


    def size(self) -> int:
        '''Return the size of the function's domain.

        :returns: the number of simplices in the domain'''
        return len(self._dict)


    def inDomain(self, s: Simplex) -> bool:
        '''Test whether a simplex is defined under the function.

        :param s: the simplex
        :returns: True if the simplex is in the domain of the function
        '''
        return s in self._dict.keys()


    def setValueForSimplex(self, s: Simplex, v: A):
        '''Set the value associated with a simplex.

        :param s: the simplex
        :param a: the value'''
        self.complex().containsSimplex(s, fatal=True)
        self._dict[s] = v


    def removeSimplex(self, s: Simplex, fatal: bool = False):
        '''Remove the value associated with a simplex.

        A value can be removed even if it isn't in the function unless
        fatal is True, in whcih case a ValueError is raised. (The simplex
        must always be part of the complex, however.)

        :param s: the simplex
        :param fatal: (optional) if True, raise an exception for non-function values (defaults to False)'''
        self.complex().containsSimplex(s, fatal=True)
        if s in self._dict.keys():
            del self._dict[s]
        else:
            if fatal:
                raise ValueError(f'Simplex {s} not included in the chain')


    def hasValue(self, s: Simplex, fatal: bool = False) -> bool:
        '''Test if there is a value assigned to the simplex.
        If fatal is True, then an exception is raised if there is no value.

        Note that is a value isn't set and :meth:`valueForSimplex` is called,
        the default value will still be returned.

        :param s: the simplex
        :param fatal: (optional) if True, raise an exception for missing values (defaults to False)
        :returns: True if a value has been set'''
        if s in self._dict.keys():
            return True
        else:
            if fatal:
                raise ValueError(f'No value set for {s}')
            else:
                return False


    def valueForSimplex(self, s: Simplex) -> A:
        '''Extract the value associated with the simplex.

        :param s: the simplex
        :returns: the attribute valuye on that simplex or the default value'''
        self.complex().containsSimplex(s, fatal=True)
        return self._dict.get(s)


class ComputedSFRepresentation(SFRepresentation[A]):
    '''A simplicial function representation computed for each simplex.

    This representation has no default value: the function should
    therefore be total.

    :param f: function from complex and simplex to value

    '''

    def __init__(self, f: SFValueFunction):
        super().__init__()
        self._f = f


    # ---------- Access ----------

    def f(self) -> SFValueFunction:
        '''Return the underlying function

        :returns: the function'''
        return self._f


    def domain(self) -> Iterable[Simplex]:
        '''Return the domain of the function, which is the entire complex.

        :returns: all the simplices in the complex'''
        return self.complex().simplices()


    def size(self) -> int:
        '''Return the size of the function's domain.

        :returns: the number of simplices in the domain'''
        return len(self.complex())


    def valueForSimplex(self, s: Simplex) -> A:
        '''Return the value of the function on the given simplex.

        :param s: the simplex
        :returns: the value for that simplex'''
        self.complex().containsSimplex(s, fatal=True)
        return self.f()(self.function(), self.complex(), s)


class InferredSFRepresentation(ComputedSFRepresentation[A], LiteralSFRepresentation[A]):
    '''
    A mixed representation that takes both literal values *and*
    a function. If a value is provided for a simplex, that is the value
    of the function; otherwise the function is called to infer the value.

    An exception is raised if there is not enough information available
    to infer the value of any simplex: the conditions for this depend
    on the inference function itself.
    '''

    def __init__(self, f: SFValueFunction):
        super().__init__(f)


    def setValueForSimplex(self, s: Simplex, v: A):
        '''Set the value associated with a simplex.

        :param s: the simplex
        :param a: the value'''
        LiteralSFRepresentation.setValueForSimplex(self, s, v)


    def valueForSimplex(self, s: Simplex) -> A:
        '''Return either the value set for the simplex or
        a value inferred for it.

        :param s: the simplex
        :returns: the value'''
        if self.hasValue(s):
            return LiteralSFRepresentation.valueForSimplex(self, s)
        else:
            return ComputedSFRepresentation.valueForSimplex(self, s)


# ---------- Top-level class ----------

class SimplicialFunction(Generic[A]):
    '''A (possibly partial) function from simplices to values.

    Simplicial functions can be used to capture a range of operations
    on complexes, each with particular constraints on the range of values
    produced.

    The default constructor takes a range of parameters to cover the
    different common cases:

    - a function from simplicial function, complex, and simplex to value
    - a string, representing an attribute on simplices
    - a default value

    These are used to choose an appropriate representation,
    repectively using the function, the attributes, or a literal
    function where youn provide the mapping manually. (This approach
    is awkward, but it saves exposing all the representations in
    application code.)

    It is also possible to provide a specific representation which, if
    given, takes precedence over the other parameters (which are
    ignored).

    Another option is to override the :meth:`valueForSimplex` and
    :meth:`setValueForSimplex` methods on this class. In that case
    your constructor and overrides are responsible for managing the
    function's values.

    A simplicial function is "really" a function from complex and
    simplex to value. However, given the expense of computing some
    functions, we essentially curry the function by providing the
    complex separately, and treating the result as a function from
    simplex to value. This allows representations to pre-compute
    values or cache them to improve performance. The function can be
    "re-curried" at any time by calling :meth:`setComplex`, which will
    reset any optimisations. Clearly it makes no sense to call the
    function until a complex has been set.

    :param c: (optional) the simplicial complex
    :param f: (optional) a function to determine values
    :param attr: (optional) an attribute name
    :param rep: (optional) representation
    '''

    def __init__(self, c: Optional[SimplicialComplex] = None,
                 f: Optional[SFValueFunction] = None,
                 attr: Optional[str] = None,
                 rep: Optional[SFRepresentation[A]] = None):
        if rep is None:
            # choose a representation based on what arguments
            # we've been passed
            if f is not None:
                rep = ComputedSFRepresentation(f)
            elif attr is not None:
                rep = AttributeSFRepresentation(attr)
            else:
                rep = LiteralSFRepresentation()
        self._representation = rep

        # if there is any kind of representation, bind it
        # to this function
        self.setComplex(c)
        rep.setFunction(self)


    # ---------- Access ----------

    def setComplex(self, c: SimplicialComplex):
        '''Reset the underlying complex that is the domain
        of the function. This allows the same function to be used
        across complexes if desired.

        :params c: the complex'''
        self._representation.setComplex(c)


    def complex(self) -> Optional[SimplicialComplex]:
        '''Return the underlying complex that is the domain
        of the function.

        :returns: the complex'''
        return self._representation.complex()


    def representation(self) -> Optional[SFRepresentation]:
        '''Return the underlying representation of the function.

        :returns: the representation'''
        return self._representation


    def reset(self):
        '''Reset the function if the underlying simplicial complex is changed.
        This allows representations to re-compute themselves, clear caches,
        or take any other action. It is passed directly to the representation
        for action.
        '''
        self._representation.reset()


    def domain(self) -> Iterable[Simplex]:
        '''Return the domain of the function.

        The domain is all the simplices for which
        :meth:`valueForSimplex` will return a value.

        :returns: the simplices over which the function is defined'''
        return self._representation.domain()


    def simplices(self) -> Iterable[Simplex]:
        '''Return the simplices in the chain.

        This is a synonym for :meth:`domain`.

        :param s: the simplex
        :returns: a set of simplices'''
        return self.domain()


    def valueForSimplex(self, s: Simplex) -> A:

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


    def removeSimplex(self, s: Simplex, fatal: bool = False):
        '''Remove the value associated with a simplex.

        Not all representations allow simplices to be removed. If
        not, ValueError is raised.

        :param s: the simplex
        :param fatal:  (optional) if True, raise an exception for non-chain values (defaults to False)'''
        return self._representation.removeSimplex(s, fatal)


    def setValueForSimplex(self, s: Simplex, v: A):
        '''Set the value associated with a simplex.

        Not all representations allow explicit values to be set. If
        not, ValueError is raised.

        :param s: the simplex
        :param v: the value

        '''
        return self._representation.setValueForSimplex(s, v)


    def setValuesForSimplices(self, m: Dict[Simplex, A]):
        '''Set values for multiple simplices.

        :param m: a map of simplex to value'''
        for s in m.keys():
            self.setValueForSimplex(s, m[s])


    def allSimplices(self, pred: SFPredicate) -> Iterable[Simplex]:
        '''Return all the simplices matching a given predicate.

        The set returned will be a (possibly equal, possibly empty)
        sub-set of the simplices in the domain of the function.

        :param pred: the predicate
        :returns: a set of simplices

        '''
        return self._representation.allSimplices(pred)


    # ---------- Callable, iterable, and dict interfaces ----------

    def __call__(self, s: Simplex) -> A:
        '''Retrieve the value associated with a simplex. This method
        makes the simplicial function behave like any other Python
        function.

        All simplicial functions are total, so a value will
        alweays be returned for all simplices. Different representations
        may have different defaults.

        This method is equivalent to :meth:`valueForSimplex`, and by
        default simply calls that method.

        :param s: the simplex
        :returns the value

        '''
        return self.valueForSimplex(s)


    def __getitem__(self, s: Simplex) -> A:
        '''Retrieve the value associated with a simplex.

        This method is equivalent to :meth:`valueForSimplex`.

        :param s: the simplex
        :returns the value

        '''
        return self.valueForSimplex(s)


    def __setitem__(self, s: Simplex, v: A):
        '''Set the value associated with a simplex.

        This method is equivalent to :meth:`setValueForSimplex`.

        :param s: the simplex
        :param v: the value

        '''
        self.setValueForSimplex(s, v)


    def __contains__(self, s: Simplex) -> bool:
        '''Test whether a simplex is defined in the domain of the funciton.

        :param s: the simplex
        :returns: True if the simplex is assigned a value
        '''
        return self._representation.inDomain(s)


    def __len__(self) -> int:
        '''Return the length of the function, which is the size of its domain.

        The use of len makes more sense for (co)chains.

        :returns: the size of the domain
        '''
        return self._representation.size()


    def __iter__(self) -> Iterable[Simplex]:
        '''Return an iterator over the function.

        This iterates the domain.

        :returns: an iterator of simplices'''
        return iter(self.simplices())



    # ---------- Discrete Morse theory ----------

    def isMorse(self) -> bool:
        '''A discrete Morse function is a simplicial function :math:`f`
        such that:

        - at each simplex :math:`s`, for each simplex :math:`s < l`, there is
          at most one :math:`l` such that :math:`f(s) >= f(l)`; or
        - at each simplex :math:`s`, for each simplex :math:`l < s`, there is
          at most one :math:`l` such that :math:`f(l) >= fsl)`.

        Put another way, a Morse function generally increases with dimension
        except in at most one direction. This implies that the values
        of the simplicial function can be compared with <= and >=.

        Testing that a function is Morse is expensive, with worst-case
        time complexity of :math:`O(|s|^2)` time for a complex with
        :math:`|s|` simplices.

        :returns: True if the function is a Morse function
        '''
        c = self.complex()

        maxOrder = c.maxOrder()
        for k in range(maxOrder + 1):
            ss = c.simplicesOfOrder(k)
            for s in ss:
                v = self[s]

                # test all faces
                vs = sum([1 if self[l] >= v else 0 for l in c.faces(s)])
                if vs > 1:
                    return False

                # test all cofaces
                vs = sum([1 if self[l] <= v else 0 for l in c.cofaces(s)])
                if vs > 1:
                    return False

        # if we get here the values were all correct
        return True


    def isMorseCritical(self, s: Simplex) -> bool:
        '''Test whether the given simplex is critical in the sense of
        Morse theory. The values of the simplicial function must be
        comparable using <= and >=.

        :param s: the simplex
        :returns: True if the simplex is critical

        '''
        c = self.complex()
        v = self[s]

        # test all faces
        vs = sum([1 if self[l] >= v else 0 for l in c.faces(s)])
        if vs > 0:
            return False

        # test all cofaces
        vs = sum([1 if self[l] <= v else 0 for l in c.cofaces(s)])
        if vs > 0:
            return False

        # if we get here, we passed
        return True
