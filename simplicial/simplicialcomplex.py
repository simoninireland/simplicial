# Base class for simplicial complexes
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

import numpy
import copy
import itertools


class SimplicialComplex(object):
    """A finite abstract simplicial complex.
    
    A simplicial :term:`complex` is a generalisation of a network in which
    vertices (0-simplices) and edges (1-simplices) can be composed
    into triangles (2-simplices), tetrahedrons (3-simplices) and so
    forth. This class actually implements closed simplicial complexes
    that contain every simplex, every :term:`face` of that simplex, every face
    of those simplices, and so forth. Operations to add and remove
    simplices cascade to keep the complex closed: if a simplex is an
    element of a complex, then all its faces are also elements, and so
    on recursively.

    The class also includes some more advanced topological operations, notably for
    computing the :term:`Euler characteristic` of a complex and
    performing Euler integration, and for computational :term:`homology`.

    """

    # ---------- Initialisation and helpers ----------
    
    def __init__( self ):
        self._sequence = 1                  # sequence number for generating simplex names
        self._maxOrder = -1                 # order of largest simplex in the complex
        self._simplices = dict()            # dict mapping simplex names to their order and index
        self._indices = []                  # array of arrays of simplices in canonical order
        self._boundaries = []               # array of boundary matrices
        self._bases = []                    # array of basis matrices            
        self._attributes = dict()           # dict of simplex attributes

    def _newUniqueIndex( self, d ):
        """Generate a new unique identifier for a simplex. The default naming
        scheme uses a sequence number and a leading dimension indicator. Users
        can name simplices anything they want to get meaningful names. 
        
        :param d: dimension of the simplex to be identified
        :returns: an identifier not currently used in the complex"""
        i = self._sequence
        while True:
            id = '{dim}d{id}'.format(dim = d, id = i)
            if id not in self:
                self._sequence = i + 1
                return id
            else:
                i = i + 1
    

    # ---------- Adding simplices ----------

    def addSimplex( self, fs = [], id = None, attr = None ):
        """Add a simplex to the complex whose faces are the elements of fs.
        If no faces are given then the simplex is a 0-simplex (point).
        If no id is provided one is created. If present, attr should be a
        dict of attributes for the simplex.

        To add a simplex from its basis (rather than its faces) use
        :meth:`addSimplexByBasis`.
        
        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) name for the simplex 
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex"""

        # work out the order of the new simplex
        k = max(len(fs) - 1, 0)
        if k == 0 and len(fs) != 0:
            raise Exception("0-simplices do not have faces")
                                
        # fill in defaults
        if id is None:
            # no identifier, make one
            id = self._newUniqueIndex(k)
        else:
            # check we've got a new id
            if id in self:
                raise Exception('Duplicate simplex {id}'.format(id = id))
        if attr is None:
            # no attributes
            attr = dict()

        # if we're creating a simplex of an order higher than we've seen before,
        # create the necessary structures
        if k > self.maxOrder():
            if k > self._maxOrder + 1:
                # simplex can't have any faces, must be an error
                raise Exception("Can't add simplex of order {k}".format(k = k))
            else:
                # add empty structures
                #print "created structures for order {k}".format(k = k)
                self._indices.append([])                                                  # empty indices
                self._boundaries.append(numpy.zeros([ len(self._indices[k - 1]), 0 ]))    # null boundary operator
                self._bases.append(numpy.zeros([ len(self._indices[0]), 0 ]))             # no simplex bases
                self._maxOrder = k
        else:
            # check we don't already have a simplex of this order with
            # the given faces
            if k > 0:
                swf = self.simplexWithFaces(fs)
                if swf is not None:
                    raise Exception("Already have simplex {s} with faces {fs}".format(s = swf,
                                                                                      fs = fs))
            
        # if we have simplices in the order above this one, extend that order's boundary operator
        # for that order
        if self.maxOrder() > k:
            # we have a higher order of simplices, add a row of zeros to its boundary operator
            #print "extended structures for order {kp}".format(kp = k + 1)
            self._boundaries[k + 1] = numpy.r_[self._boundaries[k + 1], numpy.zeros([ 1, len(self._indices[k + 1]) ])]

        # perform the addition
        if k == 0:
            # add the 0-simplex
            self._indices[k].append(id)             # add simplex to canonical ordering
            si = len(self._indices[k]) - 1
            self._simplices[id] = (k, si)           # map simplex to its order and index
            self._attributes[id] = attr             # store the attributes of the new simplex
            
            # extend all the basis matrices with this new simplex
            if self.maxOrder() > 0:
                for i in range(1, self.maxOrder() + 1):
                    self._bases[i] = numpy.r_[self._bases[i], numpy.zeros([ 1, len(self._indices[i]) ])]

            # mark the simplex as its own basis
            if len(self._bases[0]) == 0:
                # first 0-simplex, create the basis matrix
                self._bases[0] = numpy.ones([ 1, 1 ])
                #print "after {b}".format(b = self._bases[0])
            else:
                # later 0-simplices, add a row and column for the new 0-simplex
                #print "before {b}".format(b = self._bases[0])
                self._bases[0] = numpy.c_[self._bases[0], numpy.zeros([ si, 1 ])]
                #print "during {b}".format(b = self._bases[0])
                self._bases[0] = numpy.r_[self._bases[0], numpy.zeros([ 1, si + 1 ])]
                (self._bases[0])[si, si] = 1
                #print "after {b}".format(b = self._bases[0])
        else:
            # build the boundary operator for the new higher simplex
            bk = numpy.zeros([ len(self._indices[k - 1]), 1 ])
            bs = set()
            for f in fs:
                if f in self:
                    # check the face is of the correct order
                    (fo, fi) = self._simplices[f] 
                    if fo == k - 1:
                        # add the face to the boundary
                        #print "added {id} ({i}) to boundary".format(id = f, i = fi)
                        bk[fi, 0] = 1

                        # add the face's basis to the simplex' basis
                        bs.update(self.basisOf(f))
                    else:
                        raise Exception("Simplex {f} has wrong order ({fo}) to be a face of a simplex of order {k}".format(f = f,
                                                                                                                           fo = fo,
                                                                                                                           k = k))
                else:
                    raise Exception("Unknown simplex {f}".format(f = f))
            #print "boundary of {id} is {b}".format(id = id, b = bk)

            # add simplex
            self._indices[k].append(id)                                # add simplex to canonical ordering
            si = len(self._indices[k]) - 1
            self._simplices[id] = (k, si)                              # map simplex to its order and index
            self._boundaries[k] = numpy.c_[self._boundaries[k], bk]    # append boundary operator column
            self._attributes[id] = attr                                # store the attributes of the new simplex
            self._bases[k] = numpy.c_[self._bases[k], numpy.zeros([len(self._indices[0]), 1 ])]
            for b in bs:
                (_, bi) = self._simplices[b]
                (self._bases[k])[bi, si] = 1                           # mark the 0-simplex in the basis
            #print "added {id} with basis {bs}".format(id = id, bs = bs)
            
        # return the simplex' name
        return id

    def isBasis( self, bs, fatal = False ):
        """Return True if the given set of simplices is a basis, that is,
        a set of 0-simplices. The simplices must already exist in the complex.
        The operation returns a boolean unless fatal is True, in which
        case a missing or non-basis element will raise an exception.

        :param bs: the simplices
        :param fatal: (optional) make missing or higher-order simplices fatal (defaults to False)
        :returns: True if the given simplices form a basis"""
        for b in bs:
            if b in self:
                if self.orderOf(b) != 0:
                    # simplex isn't an 0-simplex, so not a basis
                    if fatal:
                        # we treat this as a fatal event
                        raise Exception("Higher-order simplex {s} in basis set".format(s = b))
                    else:
                        # non-fatal
                        return False
            else:
                # simplex not present in complex
                if fatal:
                    # we treat this as a fatal event
                    raise Exception("Simplex {s} not found".format(s = b))
                else:
                    # non-fatal
                    return False
        return True
    
    def ensureBasis( self, bs, attr = None ):
        """For a given set of simplices, ensure they constitute a basis. This means
        that any simplices already present must be 0-simplices, and any missing
        ones will be created.

        :param bs: the simplices
        :param attr: (optional) attributes for any simplices added"""
        for b in bs:
            if b in self:
                if self.orderOf(b) != 0:
                    # simplex isn't an 0-simplex, so not a basis
                    raise Exception("Higher-order simplex {s} in basis set".format(s = b))
            else:
                # simplex not present in complex
                self.addSimplex(id = b, attr = attr)

    def _addSimplexWithBasis( self, id, attr, k, bs ):
        """Private method to add a simplex from its basis. If a simplex
        with this basis already exists, it is returned.
        
        :param id: the name of the top-most simplex
        :param attr: the attributes of the top-most simplex
        :param k: the order of the new top-most simplex
        :param bs: the basis
        :returns: the simplex"""
        s = self.simplexWithBasis(bs)
        if s is None:
            # no simplex, recursively create all its faces
            fs = set()
            for pfs in itertools.combinations(bs, len(bs) - 1):
                fs.add(self._addSimplexWithBasis(id, attr, k, pfs))
                
            # create the simplex from its faces
            if k == len(bs) - 1:
                # we're creating the top-most simplex, so use its name and attributes
                s = self.addSimplex(id = id, fs = fs, attr = attr)
            else:
                # we're adding a face, synthesise the name
                s = self.addSimplex(fs = fs)
                
        # return the simplex
        return s
        
    def addSimplexWithBasis( self, bs, id = None, attr = None ):
        """Add a simplex by providing its basis, which uniquely defines it.
        This method adds all the simplices necessary to define the new
        simplex, using :meth:`simplexByBasis` to find and re-use any that are
        already in the complex. All simplices created (including the top-most one)
        are given the attributes provided.

        To add a simplex defined by its faces, use :meth:`addSimplex`.

        Defining a k-simplex requires a basis of (k + 1) 0-simplices.

        :param bs: the basis
        :param id: (optional) the name of the new simplex (synthesised if omitted)
        :param attr: (optional) dict of attributes (defaults to none)
        :returns: the name of the new simplex (which will be id if provided)"""
        k = len(bs) - 1    # order of the final simplex

        # fill in defaults
        if id is None:
            id = self._newUniqueIndex(k)
        if attr is None:
            attr = dict()

        # check we don't already have a simplex with this basis
        eid = self.simplexWithBasis(bs)
        if eid is not None:
            raise Exception("Simplex {id} already exists with basis {bs}".format(id = eid,
                                                                                 bs = bs))
        
        # if we're creating an 0-simplex, we're equivalent to addSimplex
        if k == 0:
            return self.addSimplex(id = id, attr = attr)

        # make sure the list is a basis, creating any missing 0-simplices
        self.ensureBasis(bs, attr)

        # recursively add the simplex and any of its missing faces
        s = self._addSimplexWithBasis(id, attr, k, bs)

        return s

    def addSimplexOfOrder( self, k, id = None, attr = None ):
        """Add a new simplex, disjoint from all others, with the given order.
        This will create all the necessary faces and so on down to a new
        basis.

        :param k: the order of the new simplex
        :param id: (optional) name of the new simplex
        :param attr: (optional) dict of attributes added to the new simplex
        :returns: the name of the new simplex"""
        if k == 0:
            # it's an 0-simplex, just try to create a new one
            return self.addSimplex(id = id, attr = attr)
        else:
            # create a basis of new names
            bs = []
            for i in range(k + 1):
                bs.append(self.addSimplex())

            # create the new simplex and return it
            return self.addSimplexWithBasis(bs, id, attr)
    
    def addSimplicesFrom( self, c, rename = None ):
        """Add simplices from the given complex. The rename parameter
        is an optional mapping of the names in c that can be provided
        as a dict of old names to new names or a function from names
        to names.

        If the relabeling is a dict it may be incomplete, in which
        case simplices retain their names.  (If the relabeling is a
        function, it has to handle all names.)

        This operation is equivalent to copying the other complex,
        re-labeling it using :meth:`relabel` and then copying it
        into this complex directly. The caveats on attributes
        containing simplex names mentioned in respect to :meth:`relabel`
        apply to :meth:`addSimplicesFrom` too.
        
        :param c: the other complex
        :param rename: (optional) renaming dict or function
        :returns: a list of simplex names"""

        # fill-out the defaults
        if rename is None:
            f = lambda s: s
        else:
            if isinstance(rename, dict):
                f = lambda s: rename[s] if s in rename.keys() else s
            else:
                f = rename

        # perform the copy, renaming the nodes as they come in
        ns = []
        for s in c.simplices():
            t = f(s)
            if s != t and t in self._simplices.keys():
                raise Exception('Copying attempting to re-write {s} to the name of an existing simplex {t}'.format(s = s, t = t))
            id = self.addSimplex(id = t,
                                 fs = list(map(f, c.faces(s))),
                                 attr = c[s])
            ns.append(id)
        return ns


    # ---------- Relabelling ----------
    
    def relabel( self, rename ):
        """Re-label simplices using the given relabeling, which may be a
        dict from old names to new names or a function taking a name
        and returning a new name.

        If the relabeling is a dict it may be incomplete, in which
        case unmentioned simplices retain their names. (If the relabeling is a
        function, it has to handle all names.)

        In both cases, :meth:`relabel` will complain if the relabeling
        generates as a "new" name a name already in the complex. (This
        detection isn't completely foolproof: just don't do it.) If you want
        to unify simplices, use :meth:`joinSimplices` instead.

        (Be careful with attributes: if a simplex has an attribute the
        value of which is the name of another simplex, then renaming
        will destroy the connection and lead to problems.)

        :param rename: the relabeling, a dict or function
        :returns: a list of simplices with their new names"""

        # force the map to be a function
        if isinstance(rename, dict):
            f = lambda s: rename[s] if s in rename.keys() else s
        else:
            f = rename

        # perform the renaming
        ss = list(self._simplices.keys())   # grab so we can change the structure
        for s in ss:
            sprime = f(s)
            if s != sprime:
                # check it's not in use already
                if sprime in self:
                    raise Exception('Relabeling attempting to re-write {s} to existing simplex {sprime}'.format(s = s, sprime = sprime))

                # change the entry in the simplex dict
                (k, i) = self._simplices[s]
                self._simplices[sprime] = (k, i)
                del self._simplices[s]
            
                # change the entry in the appropriate indices array 
                (self._indices[k])[i] = sprime
            
                # change the entry in the attributes dict
                self._attributes[sprime] = self._attributes[s]
                del self._attributes[s]

        # return the new names of all the simplices
        return self.simplices()


    # ---------- Deleting simplices ----------
    
    def _deleteSimplex( self, s ):
        """Internal method to delete a simplex. This can result
        in a broken complex, so it's almost always better to
        use :meth:`deleteSimplex`.
        
        :param s: the simplex"""

        # each simplex appears in two boundary matrices (for its
        # own order and the order above, if present); in one
        # basis matrix (for its order); in the indices array for
        # its order; and in the attributes dict

        # find the index and order of the simplex
        (k, i) = self._simplices[s]

        # for higher-order simplices, delete from boundary and basis matrices 
        if k > 0:
            # delete from the boundary matrices
            self._boundaries[k] = numpy.delete(self._boundaries[k], i, axis = 1)
            if k < self.maxOrder():
                self._boundaries[k + 1] = numpy.delete(self._boundaries[k + 1], i, axis = 0)

            # delete from the basis matrix
            self._bases[k] = numpy.delete(self._bases[k], i, axis = 1)

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
        
    def deleteSimplex( self, s ):
        """Delete a simplex and all simplices of which it is a part. 
        
        :param s: the simplex"""
        for t in self.partOf(s, reverse = True):
            # delete in decreasing order, down to the basis
            self._deleteSimplex(t)

    def __delitem__(self, s):
        """Delete the simplex and all simplices of which it is a part.
        Equivalent to :meth:`deleteSimplex`.

        :param s: the simplex"""
        self.deleteSimplex(s)

    def deleteSimplexWithBasis( self, bs ):
        """Delete the simplex with the given basis.

        :param bs: the basis"""
        self.deleteSimplex(self.simplexWithBasis(bs))
        
    def deleteSimplices( self, ss ):
        """Delete all simplices in the given list.

        :param ss: the simplices"""
        for s in ss:
            # protect against unfortunate cascades of deletions
            if self.containsSimplex(s):
                self.deleteSimplex(s)
                
    def restrictBasisTo( self, bs ):
        """Restrict the complex to include only those simplices whose 
        bases are wholly contained in the given set of 0-simplices.
        All other simplices, including other 0-simplices, are deleted.
        
        :param bs: the basis
        :returns: the complex"""

        # make sure we have a basis
        self.isBasis(bs, fatal = True)

        # form a column vector with 1s in the rows corresponding to each element
        # in the basis
        sizeOfBasis = len(self._indices[0])
        basisMask = numpy.zeros([ sizeOfBasis ])
        for b in bs:
            (_, i) = self._simplices[b]
            basisMask[i] = 1
        
        # traverse the basis matrices at all orders
        for k in range(1, self.maxOrder() + 1):
            # record any columns which contain 1s in any rows except
            # those corresponding to the given basis
            simplicesToRemove = set()
            nk = len(self._indices[k])
            for i in range(nk):
                c = self._bases[k][:, i]
                # sd: should be able to optimise this within numpy
                for j in range(len(c)):
                    if (c[j] == 1) and (basisMask[j] == 0):
                        # mark simplex for removal
                        s = self._indices[k][i]
                        simplicesToRemove.add(s)
                        break
                    
            # remove all the marked simplices
            for s in simplicesToRemove:
                self._deleteSimplex(s)

        # remove all 0-simplices not in the basis
        for s in self.simplicesOfOrder(0):
            if s not in bs:
                self._deleteSimplex(s)

        # return the now-modified complex itself
        return self
    
        
    # ---------- Accessing simplices ----------
    
    def orderOf( self, s ):
        """Return the order of a simplex.
        
        :param s: the simplex
        :returns: the order of the simplex"""
        try:
            (k, _) = self._simplices[s]
            return k
        except:
            raise Exception('No simplex {s} in complex'.format(s = s))

    def indexOf( self, s ):
        """Return the unique-within-its-order index of the given simplex.
        Indices form a dense sequence. The index isn't robust to changes
        in the complex, so the index returned for a simplex may change if
        simplices are added or removed.

        Note that indices are unique only within the same order, not across
        all simplices; simplex names are however globally unique.

        :param s: the simplex
        :returns: an index"""
        try:
            (_, i) = self._simplices[s]
            return i
        except:
            raise Exception('No simplex {s} in complex'.format(s = s))
        
    def maxOrder( self ):
        """Return the largest order of simplices in the complex, that is
        to say, the largest order for which a call to :meth:`simplicesOfOrder`
        will return a non-empty list.
        
        :returns: the largest order that contains at least one simplex, or -1"""
        return self._maxOrder

    def numberOfSimplicesOfOrder( self ):
        """Return a dict mapping an order to the number of simplices
        of that order in the complex. Use :meth:`simplicesOfOrder` to
        retrieve the actual simplices.
        
        :returns: a list of number of simplices at each order"""
        orders = []
        maxk = self.maxOrder()
        if maxk is not None:
            for k in range(maxk + 1):
                orders.append(len(self._indices[k]))
        return orders

    def simplices( self, reverse = False ):
        """Return all the simplices in the complex. The simplices are
        returned in order of their orders, 0-simplices first unless the
        reverse paarneter is True, in which case 0-simplices will be last.
        
        :param reverse: (optional) reverse the sort order if True
        :returns: a list of simplices"""
        ss = []
        maxk = self.maxOrder()
        if maxk is not None:
            if reverse:
                ks = range(maxk, -1, -1)
            else:
                ks = range(maxk + 1)
            for k in ks:
                # extract all the simplices of the given order and
                # add them in their canonical order
                ss.extend(self._indices[k])
        return ss
                    
    def simplicesOfOrder( self, k ):
        """Return all the simplices of the given order. This will
        be empty for any order greater than that returned by :meth:`maxOrder`.
        
        :param k: the desired order
        :returns: a set of simplices, which may be empty"""
        if k <= self.maxOrder():
            return set(self._indices[k])
        else:
            return set()

    def simplexWithBasis( self, bs, fatal = False ):
        """Return the simplex with the given basis, if it exists
        in the complex. If no such simplex exists, or if the givcen
        set is not a basis, then None is returned; if fatal is True, then
        an exception is raised instead.

        :param bs: the basis
        :param fatal: (optional) make failure raise an exception (defaults to False) 
        :returns: the simplex or None"""
        k = len(bs) - 1

        # check we have a basis
        if not self.isBasis(bs, fatal = fatal):
            return None
        
        # if the order is greater than the maximum, we can't have such a simplex
        if k > self.maxOrder():
            if fatal:
                raise Exception('Complex does not have any simplices of order {k}'.format(k = k))
            else:
                return None

        # an 0-simplex just has to be there (since we know we have a valid basis)
        if k == 0:
            return (list(bs))[0]

        # form the basis column for this basis
        bc = numpy.zeros([ len(self._indices[0]) ])
        for b in bs:
            (_, bi) = self._simplices[b]
            bc[bi] = 1
            
        # check for a simplex with the given basis
        for i in range(len(self._indices[k])):
            #print "check {bs} against {s}".format(bs = bc, s = (self._bases[k])[:, i])
            if ((self._bases[k])[:, i] == bc).all():
                return (self._indices[k])[i]

        # if we get here, there was no such simplex
        if fatal:
            raise Exception('Complex does not have a simplex with basis {bs}'.format(bs = bs))
        else:
            return None

    # sd: this needs optimising
    def simplexWithFaces( self, fs ):
        """Return the simplex that has the given simplices as faces.

        :param fs: the faces
        :returns: the simplex or None"""

        # get the order of simplex we're searching for
        k = len(fs) - 1
        
        # check that the faces have a common order and are the right number
        if k <= 0:
            # not enough faces
            raise Exception('Need at least 1 face')
        else:
            # check all faces are of order (k - 1)
            for f in fs:
                if self.orderOf(f) != k - 1:
                    raise Exception('Simplex of order {k} has faces of order {kmo}, not {fo}'.format(k = k,
                                                                                                     kmo = k - 1,
                                                                                                     fo = self.orderOf(f)))

        # search for simplex
        ffs = set(fs)
        for s in self.simplicesOfOrder(k):
            sfs = self.faces(s)
            if sfs == ffs:
                return s

        # if we get here, we didn't find a simplex with the right faces
        return None

    def allSimplices( self, p, reverse = False ):
        """Return all the simplices that match the given predicate, which should
        be a function from complex and simplex to boolean. The simplices are
        sorted according to their orders.
        
        :param p: a predicate
        :param reverse: (optional) reverse the order 
        :returns: the set of simplices satisfying the predicate"""
        ss = [ s for s in self._simplices if p(self, s) ]
        if reverse:
            return reversed(ss)
        else:
            return ss

    
    # ---------- Testing for simplices ----------

    def containsSimplex( self, s ):
        """Test whether the complex contains the given simplex.
        
        :param s: the simplex
        :returns: True if the simplex is in the complex"""
        return (s in self._simplices.keys())
    
    def __contains__( self, s ):
        """Dict-like interface to :meth:`containsSimplex`.

        :param s: the simplex
        :returns: True if the simplex is in the complex"""
        return self.containsSimplex(s)
    
    def containsSimplexWithBasis( self, bs ):
        """Test whether the complex contains a simplex with the given basis.
        
        :params bs: the basis
        :returns: True is the complex contains a simplex with this basis"""
        return (self.simplexWithBasis(bs) is not None)
    

    # ---------- Attributes ----------
    
    def __getitem__( self, s ):
        """Return the attributes associated with the given simplex.
        
        :param s: the simplex
        :returns: a dict of attributes"""
        return self._attributes[s]
    
    def __setitem__( self, s, attr ):
        """Set the attributes associated with a simplex.
        
        :param s: the simplex
        :param attr: a dict of attributes"""
        self._attributes[s] = attr


    # ---------- Structure of complex, per-simplex level ----------
    
    def faces( self, s ):
        """Return the faces of a simplex.
        
        :param s: the simplex
        :returns: a set of faces"""
        (k, i) = self._simplices[s]
        if k == 0:
            # 0-simplices do not have faces
            return set()

        # extract the column of the boundary matrix
        #print "boundary for {s} order {k} {b}".format(k = k, s = s, b = self._boundaries[k])
        b = (self._boundaries[k])[:, i]
        #print "boundary of {s} is {b}".format(s = s, b = b)

        # extract the simplex names from this column
        fs = set()
        for i in range(len(b)):
            if b[i] == 1:
                #print "add index {i} = {id}".format(i = i, id = (self._indices[k - 1])[i])
                fs.add((self._indices[k - 1])[i])
        return fs
    
    def faceOf( self, s ):
        """Return the simplices that the given simplex is a face of. This
        is not transitive: all the simplices returned will be of an order
        one greater than the given simplex. The transitive closure of
        :meth:`faceOf` is :meth:`partOf`.
        
        :param s: the simplex
        :returns: a list of simplices"""
        (k, i) = self._simplices[s]
        if k == self.maxOrder():
            # simplex is of maximal order, so isn't a face or a larger simplex
            return set()
        else:
            # convert the 1s into simplex names of the faces
            ss = self._indices[k + 1]
            fs = numpy.compress((self._boundaries[k + 1])[i], ss)
            return list(fs)            

    def _partOf( self, s, k ):
        """Internal method to find the star of a simplex. The simplices
        are returned mixed-up, which :meth:`partOf` then corrects.

        :param s: the simplex
        :param k: the order of s"""
        ps = set()
        for f in self.faceOf(s):
            ps.add((k + 1, f))
            ps.update(self._partOf(f, k + 1))
        return ps
        
    def partOf( self, s, reverse = False, exclude_self = False ):
        """Return the transitive closure of all simplices of which the simplex
        is part: a face of, or a face of a face of, and so forth. This is
        the dual of :meth:`closureOf`. If exclude_self is False (the default),
        the set include the simplex itself. The simplices are returned
        in increasing order unless reverse is True, in which case
        they are returned largest order first.

        In some of the topology literature this operation is called the star.

        This method is essentially the dual of :meth:`parclosureOf`, looking
        up the simplex orders rather than down.
        
        :param s: the simplex
        :param reverse: (optional) reverse the sort order (defaults to False)
        :param exclude_self: (optional) exclude the simplex itself (default to False)
        :returns: the list of simplices the simplex is part of"""
        
        # get the set of simplices we're part of, with their orders
        k = self.orderOf(s)
        psos = self._partOf(s, k)

        # order the simplices
        spsos = sorted(psos, key = (lambda ka: ka[0]), reverse = reverse)

        # extract just the simplices
        sps = list(map((lambda ka: ka[1]), spsos))

        # add the initial simplex if required
        # sd: this is the opposite logic to that of the argument, because the
        # initial simplex won't be added to the list by the recursive
        # process that builds it
        if not exclude_self:
            if reverse:
                sps.append(s)
            else:
                sps.insert(0, s)

        # return the list
        return sps
        
    def basisOf( self,  s ):
        """Return the basis of a simplex, the set of 0-simplices that
        define it.
        
        :param s: the simplex
        :returns: the set of 0-simplices that form the basis of s"""
        (k, si) = self._simplices[s]
        bk = (self._bases[k])[:, si]
        #print "simplex {s} basis column {bk}".format(s = s, bk = bk)
        bs = set()
        for i in range(len(bk)):
            if bk[i] == 1:
                bs.add((self._indices[0])[i])
        #print "basis {bs}".format(bs = bs)
        return bs
    
    def closureOf( self, s, reverse = False, exclude_self = False ):
        """Return the closure of a simplex. The closure is defined
        as the simplex plus all its faces, transitively down to its basis.
        If exclude_self is True, the closure excludes the simplex itself.
        
        This method is essentially the dual of :meth:`partOf`, looking
        down the simplex orders rather than up.

        By default the simplices are returned in increasing order, basis first:
        setting reverse to True will generate the simplices in decreasing order,
        highest order first.

        :param s: the simplex
        :param reverse: (optional) return simplex in decreasing order (defaults to False)
        :param exclude_self: (optional) exclude the simplex itself (defaults to False)
        :returns: the closure of the simplex"""
        k = self.orderOf(s)
        cs = dict()
        cs[k] = set([ s ])

        # work down the orders extracting faces
        for fk in range(k, 0, -1):
            cs[fk - 1] = set()
            for t in cs[fk]:
                cs[fk - 1].update(self.faces(t))

        # return the simplices in the requested order, excluding the
        # top simplex if requested
        ss = []
        if exclude_self:
            topk = k - 1
        else:
            topk = k
        if reverse:
            for fk in range(topk, -1, -1):
                ss = ss + list(cs[fk])
        else:
            for fk in range(0, topk + 1):
                ss = ss + list(cs[fk])
        return ss 


    # ---------- Euler characteristic and integration ----------
    
    def eulerCharacteristic( self ):
        """Return the Euler characteristic of this complex, which is a
        measure of its topological structure.
        
        :returns: the Euler characteristic"""
        euler = 0
        orders = self.numberOfSimplicesOfOrder()
        for k in range(len(orders)):
            euler = euler + pow(-1, k) * orders[k]
        return euler
    
    def eulerIntegral( self, observation_key = 'height' ):
        """Perform an Euler integraton across a simplicial complex
        using the value of a particular attribute.
    
        :param c: the complex
        :param observation_key: the attribute to integrate over (defaults to 'height')"""

        # compute maximum "height"
        maxHeight = max([ self[s][observation_key] for s in self.simplices() ])

        # perform the integration over the level sets
        a = 0
        for s in xrange(maxHeight + 1):
            # form the level set
            # sd TODO: the level set is uniformly growing as s decreases, so we can optimise?
            cprime = copy.deepcopy(self)
            bs = cprime.allSimplices(lambda csp: self.orderOf(csp[1]) == 0 and
                                                 self[csp[1]][observation_key] > s)
            cprime.restrictBasisTo(bs)
            
            # compute the Euler characteristic of the level set
            chi = cprime.eulerCharacteristic()
            #print 'level {level}, chi = {chi}'.format(level = s, chi = chi)
            
            # add to the integral
            a = a + chi

        # return the accumulated integral
        return a


    # ---------- Homology ----------

    def isChain( self, ss, p = None, fatal = False ):
        """Test whether the given set of simplices is a p-chain for some order p. A
        p-chain is a collection of simplices of order p. If fatal is True then any
        missing or wrong-order simplices raise an exception.

        A :term:`basis` is an 0-chain (see :meth:`isBasis`).

        :param ss: the simplices
        :param p: (optional) the order (defaults to the order of the first simplex in the chain)
        :param fatal: (optional) raise an exception for invalid chains (defaults to False)
        :returns: True if the simplices form a p-chain"""

        # a list of no simplices is a p-chain by default
        if len(ss) == 0:
            return True
        
        # fill in defaults
        if p is None:
            p = self.orderOf(ss[0])

        # check all simplices
        for s in ss:
            # check the simplex exists
            if s not in self:
                if fatal:
                    raise Exception('{p}-chain contains non-existent simplex {s}'.formats(p = p, s = s))
                else:
                    return False
                
            # check the simplex' order
            sk = self.orderOf(s)
            if sk != p:
                if fatal:
                    raise Exception('{p}-chain contains simplex {s} of order {sk}'.formats(p = p, s = s, sk = sk))
                else:
                    return False
        return True

    def boundary( self, ss ):
        """Return the :term:`boundary` of the given :term:`p-chain`. This will be a (p - 1)-chain
        of simplices from the complex.

        :param ss: a chain (list) of simplices
        :returns: the boundary of the chain"""

        # an empty p-chain has no boundary
        ss = list(ss)
        if len(ss) == 0:
            return set()
        
        # check we have a valid chain and get its order
        self.isChain(ss, fatal = True)
        p = self.orderOf(ss[0])

        # extract the boundary
        bs = set()
        for s in ss:
            # extract the boundary of this simplex
            fs = self.faces(s)

            # any simplices in both sets aren't in the boundary; any not
            # in the boundary should be added
            bs ^= fs
        return bs
        
    def boundaryMatrix( self, k ):
        """Return the :term:`boundary operator` of the k-simplices in the 
        complex as a `numpy` matrix. The columns correspond to
        simplices of order k while rows correspond to simplices
        of order (k - 1). The matrix has a 1 when a (k - 1) simplex 
        is a face of the corresponding k-simplex, and 0 otherwise.

        The boundary of the 0-simplices is a matrix with one row,
        all zeros. The boundary of an order greater than the maximum
        order of the complex is a 0x0 matrix.

        :param k: the order of simplices
        :returns: the boundary matrix"""
        if k == 0:
            # return a row of zeros
            return numpy.zeros([ 1, len(self._indices[0]) ])
        else:
            if k > self.maxOrder():
                # return a null boundary operator
                return numpy.zeros([ 0, 0 ])
            else:
                return self._boundaries[k]

    def disjoint( self, ss ):
        """Test whether the elements of a set of simplices are disjoint,
        defined as if they share no common simplices in their closures.
        (This doesn't mean that they aren't part of a common super-simplex,
        however.) The simplices need not be of the same order, i.e., need
        not form a p-chain.

        :param ss: the simplices
        :returns: True if the simplices are disjoint"""
        cl = None
        for s in ss:
            if cl is None:
                # first simplex, grab its closure
                cl = set(self.closureOf(s))
            else:
                # next simplex, check for intersection of closure
                clprime = set(self.closureOf(s))
                if cl.isdisjoint(clprime):
                    # closures are disjoint, unify them
                    cl = cl.update(clprime)
                else:
                    # closures intersect, we fail
                    return False

        # if we get here, all the simplices were disjoint
        return True

    def smithNormalForm( self, B ):
        """Reduce a boundary matrix to Smith Normal Form, which has a leading diagonal
        of 1s for some number of rows, and is everywhere else zero.

        :param b: the boundary matrix to reduce
        :returns: the Smith Normal Form of the boundary matrix"""
        return self._reduce(B, 0)
    
    def _reduce( self, Bin, x = 0 ):
        """Reduce a boundary matrix to Smith Normal Form.
        The algorithm is taken from `here <https://www.cs.duke.edu/courses/fall06/cps296.1/Lectures/sec-IV-3.pdf>`_.
        Note that this is simpler than other algorithms in the literature because
        we're working over a binary field.

        :param b: the boundary matrix to reduce
        :param x: the row/column being reduced, initially 0
        :returns: the Smith Normal Form of the boundary matrix"""

        # check we're still in scope
        (rb, cb) = Bin.shape
        if x >= min([ rb, cb ]):
            # no, return the reduced matrix
            return Bin

        #  check if we have another row to reduce
        for k in range(x, rb):
            for l in range(x, cb):
                if Bin[k, l] == 1:
                    # yes, make a copy of the matrix
                    B = Bin.copy()
                                    
                    # exchange rows x and k
                    B[[x, k], :] = B[[k, x], :]

                    # exchange columns x and l
                    B[:, [x, l]] = B[:, [l, x]]

                    # zero the x column in subsequent rows
                    for i in range(x + 1, rb):
                        if B[i, x] == 1:
                            B[i, :] = (B[i, :] + B[x, :]) % 2

                    # ...and the x row in subsequent columns
                    for j in range(x + 1, cb):
                        if B[x, j] == 1:
                            B[:, j] = (B[:, j] + B[:, x]) % 2

                    # move to the next row
                    return self._reduce(B, x + 1)

        # if we get here, we're fully reduced
        return Bin

    def bettiNumbers( self, ks = None ):
        """Return a dict of Betti numbers for the different dimensions
        of the complex.

        :param ks: (optional) dimensions to compute (defaults to all)
        :returns: a dict of Betti numbers"""
        
        # fill in the default
        if ks is None:
            ks = range(self.maxOrder() + 1)

        # compute the Betti numbers
        boundary = dict()
        betti = dict()
        for k in ks:
            # compute the reduced boundary operator matrices if we
            # haven't already done so
            if k not in boundary.keys():
                boundary[k] = self.smithNormalForm(self.boundaryMatrix(k))
            A = boundary[k]
            if k + 1 not in boundary.keys():
                boundary[k + 1] = self.smithNormalForm(self.boundaryMatrix(k + 1))
            B = boundary[k + 1]

            # dimensions of boundary matrices
            (ra, ca) = A.shape
            (rb, cb) = B.shape

            # compute the ranks of the Z_k and B_k groups
            zc = numpy.zeros(ra)
            kernelDim = [ numpy.all(A[:, j] == zc) for j in range(ca) ].count(True) # zero columns 
            zr = numpy.zeros(cb)
            imageDim = [ numpy.all(B[i, :] == zr) for i in range(rb) ].count(False) # non-zero rows
            betti[k] = kernelDim - imageDim

        return betti


    # ---------- Derived complexes ----------

    def _isClosed( self, boundary, fs ):
        """Determine whether the given set of (k + 1) faces forms the
        boundary of a k-simplex according to the boundary operator.
        The faces are given by indices into the boundary matrix. They
        are closed if, when we sum the columns corresponding to them,
        the result consists of values that are 0 (mod 2), i.e., if
        every face connects either 0 or an even number of simplices.

        :param boundary: the boundary matrix
        :param fs: list of face indices
        :returns: True if the faces form a closed k-simplex"""

        # extract and sum columns
        s = numpy.sum(boundary[:, fs], axis = 1) % 2
        
        # check we only have 2 or 0 in all positions
        return numpy.all(numpy.logical_or(s == 2, s == 0))

    def _completePotentialSimplices( self, nss ):
        """Grow a flag complex via the addition of the given simplices. The
        intuition is that adding a small number of new simplices leads to a
        growth in the flag complex as new potential simplices are completed,
        while cutting down the number of combinations of simplices that need checking. 

        :param nss: a dict of order to sets of simplex indices of the added simplices"""
        
        # work up the simplex orders
        k = 1
        maxk = max(nss.keys())
        while k <= (maxk + 1):
            k = k + 1
            if ((k - 1) not in nss.keys()) or (len(nss[k - 1]) == 0):
                # no new simplices to form faces of any new simplices at this order
                continue
            if k not in nss.keys():
                 # create a new set into which to add created simplex indices
                nss[k] = set()
                   
            # grab the boundary matrix of the faces
            boundary = self.boundaryMatrix(k - 1)
            
            # test all coilections of (k + 1) (k - 1)-simplices that include
            # at least one of the new simplicies to see whether they close
            # a new simplex at the higher order
            ks = len(self._indices[k - 1])
            for fs in [ set(fs) for fs in itertools.combinations(range(ks), k + 1) ]:
                if not nss[k - 1].isdisjoint(fs):
                    if self._isClosed(boundary, list(fs)):
                        # simplices form a boundary, add to the
                        # flag complex (if it doesn't already exist)
                        # sd: this could be a lot more optimised
                        cfs = [ self._indices[k - 1][i] for i in fs ]
                        if self.simplexWithFaces(cfs) is None:
                            s = self.addSimplex(fs = cfs)
                            (_, i) = self._simplices[s]
                            nss[k].add(i)
                            maxk = k
        
    def flagComplex( self ):
        """Generate the :term:`flag complex` of this complex. The flag complex
        is formed by creating all the "implied" simplices for which all
        faces are present. For example, three 1-simplices forming an
        (empty) triangle will be "closed" by creating a 2-simplex
        with them as its faces. This may in turn allow a further
        3-simplex to be formed if the new 2-simplex closes a tetrahedron,
        and so forth.

        :returns: the flag complex"""

        # start with a copy of ourselves
        flag = copy.copy(self)

        # we work from the bottom with all 1-simplices
        nss = dict()
        nss[1] = set(range(len(flag.simplicesOfOrder(1))))
        flag._completePotentialSimplices(nss)

        return flag

    def growFlagComplex( self, newSimplices ):
        """Grow the :term:`flag complex` incrementally  by filling-in any
        higher-order simplices formed by the addition of a set of new
        simplices to the complex.

        The set of new simplices can contain simplices of any order,
        although 0-simplices will have no effect. For a lot of applications
        (for example for building a :term:`Vietoris-Rips complex`) the new
        simplices willm all be 1-simplices (edges).

        :param newSimplices: a collection of new simplices"""

        # convert a list of simplices to a dict of sets of indices, keyed by order
        nss = dict()
        for s in newSimplices:
            (k, i) = self._simplices[s]
            if k not in nss.keys():
                nss[k] = set([ i ])
            else:
                nss[k].add(i)

        # extend the complex
        self._completePotentialSimplices(nss)
