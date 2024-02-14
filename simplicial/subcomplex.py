# Simplicial complex live views
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

import numpy
from typing import Dict, Any, List, Set, Tuple
from simplicial import Simplex, Attributes, Representation


class SubcomplexRepresentation(Representation):
    '''A representation offering a view onto another.



    :param rep: the underlying representation
    :param bs: the basis for the sub-complex
    '''


    def __init__(self, rep: Representation, bs: List[Simplex]):
        super().__init__()
        self._rep = rep
        self._basis = bs


    # ---------- Core interface ----------

    def newSimplex(self, fs: List[Simplex]) -> str:
        '''Add the new simplex to the underlying representation.

        :param fs: the faces
        :returns: the simplex name'''
        return self._rep.newSimplex(fs)


    def addSimplex(self, fs: List[Simplex] = None, id: Simplex = None, attr: Attributes = None) -> Simplex:
        """Add a simplex to the underlying representation.

        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) name for the simplex
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex

        """
        return self._rep.addSimplex(fs, id, attr)

    def relabelSimplex(self, s: Simplex, q: Simplex):
        '''Relabel a simplex in the underlying representation.

        :param s: the simplex to rename
        :param q: the new name'''
        return self._rep.relabelSimplex(s, q)

    def forceDeleteSimplex(self, s: Simplex):
        """Delete a simplex in the underlying representation without sanity checks.

        :param s: the simplex"""
        return self._rep.forceDeleteSimplex(s)
