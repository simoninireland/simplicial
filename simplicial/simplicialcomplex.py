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

import copy
import itertools


class SimplicialComplex(object):
    '''A finite simplicial complex.
    
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
    performing Euler integration.

    '''
    
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
    
    def addSimplex( self, fs = [], id = None, attr = None ):
        '''Add a simplex to the complex whose faces are the elements of fs.
        If no faces are given then the simplex is a 0-simplex (point).
        If no id is provided one is created. If present, attr should be a
        dict of attributes for the simplex.

        To add a simplex from its basis (rather than its faces) use
        :meth:`addSimplexByBasis`.
        
        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) name for the simplex 
        :param attr: (optional) dict of attributes
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
            of = self.order(f)
            if of != os - 1:
                raise Exception('Face {id} is of order {of}, not {os}'.format(id = f,
                                                                              of = of,
                                                                              os = os - 1))
                
        # add simplex and its attributes
        self._simplices[id] = ofs 
        self._attributes[id] = attr
        self._faces[id] = []
        
        # record the faces
        for f in ofs:
            self._faces[f].append(id)

        # return the simplex' name
        return id

    def addSimplexWithBasis( self, bs, id = None, attr = None ):
        '''Add a simplex by providing its basis, which uniquely defines it.
        This method adds all the simplices necessary to define the new
        simplex, using :meth:`simplexByBasis` to find and re-use any that are
        already in the complex.

        To add a simplex defined by its faces, use :meth:`addSimplex`.

        If the simplex with the given basis already exists in the complex,
        this method does nothing.

        Defining a k-simplex requires a (k + 1) basis. All elements of
        the basis must be 0-simplices.

        :param bs: the basis
        :param id: (optional) the name of the new simplex
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex'''
        so = len(bs) - 1   # order of the final simplex
        fs = []            # faces in the final simplex

        # make sure the list is a basis
        for b in bs:
            if b in self._simplices.keys():
                # simplex exists, check it's an 0-simplex
                if self.order(b) > 0:
                    raise Exception('Higher-order simplex {s} in basis set'.format(s = b))
                else:
                    s = b
            else:
                # simplex doesn't exist, create it
                s = self.addSimplex(id = b)

            # capture the simplex as a face if we're building a 1-simplex
            if so == 1:
                fs.append(s)

        # check if we have a simplex with this basis
        s = self.simplexWithBasis(bs)
        if s is not None:
            # we have, did we also get a name?
            if id is not None:
                # we did, so they have to match
                if s != id:
                    raise Exception('Simplex {s} with given basis already exists'.format(s = s))

            # return this simplex
            return s
                    
        # create a name for the new simplex if needed
        if id is None:
            id = self._newUniqueIndex(so)

        # if for some reason we're adding just an 0-simplex,
        # we're now finished
        if so == 0:
            return s

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
            if id is None:
                return self.addSimplex()
            else:
                return self.addSimplexWithBasis([ id ])
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
            if s != t and t in self._simplices.keys():
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

    def order( self, s ):
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
            os = [ self.order(s) for s in self._simplices ]
            return max(os)
    
    def numberOfSimplicesOfOrder( self ):
        '''Return a dict mapping an order to the number of simplices
        of that order in the complex.
        
        :returns: a dict mapping order to number of simplices'''
        orders = dict()
        for s in self._simplices:
            o = self.order(s)
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
        return cmp(self.order(s), self.order(t))

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
            if self.order(s) > 0:
                raise Exception('Higher-order simplex {s} in basis set'.format(s = s))

        # check for a simplex with the given basis
        so = len(bs) - 1
        ss = None
        for s in bs:
            ps = set([ p for p in self.partOf(s) if self.order(p) == so ])
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
        
    def __delitem__( self, s ):
        '''Delete the simplex and all simplices of which it is a part.
        Equivalent to :meth:`deleteSimplex`.
        
        :param s: the simplex'''
        self.deleteSimplex(s)
        
    def allSimplices( self, p, reverse = False ):
        '''Return all the simplices that match the given predicate, which should
        be a function from complex and simplex to boolean. The simplices are
        sorted according to their orders.
        
        :param p: a predicate
        :param reverse: (optional) reverse the order 
        :returns: the set of simplices satisfying the predicate'''
        return self._orderSortedSimplices([ s for s in self._simplices if p(self, s) ], reverse)
    
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
        return set([ f for f in self.closureOf(s) if self.order(f) == 0 ])  
    
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

    def restrictBasisTo( self, bs ):
        '''Restrict the complex to include only those simplices whose 
        bases are wholly contained in the given set of 0-simplices.
        
        :param bs: the basis
        :returns: the complex'''
        bs = set(bs)
        
        # make sure we have a set of 0-simplices
        for s in bs:
            if self.order(s) > 0:
                raise Exception('Higher-order simplex {s} in basis set'.format(s = s))
        
        # find all simplices that need to be excluded
        remove = set([])
        for s in self._simplices:
            if self.order(s) == 0:
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

    def disjoint( self, ss ):
        '''Test whether a set of simplices are disjoint, defined as if
        they share no common simplices in their closures. (It doesn't
        mean that they aren't part of a common super-simplex, however.)

        :param ss: the simplices
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
        a = 0
        for s in xrange(self.maxOrder() + 1):
            # form the level set
            # sd TODO: the level set is uniformly growing as s decreases, so we can optimise?
            cprime = copy.deepcopy(self)
            bs = cprime.allSimplices(lambda c, sp: self.order(sp) == 0 and
                                                   self[sp][observation_key] > s)
            cprime.restrictBasisTo(bs)
            
            # compute the Euler characteristic of the level set
            chi = cprime.eulerCharacteristic()
            #print 'level {level}, chi = {chi}'.format(level = s, chi = chi)
            
            # add to the integral
            a = a + chi

        # return the accumulated integral
        return a

    
                
                
