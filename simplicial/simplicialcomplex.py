# Reference implementation for simplicial complexes
#
# Copyright (C) 2017--2022 Simon Dobson
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


class ReferenceRepresentation(Representation):
    '''A reference implementation for simplicial complexes.

    This implementation is a direct in-memory representation of a
    simplicial complex. It is not minimal, in the sense that it holds
    the same information in different forms optimised to different uses.
    See :ref:`reference-implementation` for details.

    :param c: the complex we're representing
    '''

    # ---------- Initialisation and helpers ----------

    def __init__(self):
        super().__init__()

        self._maxOrder: int = -1                                 # order of largest simplex in the complex
        self._simplices: Dict[Any, Tuple[int, int]] = dict()     # dict mapping simplex names to their order and index
        self._indices: List[List[Simplex]] = []                  # array of arrays of simplices in canonical order
        self._boundaries: List[numpy.ndarray] = []               # array of boundary matrices
        self._bases: List[numpy.ndarray] = []                    # array of basis matrices
        self._attributes: Dict[Simplex, Attributes] = dict()     # dict of simplex attributes
        self._sequence: int = 0                                  # sequence number of new simplex names


    # ---------- Core interface ----------

    def newSimplex(self, d: int) -> str:
        """Generate a new unique identifier for a simplex. The default naming
        scheme uses a sequence number and a leading dimension indicator. Users
        can name simplices anything they want to get meaningful names.

        :param d: dimension of the simplex to be identified
        :returns: an identifier not currently used in the complex"""
        i = self._sequence
        while True:
            id = f'{d}d{i}'
            if id not in self._simplices:
                self._sequence = i + 1
                return id
            else:
                i = i + 1

    def addSimplex(self, fs: List[Simplex], id: Simplex, attr: Attributes):
        """Add a simplex to the complex whose faces are the elements
        of fs. This manipulates several internal dat a structures
        including the simplex list, face list, and boundary operator
        matrices.

        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) name for the simplex
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex

        """

        # work out the order of the new simplex
        k = max(len(fs) - 1, 0)
        if k == 0 and len(fs) != 0:
            raise ValueError("0-simplices do not have faces")

        # fill in defaults
        if id is None:
            # no identifier, make one
            id = self.newSimplex(k)
        else:
            # check we've got a new id
            if id in self._simplices:
                raise KeyError(f'Duplicate simplex {id}')
        if attr is None:
            # no attributes, use an empty dict
            attr = dict()

        # make sure all the faces are distinct
        if len(fs) != len(set(fs)):
            # find the duplicate, for reporting -- slow, but we're exiting anyway
            seen = set()
            for f in fs:
                if f in fs:
                    raise KeyError(f'Duplicate face {f}')
                else:
                    seen.add(f)

        # if we're creating a simplex of an order higher than we've seen before,
        # create the necessary structures
        if k > self.maxOrder():
            if k > self._maxOrder + 1:
                # simplex can't have any faces, must be an error
                raise ValueError(f'Can\'t add simplex of order {k}')
            else:
                # add empty structures
                #print "created structures for order {k}".format(k = k)
                self._indices.append([])                                                                  # empty indices
                self._boundaries.append(numpy.zeros([len(self._indices[k - 1]), 0],
                                                    dtype=numpy.int8))    # null boundary operator
                self._bases.append(numpy.zeros([len(self._indices[0]), 0],
                                               dtype=numpy.int8))           # no simplex bases
                self._maxOrder = k
        else:
            # check we don't already have a simplex of this order with
            # the given faces
            if k > 0:
                swf = self._complex.simplexWithFaces(fs)
                if swf is not None:
                    raise KeyError(f'Already have simplex {swf} with faces {fs}')

        # if we have simplices in the order above this one, extend that order's boundary operator
        # for that order
        if self._maxOrder > k:
            # we have a higher order of simplices, add a row of zeros to its boundary operator
            #print("extended structures for order {kp}".format(kp = k + 1))
            self._boundaries[k + 1] = numpy.r_[self._boundaries[k + 1],
                                               numpy.zeros([1, len(self._indices[k + 1])],
                                                           dtype=numpy.int8)]

        # perform the addition
        if k == 0:
            # add the 0-simplex
            self._indices[k].append(id)             # add simplex to canonical ordering
            si = len(self._indices[k]) - 1
            self._simplices[id] = (k, si)           # map simplex to its order and index
            self._attributes[id] = attr             # store the attributes of the new simplex

            # extend all the basis matrices with this new simplex
            if self._maxOrder > 0:
                for i in range(1, self._maxOrder + 1):
                    self._bases[i] = numpy.r_[self._bases[i],
                                              numpy.zeros([1, len(self._indices[i])],
                                                          dtype=numpy.int8)]

            # mark the simplex as its own basis
            if len(self._bases[0]) == 0:
                # first 0-simplex, create the basis matrix
                self._bases[0] = numpy.ones([1, 1])
                #print "after {b}".format(b = self._bases[0])
            else:
                # later 0-simplices, add a row and column for the new 0-simplex
                #print("before {b}".format(b = self._bases[0]))
                self._bases[0] = numpy.c_[self._bases[0],
                                          numpy.zeros([si, 1],
                                                      dtype=numpy.int8)]
                #print("during {b}".format(b = self._bases[0]))
                self._bases[0] = numpy.r_[self._bases[0],
                                          numpy.zeros([1, si + 1],
                                                      dtype=numpy.int8)]
                (self._bases[0])[si, si] = 1
                #print("after {b}".format(b = self._bases[0]))
        else:
            # build the boundary operator for the new higher simplex
            bk = numpy.zeros([len(self._indices[k - 1]), 1],
                             dtype=numpy.int8)
            bs = set()
            for f in fs:
                if f in self._simplices:
                    # check the face is of the correct order
                    (fo, fi) = self._simplices[f]
                    if fo == k - 1:
                        # add the face to the boundary
                        #print("added {id} ({i}) to boundary".format(id = f, i = fi))
                        bk[fi, 0] = 1

                        # add the face's basis to the simplex' basis
                        bs.update(self.basisOf(f))
                    else:
                        raise ValueError(f'Simplex {f} has wrong order ({fo}) to be a face of a simplex of order {k}')
                else:
                    raise KeyError(f'Unknown simplex {f}')
            #print("boundary of {id} is {b}".format(id = id, b = bk))

            # add simplex
            self._indices[k].append(id)                                # add simplex to canonical ordering
            si = len(self._indices[k]) - 1
            self._simplices[id] = (k, si)                              # map simplex to its order and index
            self._boundaries[k] = numpy.c_[self._boundaries[k], bk]    # append boundary operator column
            self._attributes[id] = attr                                # store the attributes of the new simplex
            self._bases[k] = numpy.c_[self._bases[k],
                                      numpy.zeros([len(self._indices[0]), 1],
                                                  dtype=numpy.int8)]
            for b in bs:
                (_, bi) = self._simplices[b]
                (self._bases[k])[bi, si] = 1                           # mark the 0-simplex in the basis
            #print("added {id} with basis {bs}".format(id = id, bs = bs))

        # return the simplex' name
        return id

    def relabelSimplex(self, s: Simplex, q: Simplex):
        '''Relabel a simplex. This changes the canonical mapping of
        simplices to indices as well as the simplex list.

        :param s: the simplex to rename
        :param q: the new name'''

        # check new name is not in use already
        if q in self._simplices:
            raise ValueError(f'Relabeling attempting to re-write {s} to existing simplex {q}')

        # change the entry in the simplex dict
        (k, i) = self._simplices[s]
        self._simplices[q] = (k, i)
        del self._simplices[s]

        # change the entry in the appropriate indices array
        (self._indices[k])[i] = q

        # change the entry in the attributes dict
        self._attributes[q] = self._attributes[s]
        del self._attributes[s]

    def forceDeleteSimplex(self, s: Simplex):
        """Delete a simplex without sanity checks. It delets the simplex,
        its attributes, and its entries in the appropriate boundary matrices.

        :param s: the simplex"""

        # each simplex appears in two boundary matrices (for its
        # own order and the order above, if present); in one
        # basis matrix (for its order); in the indices array for
        # its order; and in the attributes dict

        # find the index and order of the simplex
        (k, i) = self._simplices[s]
        #print(f'delete {s} {i} (order {k})')

        # delete from the basis matrices
        self._bases[k] = numpy.delete(self._bases[k], i, axis=1)
        if k == 0:
            # for 0-simplices, delete rows from all higher orders
            for j in range(self._maxOrder + 1):
                #print(f'delete {s} from order {j}')
                self._bases[j] = numpy.delete(self._bases[j], i, axis=0)

        # delete from boundary matrices
        #print('delete {s} {i} (order {k})'.format(s = s, i = i, k = k))
        if k > 0:
            # delete column from order-k boundary
            #print('delete col {i} from {k}-boundary'.format(i = i, k = k))
            self._boundaries[k] = numpy.delete(self._boundaries[k], i, axis=1)
        if k < self._maxOrder:
            # delete row from order-(k + 1) boundary
            #print('delete row {i} from ({k} + 1)-boundary'.format(i = i, k = k))
            self._boundaries[k + 1] = numpy.delete(self._boundaries[k + 1], i, axis=0)

        # delete from the attributes dict
        del self._attributes[s]

        # delete from the simplices dict
        del self._simplices[s]

        # delete from the indices array
        del (self._indices[k])[i]

        # fix-up the indices of all the other simplices at this order
        ss = self._indices[k]
        for j in range(i, len(ss)):
            self._simplices[ss[j]] = (k, j)

        # if we've emptied the maximum order, reduce it by one
        # and delete the now-empty matrices
        if k == self._maxOrder and len(self._indices[k]) == 0:
            self._maxOrder -= 1
            #print('maxorder reduced to {m}'.format(m = self._maxOrder))
            del self._boundaries[k]
            del self._bases[k]

    def orderOf(self, s: Simplex) -> int:
        """Return the order of a simplex.

        :param s: the simplex
        :returns: the order of the simplex"""
        if s in self._simplices:
            (k, _) = self._simplices[s]
            return k
        else:
            raise KeyError(f'No simplex {s} in complex')

    def indexOf(self, s: Simplex) -> int:
        """Return the inmdex of a simplex.

        :param s: the simplex
        :returns: an index"""
        if s in self._simplices:
            (_, i) = self._simplices[s]
            return i
        else:
            raise KeyError(f'No simplex {s} in complex')

    def basisOf(self, s: Simplex) -> Set[Simplex]:
        """Return the basis of a simplex.

        :param s: the simplex
        :returns: the set of 0-simplices that form the basis of s"""
        (k, si) = self._simplices[s]
        bk = (self._bases[k])[:, si]
        #print("simplex {s} basis column {bk}".format(s = s, bk = bk))
        bs = set()
        for i in range(len(bk)):
            if bk[i] == 1:
                bs.add((self._indices[0])[i])
        #print("basis {bs}".format(bs = bs))
        return bs

    def maxOrder(self) -> int:
        """Return the largest order of simplices in the complex.

        :returns: the largest order that contains at least one simplex, or -1"""
        return self._maxOrder

    def simplices(self, reverse: bool) -> List[Simplex]:
        """Return all the simplices in the complex, in order: the
        low orders first (unless reverse is True), and in canonical
        order within each order.

        :param reverse: (optional) reverse the sort order if True
        :returns: a list of simplices"""
        return [face_val for face in self._indices[::(-1) ** reverse] for face_val in face]

    def simplicesOfOrder(self, k: int) -> List[Simplex]:
        """Return all the simplices of the given order.
        The simplices are returned in "canonical" order, meaning the order
        they appear in the boiundary operator matrices.

        :param k: the desired order
        :returns: a set of simplices, which may be empty"""
        if k <= self.maxOrder():
            return list(self._indices[k])
        else:
            return list()

    def containsSimplex(self, s: Simplex) -> bool:
        """Test whether the complex contains the given simplex.

        :param s: the simplex
        :returns: True if the simplex is in the complex"""
        return (s in self._simplices.keys())

    def getAttributes(self, s: Simplex) -> Attributes:
        """Return the attributes associated with the given simplex.

        :param s: the simplex
        :returns: a dict of attributes"""
        return self._attributes[s]

    def setAttributes(self, s: Simplex, attr: Attributes):
        """Set the attributes associated with a simplex.

        :param s: the simplex
        :param attr: a dict of attributes"""
        self._attributes[s] = attr

    def faces(self, s: Simplex) -> Set[Simplex]:
        """Return the faces of a simplex.

        :param s: the simplex
        :returns: a set of faces"""
        (k, i) = self._simplices[s]
        if k == 0:
            # 0-simplices do not have faces
            return set()

        # extract the column of the boundary matrix
        #print("boundary for {s} order {k} {b}".format(k = k, s = s, b = self._boundaries[k]))
        b = (self._boundaries[k])[:, i]
        #print("boundary of {s} is {b}".format(s = s, b = b))

        # extract the simplex names from this column
        fs = set()
        for i in range(len(b)):
            if b[i] == 1:
                #print("add index {i} = {id}".format(i = i, id = (self._indices[k - 1])[i]))
                fs.add((self._indices[k - 1])[i])
        return fs

    def cofaces(self, s: Simplex) -> Set[Simplex]:
        '''Return the simplices the given simnplex is a face of.

        :param s: the simplex
        :returns: a list of simplices'''
        (k, i) = self._simplices[s]
        if k == self.maxOrder():
            # simplex is of maximal order, so isn't a face or a larger simplex
            return set()
        else:
            # convert the 1s into simplex names of the faces
            ss = self._indices[k + 1]
            fs = numpy.compress((self._boundaries[k + 1])[i], ss)
            return list(fs)

    def boundaryOperator(self, k: int) -> numpy.ndarray:
        """Return the boundary operator of the k-simplices.

        :param k: the order of simplices
        :returns: the boundary matrix

        """
        if k == 0:
            # return a row of zeros
            return numpy.zeros([1, len(self._indices[0])])
        else:
            if k > self.maxOrder():
                # return a null boundary operator
                return numpy.zeros([0, 0])
            else:
                return self._boundaries[k]


    # ---------- Optimised versions of methods ----------

    def simplexWithBasis(self, bs: List[Simplex], fatal: bool = False) -> Simplex:
        """Return the simplex with the given basis, if it exists
        in the complex. If no such simplex exists, or if the given
        set is not a basis, then None is returned; if fatal is True, then
        an exception is raised instead.

        :param bs: the basis
        :param fatal: (optional) make failure raise an exception (defaults to False)
        :returns: the simplex or None"""
        k = len(bs) - 1

        # check we have a basis
        if not self.isBasis(bs, fatal=fatal):
            return None

        # if the order is greater than the maximum, we can't have such a simplex
        if k > self.maxOrder():
            if fatal:
                raise KeyError(f'Complex does not have any simplices of order {k}')
            else:
                return None

        # an 0-simplex just has to be there (since we know we have a valid basis)
        if k == 0:
            return (list(bs))[0]

        # form the basis column for this basis
        bc = numpy.zeros([len(self._indices[0])])
        for b in bs:
            (_, bi) = self._simplices[b]
            bc[bi] = 1

        # check for a simplex with the given basis
        for i in range(len(self._indices[k])):
            #print("check {bs} against {s}".format(bs = bc, s = (self._bases[k])[:, i]))
            if ((self._bases[k])[:, i] == bc).all():
                return (self._indices[k])[i]

        # if we get here, there was no such simplex
        if fatal:
            raise KeyError(f'Complex does not have a simplex with basis {bs}')
        else:
            return None
