# A filtration of simplicial complexes
#
# Copyright (C) 2017--2020 Simon Dobson
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
import copy
import itertools

from simplicial import *

class Filtration(SimplicialComplex):
    '''A filtration of simplicial complexes.
    
    A filtration is a sequence of simplicial complexes parameterised by a single
    number and ordered by inclusion. For two values of the parameter :math:`p_1`
    and :math:`p_2` with corresponding complexes :math:`C_1` and :math:`C_2`,
    :math:`p_1 < p_2 \implies C_1 < C_2`: all the simplices in :math:`C_1` are
    contained in :math:`C_2`, with both being legal simplicial complexes.

    This class allows different simplices to be assigned to different parameter
    values while maintaining the integrity of the complex. It provides a method
    for copying just the complex at a given level if required.

    Filtrations are the basis for persistent homology, and this class also provides
    operations for efficiently computing the homology groups of the sequence of
    complexes.   

    :param p: the initial parameter (defaults to 0)
    '''

    # ---------- Initialisation and helpers ----------
    
    def __init__( self,  p = 0 ):
        super(Filtration, self).__init__()
        self._parameter = p         # ordering parameter
        self._appears = dict()      # mapping from simplex to the parameter value it appears at
        self._includes = dict()     # the reverse mapping, from parameter to simplices

    
    # ---------- Parameter setting ----------

    def set(self, p):
        '''Set the parameter.

        :param p: the new parameter value'''
        self._parameter = p

    
    # ---------- Adding simplices ----------

    def addSimplex( self, fs = [], id = None, attr = None ):
        """Add a simplex to the complex currently parameterised within
        the filtration.

        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) name for the simplex 
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex"""
        nid = super(Filtration, self).addSimplex(fs, id, attr)
        self._appears[nid] = self._parameter
        self._includes[self._parameter] = nid

    # All other simplex addition methods use this one as their base


    # ---------- Relabelling ----------

    # TBD


    # ---------- Deleting simplices ----------

    # TBD


    # ---------- Accessing simplices ----------

    def maxOrder(self):
        '''Return the largest order of simplices in the complex
        at the current parameter value.

        :returns: the largest order'''
        # TBD
        pass

