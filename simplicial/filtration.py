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
    index (typically a number) and ordered by inclusion. For two values of the index :math:`p_1`
    and :math:`p_2` with corresponding complexes :math:`C_1` and :math:`C_2`,
    :math:`p_1 < p_2 \implies C_1 < C_2`: all the simplices in :math:`C_1` are
    contained in :math:`C_2`, with both being legal simplicial complexes.

    This class allows different simplices to be assigned to different indices
    while maintaining the integrity of the complex. It provides a method
    for copying just the complex at a given level if required.

    Filtrations are the basis for persistent homology, and this class also provides
    operations for efficiently computing the homology groups of the sequence of
    complexes.   

    :param ind: the initial index (defaults to 0)
    '''

    # ---------- Initialisation and helpers ----------
    
    def __init__( self,  ind = 0 ):
        super(Filtration, self).__init__()
        self._index = ind           # index
        self._appears = dict()      # mapping from simplex to the index value it appears at
        self._includes = dict()     # the reverse mapping, from index to a set of simplices
        self._includes[ind] = set()
        self._maxOrders = dict()    # maximum orders at each index
        self._maxOrders[ind] = self.maxOrder()

    
    # ---------- Indexing ----------

    def getIndex(self):
        '''Get the current index.

        :returns: the index'''
        return self._index

    def indices(self, reverse = False):
        '''Return an enumeration of the indices of the filtration,
        in ascending order by default.

        :param reverse: (optional) reverse the order of the indices (defaults to ascending)
        :returns: the indices'''
        return sorted(self._includes.keys(), reverse = reverse)
        
    def setIndex(self, ind):
        '''Set the index.

        :param ind: the new index value'''
        self._index = ind

        # create the necessary data structures
        if ind not in self._includes.keys():
            self._includes[ind] = set()
            ind = self.getIndex()
            inds = self.indices()
            i = inds.index(ind)
            if i > 0:
                self._maxOrders[ind] = self._maxOrders[inds[i - 1]]
            else:
                self._maxOrders[ind] = -1

        self._maxOrder = self._maxOrders[ind]

    def setPreviousIndex(self):
        '''Set the index to the previous value. If we're at the smallest index,
        nothing happens.

        :returns: the new index'''
        ind = self.getIndex()
        inds = self.indices()
        i = inds.index(ind)
        if i == 0:
            # currently at the lowest index, do nothing
            return ind
        else:
            # move to the earlier index
            self._index = inds[ind - 1]
            return self._index

    def setMinimumIndex(self):
        '''Set the index of the filtration to its minumum value, selecting
        the smallest complex.'''
        self.setIndex(self.indices()[0])
 
    def setNextIndex(self):
        '''Set the index to the next value. If we're at the largest index,
        nothing happens.

        :returns: the new index'''
        ind = self.getIndex()
        inds = self.indices()
        i = inds.index(ind)
        if i == len(inds) - 1:
            # currently at the highest index, do nothing
            return ind
        else:
            # move to the next index
            self._index = inds[ind + 1]
            return self._index

    def setMaximumIndex(self):
        '''Set the index of the filtration to its maximum value, selecting
        the largest complex.'''
        self.setIndex(self.indices()[-1])
        
    
    # ---------- Adding simplices ----------

    def addSimplex( self, fs = [], id = None, attr = None ):
        '''Add a simplex to the filtration at the current index.

        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) name for the simplex 
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex'''
        nid = super(Filtration, self).addSimplex(fs, id, attr)
        ind = self.getIndex()
        self._appears[nid] = ind
        self._includes[ind].add(nid)
        if self.maxOrder() > self._maxOrders[ind]:
            self._maxOrders[ind] = self.maxOrder()

    # All other simplex addition methods use this one as their base


    # ---------- Relabelling ----------

    # TBD


    # ---------- Deleting simplices ----------

    def _deleteSimplex(self, s):
        '''Delete a simplex.

        :param s: the simplex'''
        super(Filtration, self)._deleteSimplex(s)
        i = self._appears[s]
        del self._appears[s]
        self._includes[i].remove(s)
        if len(self._includes[i]) == 0:
            # last simplex at this index. delete the index as well
            del self._includes[i]


    # ---------- Accessing simplices ----------

    def orderOf(self, s):
        '''Return the order of the simplex in the filtration. This will raise
        an exception if the simplex isn't defined at the current index.

        :param s: the simplex
        :reeturns: the order of the simplex'''
        try:
            return super(Filtration, self).orderOf(s)
        except(Exception):
            # change to a slightly more informative error message
            raise Exception('No simplex {s} in filtration at index {ind}'.format(s = s, ind = self.getIndex()))

    def indexOf(self, s):
        '''Return the index of the simplex in the filtration. This will raise
        an exception if the simplex isn't defined at the current index.

        :param s: the simplex
        :reeturns: the index of the simplex within its order'''
        try:
            return super(Filtration, self).indexOf(s)
        except(Exception):
            # change to a slightly more informative error message
            raise Exception('No simplex {s} in filtration at index {ind}'.format(s = s, ind = self.getIndex()))

    def simplices(self, reverse = False):
        '''Return all the simplices in the filtration at the current index.
        The simplices are returned in order of their orders, 0-simplices first unless the
        reverse paarneter is True, in which case 0-simplices will be last.

        :param reverse: (optional) reverse sort order (defaults to False)
        :returns: a list of simplices'''
        return [ s for s in super(Filtration, self).simplices(reverse) if s in self ]
    
    def numberOfSimplices(self):
        '''Return the number of simplices in the filtration up to and including
        the current index.

        :returns: the number of simplices'''
        n = 0
        ind = self.getIndex()
        for i in self.indices():
            if i <= ind:
                n += len(self._includes[i])
            else:
                break  
        return n

    def numberOfSimplicesOfOrder(self):
        '''Return a dict mapping an order to the number of simplices
        of that order in the filtratrion up to and including the current index. 
        
        :returns: a list of number of simplices at each order'''
        nsos = super(Filtration, self).numberOfSimplicesOfOrder()
 
        # filter out any simplices not defined at the current index
        empty = set()
        for k in nsos.keys():
            nsos[k] = len([ s for s in nsos[k] if k in self ])
            if nsos[k] == 0:
                empty.add(k)

        # delete any orders emptied by this process
        for k in empty:
            del nsos[k]

        return nsos
        

    # ---------- Testing for simplices ----------

    def containsSimplex(self, s):
        '''Test whether the filtration contains the given simplex at the current index.
        This implies that the simplex was added to the filtration at an index that
        is the same or lessa than the current index.

        :returns: True if the simplex is in the filtration'''
        return super(Filtration, self).containsSimplex(s) and self._appears[s] <= self.getIndex()

    # ---------- Inclusion of complexes ----------
