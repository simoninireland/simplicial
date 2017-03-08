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

class SimplicialComplex(object):
    '''A finite simplicial complex.
    
    A simplicial complex is a generalisation of a network in which vertices (0-simplices)
    and edges (1-simplices) can be composed into triangles (2-simplices), tetrahedrons
    (3-simplices) and so forth. This classs actually implements closed simplicial
    complexes that contain every simplex, every face of that simplex, every face of
    those simplices, and so forth. Operations to add and remove simplices cascade to
    keep the complex closed.

    The class also includes some topological operations, notably for computing
    Euler characteristics of spaces and performing Euler integration.'''
    
    def __init__( self ):
        '''Create an empty complex.'''
        self._sequence = 1        # sequence number for generating simplex names
        self._simplices = dict()  # dict from simplex to faces
        self._attributes = dict() # dict from simplex to attributes 
        self._faces = dict()      # dict from simplex to simplices of which it is a face

    def _newUniqueIndex( self, d ):
        '''Generate a new unique identifier for a simplex. The default naming
        schemem uses a sequence number and a leading dimension indicator. Users
        can name simplices anything they want tyo get meaningful names. 
        
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
        
        :param id: (optional) identifier for the simplex 
        :param fs: (optional) a list of faces of the simplex
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex'''
        
        # fill in defaults
        if id is None:
            # no identifier, make one
            id = self._newUniqueIndex(len(fs) - 1)
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

        # return the simplices' name
        return id
    
    def addSimplicesFrom( self, c, rename = None ):
        '''Add simplices from the given complex. The rename parameter
        is is an optional mapping of the names in c that can be provided
        as a dict or a function.
        
        :param c: the other complex
        :param rename: (optional) renaming dict or function
        :returns: a list of simplex names'''

        # fill-out the defaults
        if rename is None:
            f = lambda s: s
        else:
            if isinstance(rename, dict):
                f = lambda s: rename[s]
            else:
                f = rename

        # perform the copy, renaming the nodes as they come in
        ns = []
        for s in c.simplices():
            id = self.addSimplex(id = f(s),
                                 fs = map(f, c.faces(s)),
                                 attr = c[s])
            ns.append(id)
        return ns
    
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
        '''Delete a simplex and all simplices of which it is a part. We have
        to do this to guarantee the closure of the simplicial complex. 
        
        :param s: the simplex'''
        ss = self.partOf(s)
        for t in ss:
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
        
        :returns: the largest order that contains at least one simplex'''
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

    def _orderCmp( self, s, t, reverse = False ):
        '''Comparison function for simplices based on their order.

        :param s: the first simplex
        :param t: the second simplex
        :returns: -1, 0, 1 for less than, equal, greater than (or reversed)'''
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
        '''Return a list of all simplices of the given order. This will
        be empty for any order not returned by :meth:`orders`.
        
        :param o: the desired order
        :returns: a list of simplices, which may be empty'''
        ss = []
        for s in self._simplices:
            if max(len(self.faces(s)) - 1, 0) == o:
                ss.append(s)
        return ss
    
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
        
    def allSimplices( self, p ):
        '''Return all the simplices that match the given predicate, which should
        be a function from complex and simplex to boolean.
        
        :param p: a predicate
        :returns: the set of simplices satisfying the predicate'''
        return [ s for s in self._simplices if p(self, s) ]
    
    def faces( self, s ):
        '''Return a list of the faces in a simplex.
        
        :param s: the simplex
        :returns: a list of faces'''
        return self._simplices[s]
    
    def faceOf( self, s ):
        '''Return the simplices that the given simplex is a face of. This
        is not transitive: all the simplices returned will be of an order
        one greater than the given simplex. The transitive closure of
        :meth:`faceOf` is :meth:`partOf`.
        
        :param s: the simplex
        :returns: a list of simplices'''''
        return self._faces[s]
    
    def partOf( self, s ):
        '''Return the transitive closure of all simplices of which the simplex
        is part: itself, a face of, or a face of a face of, and so forth. This is
        the dual of closureOf().
        
        :param s: the simplex
        :returns: a simplices the simplex is part of'''
        parts = set([ s ])
        fs = self._faces[s]
        for f in fs:
            parts = parts.union(set([ f ]))
            parts = parts.union(self.partOf(f))
        return parts
        
    def basisOf( self,  s ):
        '''Return the basis of a simplex, the set of 0-simplices that
        define its faces. The length of the basis is equal to one more
        than the order of the simplex.
        
        :param s: the simplex
        :returns: the simplices that form the basis of s'''
        cl = self.closureOf(s)
        bs = [ f for f in cl if self.order(f) == 0 ]  # sd: not the most elegant way to do this....
        return bs
    
    def closureOf( self, s ):
        '''Return the closure of a simplex. The closure is defined
        as the simplex plus all its faces, transitively down to its basis.
        
        :param s: the simplex
        :returns: the closure of the simplex'''
        fs = self.faces(s)
        if len(fs) == 0:
            # 0-simplex, return it
            return set([ s ])
        else:
            # k-simplex, return a list of it and its faces
            faces = set()
            for f in fs:
                faces = faces.union(self.closureOf(f))
            faces = faces.union(set([ s ]))
            return set(faces)
        
    def restrictBasisTo( self, ss ):
        '''Restrict the complex to include only those simplices whose 
        bases are wholly contained in the given set of 0-simplices.
        
        :param ss: the basis 0-simplices
        :returns: the complex'''

        # make sure we have a set of 0-simplices
        for s in ss:
            if self.order(s) > 0:
                # sd: should we simply expand this to the simplex' own basis?
                raise Exception('Higher-order simplex {s} in basis set'.format(s = s))
        
        # find all simplices that need to be excluded
        remove = set([])
        for s in self._simplices:
            if self.order(s) == 0:
                # it's a vertex, is it in the set?
                if s not in ss:
                    # no, mark it for dropping
                    remove.add(s)
            else:
                # it's a higher-order simplex, is its basis wholly in the set?
                bs = self.basisOf(s)
                for b in bs:
                    if not b in ss:
                        # non-element of set, mark it for removal
                        remove.add(s)
                        break
        
        # close the set of simplices to be removed
        for r in remove:
            rs = remove.union(self.partOf(r))
            
        # remove the marked simplices
        for s in self._orderSortedSimplices(remove, reverse = True):
            print "remove", s
            self._deleteSimplex(s)
            
    def eulerCharacteristic( self ):
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
        return a
