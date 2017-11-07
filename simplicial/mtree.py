class MTree(object):
    '''A data structure for approximate search.

    An M-tree is an associative striucture that uses points in space
    as keys for values. The structure can be queried by providing a
    point in the space and looking for the nearest neighbouring
    points, or looking for all points within a given range. The
    dimensions of the key space, the co-ordinates of each dimension,
    and the notion ot distance used are all abstracted. The tree is
    self-balancing, creating intermediate "routing" nodes to structure
    the real data points and reduce the amount of search needed.

    :param dim: dimension of the key space (defaults to 2)
    :param levelSize: optional tuning parameter for the sizes of routing nodes

    '''

    DEFAULT_LEVEL_SIZE = 2     #: Default size of a routing node

    
    def __init__( self, dim = 2, levelSize = None ):
        self._dimension = dim
        self._root = MTreeNode(None, self._origin())
        if levelSize is None:
            levelSize = self.DEFAULT_LEVEL_SIZE
        self._levelsize = levelSize
        

    # ----- Distance -----

    def distance(self, p, q ):
        '''Compute the distance between two key points. This method
        may be overridden by sub-classes. The default assumes that the
        key space is Euclidian, keyed by numbers, and computes the
        regular straight-line distance between the points.

        :param p: one point
        :param q: the other point
        :returns: the distane between them'''
        sumsq = 0
        for d in range(self.dimension()):
            sumsq = numpy.square(q[d] - p[d])
        return numpy.sqrt(sumsq)


    # ----- Insertion and deletion -----

    def insert( self, o, v ):
        '''Insert value v at a point o.

        :param o: the key point in the key space
        :param v: the value'''
        return self._insert(self._root, o, v)

    def _insert(self, n, o, v ):
        if not n.isLeaf():
            # n is a routing node, compute all children whose distance
            # to o is less than n's radius
            nin = [ r for r in n.children() if self.distance(r, o) < n.radius() ]
            if len(nin) > 0:
                # find the closest of these children to o
                ds = [ (r, self.distance(r, o)) for r in nin.children() ]
                sds = sorted(ds, key = (lambda (a, b): b))
                (rmin, dmin) = sds[0]
            else:
                # no such child, find the child whose radius will expand
                # the least if we add o as its child
                ds = [ (r, self.distance(r, o) - r.radius()) for r in n.children() ]
                sds = sorted(ds, key = (lambda (a, b): b))
                (rmin, dmin) = sds[0]

            # recursively insert into chosen branch
            return self._insert(rmin, o, v)
            
        else:
            # n is a leaf
            if n.size() < self._levelSize:
                # child is not full, add the new node
                n.addChild(MTreeeNode(v, o))
            else:
                self._split(n, v, o)

    def _split(self, n, v, o ):
        if not n.isRoot():
            # splitting a non-root node
            p = n.parent()
            

    # ----- Queries -----

    def range( self, q, rq ):
        '''Return all values lying within a given range of the search point.

        :param q: the search point
        :param rq: the range
        :returns: a list of (point, value) pairs, in order of increasing range'''
        return self._rs(self._root, q, rq )

    def _rs( self, n, q, rq ):
        rs = []
        p = n.parent()
        if not n.isLeaf():
            for r in n.children():
                if self.distance(p, q) - self.distance(r, p) <= rq + r.distanceToParent():
                    dr = self.distance(r, q)
                    if dr <= rq + r.radius():
                        rs.append(self._rs(r.children(), q, rq))
        else:
            for j in n.children():
                if self.distance(p, q) - self.distance(j, p) < rq:
                    dj = self.distance(j, q)
                    if dj <= rq:
                        rs.append(j.value())
                        
        return rs

    
    # ----- Dict-like interface-----

    def __getitem__( self, o ):
        '''Return the value closest to the given key point. This is equivalent
        to a nearest-neighbour query :meth:`MTree.nearestNeighbour` with k = 1.

        :param o: the search point
        :returns: the nesrest value to the search point'''
        return self.nearestNeighbours(o, 1)
    
    def __setitem__( self, o, v ):
        '''Insert the given value at the given key point. This is equivalent
        to :meth:`MTree.insert`.

        :param o: the key point
        :param v: the value'''
        return self.insert(o, v)
    

class MTreeNode(object):
    '''Internal structrue for representing MTree nodes. Never exposed to clients.'''
    
    def __init__( self, v, pos ):
        self._value = v
        self._position = pos
        self._children = []
        self._radius = 0.0
        self._parent = None
        self._distance = 0.0


    # ----- Access -----

    def value( self ):
        return self._value
    
    def parent( self ):
        return self._parent
    
    def children( self ):
        return self._children

    def radius( self ):
        return self._radius

    def isLeaf( self ):
        return len(self.children()) == 0

    def size( self ):
        return len(self.children())

    def isRoot( self ):
        return (self.parent() is None)
    

    # ----- Adding and removing children -----

    def addChild( self, mn ):
        self._children.append(mn)
        mn._parent = self
        
