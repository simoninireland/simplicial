# Triangular lattices, the basic coverings of a space
#
# Copyright (C) 2017--2019 Simon Dobson
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

from typing import List
from simplicial import SimplicialComplex, Simplex, Embedding


class TriangularLattice(SimplicialComplex):
    """A triangular simplicial tiling of a plane. Triangular lattices have simplices
    of order 0, 1, and 2, connecting the 0-simplices very regularly.

    :param r: the number of rows
    :param c: the number of columns

    """

    def __init__(self, r: int, c: int):
        super(TriangularLattice, self).__init__()
        self._rows = r
        self._columns = c

        # add the basis for the lattice
        for i in range(r):
            for j in range(c):
                #print(self._indexOfVertex(i, j))
                self.addSimplex(id=self._indexOfVertex(i, j))

        # add NS edges, jumping adjacent rows
        for i in range(0, r - 2):
            for j in range(c):
                #print('2NS', self._indexOfVertex(i, j), self._indexOfVertex(i + 2, j))
                self.addSimplexWithBasis([self._indexOfVertex(i, j),
                                          self._indexOfVertex(i + 2, j)])

        # add SW and SE edges
        for i in range(0, r - 1):
            for j in range(c):
                # add SW edge except for column 0 of even-numbered rows
                if not (j == 0 and (i % 2) == 0):
                    if i % 2 == 0:
                        swj = j - 1
                    else:
                        swj = j
                    #print('2SW', self._indexOfVertex(i, j), self._indexOfVertex(i + 1, swj))
                    self.addSimplexWithBasis([self._indexOfVertex(i, j),
                                              self._indexOfVertex(i + 1, swj)])

                # add SE edge except for column (c - 1) of odd-numbered rows
                if not (j == c - 1 and (i % 2) == 1):
                    if i % 2 == 0:
                        sej = j
                    else:
                        sej = j + 1
                    #print('2SE', self._indexOfVertex(i, j), self._indexOfVertex(i + 1, sej))
                    self.addSimplexWithBasis([self._indexOfVertex(i, j),
                                              self._indexOfVertex(i + 1, sej)])

        # fill in the triangles
        for i in range(0, r - 2):
            for j in range(c):
                # add SW triangle for all except column 0 of even-numbered rows
                if not (j == 0 and (i % 2) == 0):
                    if i % 2 == 0:
                        swj = j - 1
                    else:
                        swj = j
                    #print('3SW', self._indexOfVertex(i, j), self._indexOfVertex(i + 1, swj),  self._indexOfVertex(i + 2, j))
                    self.addSimplexWithBasis([self._indexOfVertex(i, j),
                                              self._indexOfVertex(i + 1, swj),
                                              self._indexOfVertex(i + 2, j)])

                # add SE triangle for all except column (c - 1) of odd-numbered rows
                if not (j == c - 1 and (i % 2) == 1):
                    if i % 2 == 0:
                        sej = j
                    else:
                        sej = j + 1
                    #print('3SE', self._indexOfVertex(i, j), self._indexOfVertex(i + 2, j),  self._indexOfVertex(i + 1, sej))
                    self.addSimplexWithBasis([self._indexOfVertex(i, j),
                                              self._indexOfVertex(i + 2, j),
                                              self._indexOfVertex(i + 1, sej)])

    def _indexOfVertex(self, i: int, j: int) -> int:
        """Return the identifier of the given (row, column) vertex (0-simplex).
        Row and column indexing start from zero.

        :param i: the row
        :param j: the column
        :returns: the identifier of the point"""
        return i * self.columns() + j

    def rows(self) -> int:
        """Return the number of rows in the lattice.

        :returns: the number of rows"""''
        return self._rows

    def columns(self) -> int:
        """Return the number of columns in the lattice.

        :returns: the number of columns"""''
        return self._columns


class TriangularLatticeEmbedding(Embedding):
    """A regular embedding of a triangular lattice into a plane. The default is
    to embed into a unit plane, but this can be scaled as required. The lattice
    can be distorted by providing explicit positions for 0-simplices as required.

    :param c: the complex
    :param h: height of the plane (defaults to 1.0)
    :param w: width of the plane (defaults to 1.0)

    """

    def __init__(self, c: SimplicialComplex, h: float = 1.0, w: float = 1.0):
        super(TriangularLatticeEmbedding, self).__init__(c, 2)
        self._height = h
        self._width = w

    def height(self) -> float:
        """Return the height of the lattice.

        :returns: the height of the lattice"""
        return self._height

    def width(self) -> float:
        """Return the width of the lattice.

        :returns: the width of the lattice"""
        return self._width

    def computePositionOf(self, s: Simplex) -> List[float]:
        """Compute the position of the given simplex.

        :param s: the simplex
        :returns: the position of the simplex"""

        # extract simplex index
        c = self.complex()
        n = c.indexOf(s)

        # convert index to (row, column) co-ordinates
        nr = c.rows()
        nc = c.columns()
        i = int(n / c.columns())
        j = n % c.columns()

        # compute position and return it
        rh = (self.height() + 0.0) / nr           # row height
        cw = (self.width() + 0.0) / (2 * nc)      # column width
        y = self.height() - rh * i
        if i % 2 == 0:
            x = cw * (j * 2)
        else:
            # shift along for odd-numbered rows
            x = cw * ((j * 2) + 1)
        return [x, y]
