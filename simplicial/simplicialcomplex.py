# Base class for simplicial complexes
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

import numpy
import copy
import itertools


class SimplicialComplex(object):
    '''A finite abstract simplicial complex.
    
    A simplicial :term:`complex` is a generalisation of a network in which
    vertices (0-simplices) and edges (1-simplices) can be composed
    into triangles (2-simplices), tetrahedrons (3-simplices) and so
    forth. This class actually implements closed simplicial complexes
    that contain every simplex, every :term:`face` of that simplex, every face
    of those simplices, and so forth. Operations to add and remove
    simplices cascade to keep the complex closed: if a simplex is an
    element of a complex, then all its faces are also elements, and so
    on recursively.

    The class also includes some topological operations, notably for
    computing the :term:`Euler characteristic` of a complex and
    performing Euler integration, and for computational :term:`homology`.

    '''

    # ---------- Initialisation and helpers ----------
    
    def __init__( self ):
        self._sequence = 1           # sequence number for generating simplex names
        self._simplices = dict()     # dict from simplex to faces
        self._attributes = dict()    # dict from simplex to attributes 
        self._faces = dict()         # dict from simplex to simplices of which it is a face

    def _newUniqueIndex( self, d ):
        '''Generate a new unique identifier for a simplex. The default naming
        scheme uses a sequence number and a leading dimension indicator. Users
        can name simplices anything they want to get meaningful names. 
        
        :param d: dimension of the simplex to be identified
        :returns: an identifier not currently used in the complex'''
        i = self._sequence
        while True:
            id = '{dim}d{id}'.format(dim = d, id = i)
            if id not in self._simplices.keys():
                self._sequence = i + 1
                return id
            else:
                i = i + 1
    
    def _orderIndices( self, ls ):
        '''Return the list of simplex indices in a canonical order. (The
        exact order doesn't matter, it simply ensures consistent naming.)
        
        :param ls: a list of simplex names
        :returns: the simplex names in canonical order'''
        return sorted(ls)


    # ---------- Adding simplices ----------
    
    def addSimplex( self, fs = [], id = None, attr = None, ignoreDuplicate = False ):
        '''Add a simplex to the complex whose faces are the elements of fs.
        If no faces are given then the simplex is a 0-simplex (point).
        If no id is provided one is created. If present, attr should be a
        dict of attributes for the simplex.

        If ignoreDuplicate is False, n exception will be thrown if a simplex
        with the given faces already exists in the complex. If ignoreDuplicate is
        true, the new simplex will be ignored.

        To add a simplex from its basis (rather than its faces) use
        :meth:`addSimplexByBasis`.
        
        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) name for the simplex 
        :param attr: (optional) dict of attributes
        :param ignoreDuplicate: if True, silently drop addition of duplicate simplex
        :returns: the name of the new simplex'''
        
        # fill in defaults
        if id is None:
            # no identifier, make one
            id = self._newUniqueIndex(max(len(fs) - 1, 0))
        else:
            # check we've got a new id
            if id in self._simplices.keys():
                raise Exception('Duplicate simplex {id}'.format(id = id))
        if attr is None:
            # no attributes
            attr = dict()

        # we need at least two faces, defining at least a 1-simplex, since
        # 0-simplices don't have any faces
        if len(fs) == 1:
            raise Exception('Need at least two faces, defining a 1-simplex')
        
        # place faces into canonical order
        ofs = self._orderIndices(fs)
        
        # sanity check that we know all the faces, and that they're all of the
        # correct order to be faces of this simplex
        os = len(ofs) - 1
        for f in ofs:
            if f not in self._simplices.keys():
                raise Exception('Unknown simplex {id}'.format(id = f))
            of = self.orderOf(f)
            if of != os - 1:
                raise Exception('Face {id} is of order {of}, not {os}'.format(id = f,
                                                                              of = of,
                                                                              os = os - 1))

        # sanity check that we don't already have a simplex with these faces
        if os > 0:
            s = self.simplexWithFaces(ofs)
            if s is not None:
                if ignoreDuplicate:
                    # simplex exists but ignoring duplicates, so exit
                    return
                else:
                    raise Exception('Already have a simplex {s} with faces {ofs}'.format(s = s,
                                                                                         ofs = ofs))
        
        # add simplex and its attributes
        self._simplices[id] = ofs 
        self._attributes[id] = attr
        self._faces[id] = []
        
        # record the faces
        for f in ofs:
            self._faces[f].append(id)

        # return the simplex' name
        return id

    def addSimplexWithBasis( self, bs, id = None, attr = None, ignoreDuplicate = False ):
        '''Add a simplex by providing its basis, which uniquely defines it.
        This method adds all the simplices necessary to define the new
        simplex, using :meth:`simplexByBasis` to find and re-use any that are
        already in the complex.

        To add a simplex defined by its faces, use :meth:`addSimplex`.

        If ignoreDuplicate is False, n exception will be thrown if a simplex
        with the given basis already exists in the complex. If ignoreDuplicate is
        true, the new simplex will be ignored.

        Defining a k-simplex requires a (k + 1) basis. All elements of
        the basis must be 0-simplices.

        :param bs: the basis
        :param id: (optional) the name of the new simplex
        :param attr: (optional) dict of attributes
        :param ignoreDuplicate: if True, silently drop addition of duplicate simplex
        :returns: the name of the new simplex'''
        so = len(bs) - 1   # order of the final simplex
        fs = []            # faces in the final simplex

        # make sure the list is a basis
        for b in bs:
            if b in self._simplices.keys():
                # simplex exists, check it's an 0-simplex
                if self.orderOf(b) > 0:
                    raise Exception('Higher-order simplex {s} in basis set'.format(s = b))
                else:
                    s = b
            else:
                # simplex doesn't exist, create it
                s = self.addSimplex(id = b)

                # if we're creating an 0-simplex, we're now done
                if so == 0:
                    return s

            # capture the simplex as a face if we're building a 1-simplex
            if so == 1:
                fs.append(s)

        # check if we have a simplex with this basis
        s = self.simplexWithBasis(bs)
        if s is not None:
            if ignoreDuplicate:
                # duplicate simplex and we're ignoring, so return
                return s
            else:
                raise Exception('Simplex {s} with basis {bs} already exists'.format(s = s,
                                                                                    bs = bs))

        # create a name for the new simplex if needed
        if id is None:
            id = self._newUniqueIndex(so)

        # iterate up through all the simplex orders, creating
        # any missing ones and capturing the faces for the final simplex
        for k in xrange(1, so):
            # find all the bases for the simplices of this order
            bss = set(itertools.combinations(bs, k + 1))
            for pbs in bss:
                # do we have the simplex with this basis?
                s = self.simplexWithBasis(pbs)
                if s is None:
                    # no, create it
                    s = self.addSimplexWithBasis(pbs)

                # if we're at the final order, capture the simplex as a face
                if k == so - 1:
                    fs.append(s)

        # create the final simplex and return it
        s = self.addSimplex(id = id,
                            fs = fs,
                            attr = attr) 
        return s

    def addSimplexOfOrder( self, o, id = None ):
        '''Add a new simplex, disjoint from all others, with the given order.
        This will create all the necessary faces and so on down to a new
        basis.

        :param o: the order of the new simplex
        :param id: (optional) name of the new simplex
        :returns: the name of the new simplex'''
        if o == 0:
            # it's an 0-simplex, just try to create a new one
            return self.addSimplex(id = id)
        else:
            # create a basis of new names
            bs = []
            for i in xrange(o + 1):
                bs.append(self._newUniqueIndex(0))

            # create the new simplex and return it
            return self.addSimplexWithBasis(bs, id)
    
    def addSimplicesFrom( self, c, rename = None ):
        '''Add simplices from the given complex. The rename parameter
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
        :returns: a list of simplex names'''

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
                                 fs = map(f, c.faces(s)),
                                 attr = c[s])
            ns.append(id)
        return ns


    # ---------- Relabelling ----------
    
    def relabel( self, rename ):
        '''Re-label simplices using the given relabeling, which may be a
        dict from old names to new names or a function taking a name
        and returning a new name.

        If the relabeling is a dict it may be incomplete, in which
        case unmentioned simplices retain their names. (If the relabeling is a
        function, it has to handle all names.)

        In both cases, :meth:`relabel` will complain if the relabeling
        generates as a "new" name a name already in the complex. (This
        detection isn't completely foolproof: just don't do it.) If you want
        to unify simplices, use :meth:`unifyBasis` instead.

        (Be careful with attributes: if a simplex has an attribute the
        value of which is the name of another simplex, then renaming
        will destroy the connection and lead to problems.)

        :param rename: the relabeling, a dict or function
        :returns: a list of new names used

        '''

        # force the map to be a function
        if isinstance(rename, dict):
            f = lambda s: rename[s] if s in rename.keys() else s
        else:
            f = rename

        # perform the renaming
        newSimplices = dict()
        newFaces = dict()
        newAttributes = dict()
        for s in self._simplices.keys():
            t = f(s)
            if s != t and self.containsSimplex(t):
                raise Exception('Relabeling attempting to re-write {s} to existing name {t}'.format(s = s, t = t))
            newSimplices[t] = map(f, self._simplices[s])
            newFaces[t] = map(f, self._faces[s])
            newAttributes[t] = copy.copy(self._attributes[s])

        # replace the old names with the new
        self._simplices = newSimplices
        self._faces = newFaces
        self._attributes = newAttributes

        # return the new names of all the simplices
        return self.simplices()


    # ---------- Deleting simplices ----------
    
    def _deleteSimplex( self, s ):
        '''Delete a simplex. This can result in a broken complex, so
        it's almost always better to use :meth:`deleteSimplex`.
        
        :param s: the simplex'''

        # delete the simplex from the face lists of its faces
        ts = self.faces(s)
        for t in ts:
            self._faces[t].remove(s)
            
        # delete the simplex' elements
        del self._simplices[s]
        del self._attributes[s]
        del self._faces[s]
        
    def deleteSimplex( self, s ):
        '''Delete a simplex and all simplices of which it is a part. 
        
        :param s: the simplex'''
        for t in self.partOf(s, reverse = True):
            # delete in decreasing order, down to the basis
            self._deleteSimplex(t)

    def deleteSimplices( self, ss ):
        '''Delete all simplices in the given list.

        :param ss: the simplices'''
        for s in ss:
            # protect against unfortunate cascades of deletions
            if self.containsSimplex(s):
                self.deleteSimplex(s)
                
    def __delitem__( self, s ):
        '''Delete the simplex and all simplices of which it is a part.
        Equivalent to :meth:`deleteSimplex`.
        
        :param s: the simplex'''
        self.deleteSimplex(s)

    def restrictBasisTo( self, bs ):
        '''Restrict the complex to include only those simplices whose 
        bases are wholly contained in the given set of 0-simplices.
        
        :param bs: the basis
        :returns: the complex'''
        bs = set(bs)
        
        # make sure we have a set of 0-simplices
        for s in bs:
            if self.orderOf(s) > 0:
                raise Exception('Higher-order simplex {s} in basis set'.format(s = s))
        
        # find all simplices that need to be excluded
        remove = set([])
        for s in self._simplices:
            if self.orderOf(s) == 0:
                # it's a vertex, is it in the set?
                if s not in bs:
                    # no, mark it for dropping
                    remove.add(s)
            else:
                # it's a higher-order simplex, is its basis wholly in the set?
                sbs = self.basisOf(s)
                if not sbs <= bs:
                    # basis is not wholly contained, mark it for removal
                    remove.add(s)
        
        # close the set of simplices to be removed
        for r in remove:
            rs = remove.union(self.partOf(r))
            
        # remove the marked simplices
        for s in self._orderSortedSimplices(remove, reverse = True):
            self._deleteSimplex(s)

        
    # ---------- Accessing simplices ----------
    
    def orderOf( self, s ):
        '''Return the order of a simplex.
        
        :param s: the simplex
        :returns: the order of the simplex'''''
        return max(len(self.faces(s)) - 1, 0)
    
    def maxOrder( self ):
        '''Return the largest order of simplices in the complex, that is
        to say, the largest order for which a call to :meth:`simplicesOfOrder`
        will return a non-empty list.
        
        :returns: the largest order that contains at least one simplex, or None'''
        if len(self._simplices) == 0:
            return None
        else:
            os = [ self.orderOf(s) for s in self._simplices ]
            return max(os)
    
    def numberOfSimplicesOfOrder( self ):
        '''Return a dict mapping an order to the number of simplices
        of that order in the complex.
        
        :returns: a dict mapping order to number of simplices'''
        orders = dict()
        for s in self._simplices:
            o = self.orderOf(s)
            if o not in orders:
                orders[o] = 1
            else:
                orders[o] = orders[o] + 1
        return orders

    def _orderCmp( self, s, t ):
        '''Comparison function for simplices based on their order.

        :param s: the first simplex
        :param t: the second simplex
        :returns: -1, 0, 1 for less than, equal, greater than'''
        return cmp(self.orderOf(s), self.orderOf(t))

    def _orderSortedSimplices( self, ss, reverse = False ):
        '''Return the list of simplices sorted into increasing order
        of their order, or decreasing order if revere is True.
        :param ss: the simplices
        :param reverse: (optional) sort in decreasing order
        :returns: the list of simplices in increasing/decreasing order of order'''
        return sorted(ss,
                      cmp = lambda s, t: self._orderCmp(s, t),
                      reverse = reverse)
        
    def simplices( self, reverse = False ):
        '''Return all the simplices in the complex. The simplices come
        out in order of their orders, so all the 0-simplices
        first, then all the 1-simplices, and so on: if the reverse
        parameter is `True`, then the order is reversed.
        
        :param reverse: (optional) reverse the sort order if True
        :returns: a list of simplices'''
        return self._orderSortedSimplices(self._simplices, reverse)

    def simplicesOfOrder( self, o ):
        '''Return all the simplices of the given order. This will
        be empty for any order not returned by :meth:`orders`.
        
        :param o: the desired order
        :returns: a set of simplices, which may be empty'''
        ss = []
        for s in self._simplices:
            if max(len(self.faces(s)) - 1, 0) == o:
                ss.append(s)
        return set(ss)

    def simplexWithBasis( self, bs ):
        '''Return the simplex with the given basis, if it exists
        in the complex. All elements of the basis must be 0-simplices.

        :param bs: the basis
        :returns: the simplex or None'''

        # sanity check
        for s in bs:
            if self.orderOf(s) > 0:
                raise Exception('Higher-order simplex {s} in basis set'.format(s = s))

        # check for a simplex with the given basis
        so = len(bs) - 1
        ss = None
        for s in bs:
            ps = set([ p for p in self.partOf(s) if self.orderOf(p) == so ])
            if ss is None:
                ss = ps
            else:
                ss &= ps
            if len(ss) == 0:
                # no way to get a simplex, bail out
                return None

        # if we get here, we've found the simplex
        # sd: should we check that the set size is 1, just for safety?
        return ss.pop()

    def simplexWithFaces( self, fs ):
        '''Return the simplex that has the given simplices as faces.

        :param fs: the faces
        :returns: the simplex or None'''

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
                    raise Exception('Simplex of order{k} has faces of order {kmo}, not {fo}'.format(k = k,
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

    def containsSimplex( self, s ):
       '''Test whether the complex contains the given simplex.

       :param s: the simplex
       :returns: True if the simplex is in the complex'''
       return (s in self._simplices.keys())

    def containsSimplexWithBasis( self, bs ):
        '''Test whether the complex contains a simplex with the given basis.

        :params bs: the basis
        :returns: True is the complex contains a simplex with this basis'''
        return (self.simplexWithBasis(bs) is not None)
    
    def allSimplices( self, p, reverse = False ):
        '''Return all the simplices that match the given predicate, which should
        be a function from complex and simplex to boolean. The simplices are
        sorted according to their orders.
        
        :param p: a predicate
        :param reverse: (optional) reverse the order 
        :returns: the set of simplices satisfying the predicate'''
        return self._orderSortedSimplices([ s for s in self._simplices if p(self, s) ], reverse)

    
    # ---------- Attributes ----------
    
    def __getitem__( self, s ):
        '''Return the attributes associated with the given simplex.
        
        :param s: the simplex
        :returns: a dict of attributes'''
        return self._attributes[s]
    
    def __setitem__( self, s, attr ):
        '''Set the attributes associated with a simplex.
        
        :param s: the simplex
        :param attr: the attributes'''
        self._attributes[s] = attr


    # ---------- Structure of complex, per-simplex level ----------
    
    def faces( self, s ):
        '''Return the faces of a simplex.
        
        :param s: the simplex
        :returns: a set of faces'''
        return set(self._simplices[s])
    
    def faceOf( self, s ):
        '''Return the simplices that the given simplex is a face of. This
        is not transitive: all the simplices returned will be of an order
        one greater than the given simplex. The transitive closure of
        :meth:`faceOf` is :meth:`partOf`.
        
        :param s: the simplex
        :returns: a list of simplices'''''
        return self._faces[s]
    
    def partOf( self, s, reverse = False, exclude_self = False ):
        '''Return the transitive closure of all simplices of which the simplex
        is part: a face of, or a face of a face of, and so forth. This is
        the dual of :meth:`closureOf`. If exclude_self is False (the default),
        the set include the simplex itself.

        In some of the topology literature this operation is called the star.
        
        :param s: the simplex
        :param reverse: (optional) reverse the sort order
        :param exclude_self: (optional) exclude the simplex itself (default to False)
        :returns: the list of simplices the simplex is part of'''
        if exclude_self:
            parts = set()
        else:
            parts = set([ s ])
        fs = self._faces[s]
        for f in fs:
            parts |= set(self.partOf(f))
        return self._orderSortedSimplices(parts, reverse)
        
    def basisOf( self,  s ):
        '''Return the basis of a simplex, the set of 0-simplices that
        define its faces. The length of the basis is equal to one more
        than the order of the simplex.
        
        :param s: the simplex
        :returns: the set of simplices that form the basis of s'''

        # sd: not the most elegant way to do this....
        return set([ f for f in self.closureOf(s) if self.orderOf(f) == 0 ])  
    
    def closureOf( self, s, reverse = False, exclude_self = False ):
        '''Return the closure of a simplex. The closure is defined
        as the simplex plus all its faces, transitively down to its basis.
        If exclude_self is True, the closure excludes the simplex itself.

        :param s: the simplex
        :param reverse: (optional) reverse the sort order 
        :param exclude_self: (optional) exclude the simplex itself (defaults to False)
        :returns: the closure of the simplex'''

        def _close( t ):
            fs = self.faces(t)
            if len(fs) == 0:
                # 0-simplex, return it
                return set([ t ])
            else:
                # k-simplex, return a list of it and its faces
                faces = set()
                for f in fs:
                    faces = faces.union(_close(f))
                faces = faces.union(set([ t ]))
                return faces

        ss = _close(s)
        if exclude_self:
            ss.remove(s)
        return self._orderSortedSimplices(ss, reverse)


    # ---------- Euler characteristic and integration ----------
    
    def  eulerCharacteristic( self ):
        '''Return the Euler characteristic of this complex, which is a
        measure of its topological structure.
        
        :returns: the Euler characteristic'''
        euler = 0
        orders = self.numberOfSimplicesOfOrder()
        for o, n in orders.iteritems():
            euler = euler + pow(-1, o) * n
        return euler
    
    def eulerIntegral( self, observation_key = 'height' ):
        '''Perform an Euler integraton across a simplicial complex
        using the value of a particular attribute.
    
        :param c: the complex
        :param observation_key: the attribute to integrate over (defaults to 'height')'''

        # compute maximum "height"
        maxHeight = max([ self[s][observation_key] for s in self.simplices() ])

        # perform the integration over the level sets
        a = 0
        for s in xrange(maxHeight + 1):
            # form the level set
            # sd TODO: the level set is uniformly growing as s decreases, so we can optimise?
            cprime = copy.deepcopy(self)
            bs = cprime.allSimplices(lambda c, sp: self.orderOf(sp) == 0 and
                                                   self[sp][observation_key] > s)
            cprime.restrictBasisTo(bs)
            
            # compute the Euler characteristic of the level set
            chi = cprime.eulerCharacteristic()
            #print 'level {level}, chi = {chi}'.format(level = s, chi = chi)
            
            # add to the integral
            a = a + chi

        # return the accumulated integral
        return a


    # ---------- Homology ----------

    def boundary( self, ss ):
        '''Return the boundary of the given p-chain. This will be a (p - 1)-chain
        of simplices from the complex.

        :param ss: a chain (list) of simplices
        :returns: the boundary of the chain'''
        bs = set()
        p = None
        for s in ss:
            if p is None:
                # first simplex, work out the order of p-chain we're looking at
                p = self.orderOf(s)
            else:
                # later simplex, make sure it's the right order
                if self.orderOf(s) != p:
                    raise Exception('{p}-chain contains simplex of order {q}'.format(p = p,
                                                                                     q = self.orderOf(s)))

            # extract the boundary of this simplex
            fs = self.faces(s)

            # any simplices in both sets aren't in the boundary; any not
            # in the boundary should be added
            bs ^= fs
        return bs
        
    def boundaryMatrix( self, k ):
        '''Return the :term:`boundary operator` of the k-simplices in the 
        complex as a `numpy` matrix. The columns correspond to
        simplices of order k while rows correspond to simplices
        of order (k - 1). The matrix has a 1 when a (k - 1) simplex 
        is a face of the corresponding k-simplex, and 0 otherwise.

        The boundary of the 0-simplices is a matrix with one row,
        all zeros. The boundary of an order greater than the maximum
        order of the complex is a 0x0 matrix.

        :param k: the order of simplices
        :returns: the boundary matrix'''

        # extract simplices at this order
        n = self.numberOfSimplicesOfOrder()

        # if we're after order 0, return  a row of zeros
        if k == 0:
            return numpy.zeros([ 1, n[k] ])

        # if we're after an order greater than our maximum order, return a zero matrix
        if k > self.maxOrder():
            return numpy.zeros([ 0, 0 ])
        
        # form a canonical ordering for the simplics of order k and k - 1
        ks = self._orderSortedSimplices(self.simplicesOfOrder(k))
        kmos = self._orderSortedSimplices(self.simplicesOfOrder(k - 1))

        # create a zero boundary matrix
        boundary = numpy.zeros([ n[k - 1], n[k] ])

        # add 1 in every row which is a face of the column' simplex
        c = 0
        for s in ks:
            # extract the faces of the simplex
            for f in self.faces(s):
                # mark the corresponding position with a 1
                r = kmos.index(f)
                boundary[r, c] = 1
            c = c + 1

        return boundary

    def disjoint( self, ss ):
        '''Test whether the elements of a set of simplices are disjoint,
        defined as if they share no common simplices in their closures.
        (This doesn't mean that they aren't part of a common super-simplex,
        however.) The simplices need not be of the same order, i.e., need
        not form a p-chain.

        :param ss: the p-chain
        :returns: boolean'''
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
        '''Reduce a boundary matrix to Smith Normal Form, which has a leading diagonal
        of 1s for some number of rows, and is everywhere else zero.

        :param b: the boundary matrix to reduce
        :returns: the Smith Normal Form of the boundary matrix'''
        return self._reduce(B, 0)
    
    def _reduce( self, Bin, x = 0 ):
        '''Reduce a boundary matrix to Smith Normal Form.
        The algorithm is taken from `here <https://www.cs.duke.edu/courses/fall06/cps296.1/Lectures/sec-IV-3.pdf>`_. NOte that this is simpler than other algorithms in the literature because
        we're working over a binary field.

        :param b: the boundary matrix to reduce
        :param x: the row/column being reduced, initially 0
        :returns: the Smith Normal Form of the boundary matrix'''

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
        '''Return a dict of Betti numbers for the different dimensions
        of the complex.

        :param ks: (optional) dimensions to compute (defaults to all)
        :returns: a dict of Betti numbers'''
        
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


    # ---------- Derived copmplexes ----------

    def _isClosed( self, boundary, fs ):
        '''Determine whether the given set of (k + 1) faces forms the
        boundary of a k-simplex according to the boundary operator.
        The faces are given by indices into the boundary matrix. They
        are closed if, when we sum the columns corresponding to them,
        the result consists of values that are either 2 or 0, i.e., if
        every face connects either 0 or 2 simplices.

        :param boundary: the boundary matrix
        :param fs: list of face indices
        :returns: True if the faces form a closed k-simplex'''

        # extract and sum columns
        s = numpy.sum(boundary[:, fs], axis = 1)
        
        # check we only have 2 or 0 in all positions
        return numpy.all(numpy.logical_or(s == 2, s == 0))
        
    def flagComplex( self ):
        '''Generate the :term:`flag complex` of this complex. The flag complex
        is formed by creating all the "implied" simplices for which all
        faces are present. For example, three 1-simplices forming an
        (empty) triangle will be "closed" by creating a 2-simplex
        with them as its faces. This may in turn allow a further
        3-simplex to be formed if the new 2-simplex closes a tetrahedron,
        and so forth.

        :returns: the flag complex'''

        # start with a copy of ourselves
        flag = copy.copy(self)

        # work up the simplex orders
        k = 1           # we use 1-simplices as adjacencies
        added = 1
        while added > 0:
            k = k + 1
            added = 0

            # compute the boundary operator
            boundary = self.boundaryMatrix(k - 1)

            # test all (k + 1) (k - 1)-simplices to see if they form
            # a boundary
            ks = numpy.array(self._orderSortedSimplices(self.simplicesOfOrder(k - 1)))
            for fs in [ list(fs) for fs in itertools.combinations(range(len(ks)), k + 1) ]:
                if self._isClosed(boundary, fs):
                    # simplices form a boundary, add to the
                    # flag complex (if it doesn't already exist)
                    cfs = ks[fs]
                    if flag.simplexWithFaces(cfs) is None:
                        flag.addSimplex(fs = cfs)
                        added = added + 1

        return flag
