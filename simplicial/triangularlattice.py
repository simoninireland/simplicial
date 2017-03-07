# Triangular lattices, the basic coverings of a place
#
# Copyright (C) 2017 Simon Dobson
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

from simplicial import *

class TriangularLattice(SimplicialComplex):
    
    def __init__( self, r, c ):
        '''Create a triangulated lattice with the given number of rows and columns.
        
        :param r: the number of rows
        :param c: the number of columns'''
        super(TriangularLattice, self).__init__()
        self._rows = r
        self._columns = c
        
        # add the basis for the lattice
        for i in xrange(r):
            for j in xrange(c):
                self.addSimplex(id = self._indexOfVertex(i, j))
                
        # add NS edges, jumping adjacent rows
        for i in xrange(0, r - 2):
            for j in xrange(c):
                #print self._indexOfEdge(i, j, i + 2, j)
                self.addSimplex(id = self._indexOfEdge(i, j, i + 2, j),
                                fs = [ self._indexOfVertex(i, j),
                                       self._indexOfVertex(i + 2, j) ])
        
        # add SW and SE edges
        for i in xrange(0, r - 1):
            for j in xrange(c):
                # add SW edge except for column 0 of even-numbered rows
                if not(j == 0 and (i % 2) == 0):
                    if i % 2 == 0:
                        swj = j - 1
                    else:
                        swj = j
                    #print 'SW', self._indexOfEdge(i, j, i + 1, swj)
                    self.addSimplex(id = self._indexOfEdge(i, j, i + 1, swj),
                                    fs = [ self._indexOfVertex(i, j),
                                           self._indexOfVertex(i + 1, swj) ])

                # add SE edge except for column (c -1) of odd-numbered rows
                if not(j == c - 1 and (i % 2) == 1):
                    if i % 2 == 0:
                        sej = j
                    else:
                        sej = j + 1
                    #print 'SE', self._indexOfEdge(i, j, i + 1, sej)
                    self.addSimplex(id = self._indexOfEdge(i, j, i + 1, sej),
                                    fs = [ self._indexOfVertex(i, j),
                                           self._indexOfVertex(i + 1, sej) ])
                    
        # fill in the triangles
        for i in xrange(0, r - 2):
            for j in xrange(c):
                # add SW triangle for all except column 0 of even-numbered rows
                if not(j == 0 and (i % 2) == 0):
                    if i % 2 == 0:
                        swj = j - 1
                    else:
                        swj = j
                    #print 'SW tri', self._indexOfTriangle(i, j, i + 1, swj, i + 2, j)
                    self.addSimplex(id = self._indexOfTriangle(i, j, i + 1, swj, i + 2, j),
                                    fs = [ self._indexOfEdge(i, j, i + 1, swj),
                                           self._indexOfEdge(i + 1, swj, i + 2, j),
                                           self._indexOfEdge(i, j, i + 2, j) ])
                
                # add SE triangle for all except column (c - 1) of odd-numbered rows
                if not(j == c - 1 and (i % 2) == 1):
                    if i % 2 == 0:
                        sej = j
                    else:
                        sej = j + 1
                    #print 'SE tri', self._indexOfTriangle(i, j, i + 2, j, i + 1, sej)
                    self.addSimplex(id = self._indexOfTriangle(i, j, i + 2, j, i + 1, sej),
                                    fs = [ self._indexOfEdge(i, j, i + 2, j),
                                           self._indexOfEdge(i, j, i + 1, sej),
                                           self._indexOfEdge(i + 2, j, i + 1, sej) ])
        
                
    def rows( self ):
        '''Return the number of rows in the lattice.
        
        :returns: the number of rows'''''
        return self._rows
    
    def columns( self ):
        '''Return the number of columns in the lattice.
        
        :returns: the number of columns'''''
        return self._columns

    def _indexOfVertex( self, i, j ):
        '''Return the identifier of the given (row, column ) vertex (0-simplex).
        Row and column indexing start from zero.
        
        :param i: the row
        :param j: the column
        :returns: the identifier of the point'''
        return i * self.columns() + j
    
    def _indexOfEdge( self, i, j, ip, jp ):
        '''Return the identifier of the edge connecting the vertices at
        the given row and column positions.
        
        :param i: the row of the first vertex
        :param j: the column of the first vertex
        :param ip: the row of the second vertex
        :param jp: the column of the second vertex
        :returns: the identifier of the edge'''
        vs = self._orderIndices([ self._indexOfVertex(i, j),
                                  self._indexOfVertex(ip, jp) ])
        return '{s}-{e}'.format(s = vs[0],
                                e = vs[1])
    
    def _indexOfTriangle(self, i, j, ip, jp, iq, jq ):
        '''Return the identifier of the triangle filling in the
        ]vertices at the given positions.
        
        :param i: the row of the first vertex
        :param j: the column of the first vertex
        :param ip: the row of the second vertex
        :param jp: the column of the second vertex
        :param iq: the row of the third vertex
        :param jq: the column of the third vertex
        :returns: the identifier of the triangle'''
        vs = self._orderIndices([ self._indexOfVertex(i, j),
                                  self._indexOfVertex(ip, jp),
                                  self._indexOfVertex(iq, jq) ])
        return '{a}-{b}-{c}'.format(a = vs[0],
                                    b = vs[1],
                                    c = vs[2])
    
