# Utility classes
#
# Copyright (C) 2017--2024 Simon Dobson
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

from collections import UserDict
from typing import TypeVar, Dict


# ---------- Isomorphisms ----------

# type variables
L = TypeVar('L')
R = TypeVar('R')


class Isomorphism(UserDict[L, R]):
    '''An isomorphism between two sets.

    An isomorphism is basically two hash tables back to back. Any
    mapping (k -> v) added to the forward table also adds a mapping (v
    -> k) in the reverse table. The :meth:`reverse` property
    makes the reverse accessible.

    The superclass constructor copies anmy initial data using a call
    to :meth:`__setitem__`, which therefore sets the reverse mapping
    too.

    :param initialData: (optional) initial dict contents (copied)

    '''

    def __init__(self, initialData: Dict[L, R] = None):
        self.backdata: Dict[R, L] = dict()
        super().__init__(initialData)


    def __setitem__(self, k: L, v: R):
        '''Set a key-value pair.

        This sets both the forward mapping (k -> v) and the reverse
        mapping (v -> k). An exception is raised if the pair is not
        unique in either direction.

        :param k: the key
        :param v: the value

        '''
        if k in self.data.keys():
            raise KeyError(f'Duplicate key  {k} (not an isomorphism)')
        if v in self.backdata.keys():
            raise KeyError(f'Duplicate value {v} (not an isomorphism)')
        self.data[k] = v
        self.backdata[v] = k


    def __delitem__(self, k: L):
        '''Delete a key.

        The reverse mapping (the value to whioch k is mapped) is also
        deleted. Reversing the reverse results in the original
        isomorphism. Any assignments made to the forward mapping are
        reflected in the revsre; similarly any assignments made in the
        reverse are reflected in the forward.

        :param k: the key

        '''
        v = self[k]
        del self.data[k]
        del self.backdata[v]


    @property
    def reverse(self) -> 'Isomorphism':
        '''The reverse mapping.

        If there is a mapping (k -> v) in the forward, there
        is also a mapping (v->k) in the reverse.

        :returns: the rever mapping

        '''
        rev = Isomorphism()
        rev.data = self.backdata
        rev.backdata = self.data
        return rev
