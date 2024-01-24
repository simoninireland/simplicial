# Graphs as simplicial complexes
#
# Copyright (C) 2017--2024 Simon Dobson
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
from itertools import chain
from typing import List, Set, Tuple, Iterator
from simplicial import Simplex, Attributes, Representation, Isomorphism
from networkx import Graph


class GraphRepresentation(Representation):
    '''A graph as a simplicial complex.

    The representation uses a `networkx` graph to store as much data
    as possible, and this can be accessed to make use of the
    `networkx` operations This is significantly more efficient than
    :class:`ReferenceRepresentation` for a complex that doesn't have
    higher simplices, just nodes and edges.

    Any graph provided to construct the representation is copied by
    default. This would be expensive for large graphs, so there is an
    option to use the graph object as-is. However, it is important
    than any changes to the graph are made through the complex, *not*
    directly on the graph: changing the graph directly will break things.

    :param g: (optional) the graph (defaults to an empty graph)
    :param copy: (optional) copy the provided graph (defaults to True)

    '''


    # ---------- Initialisation ----------

    def __init__(self, g: Graph = None, copy: bool = True):
        super().__init__()
        self._sequence = 0
        self._edges = Isomorphism[Simplex, Tuple[Simplex, Simplex]]()
        self._edgeOrder: List[Simplex] = []

        # create, copy, or use any provided graph
        if g is None:
            self._graph = Graph()
        else:
            # get the graph
            if copy:
                self._graph = g.copy()
            else:
                self._graph = g

            # grab its structure
            for (l, r) in self._graph.edges:
                id = self.newSimplex([l, r])
                self._edges[id] = (l, r)
                self._edgeOrder.append(id)


    # ---------- Core interface ----------

    def newSimplex(self, fs: List[Simplex]) -> str:
        """Generate a new unique identifier for a simplex with the
        given faces.

        :param fs: the faces
        :returns: an identifier not currently used in the complex

        """
        i = self._sequence
        k = len(fs) if fs is not None and len(fs) > 0 else 0
        while True:
            id = f'{k}d{i}'
            if k == 0:
                # nodes: check the networkx node labels
                if not self._graph.has_node(id):
                    self._sequence = i + 1
                    return id
                else:
                    i += 1
            else:
                # edges: check the edge names
                if id not in self._edges.keys():
                    self._sequence = i + 1
                    return id
                else:
                    i += 1


    def addSimplex(self, fs: List[Simplex] = None, id: Simplex = None, attr: Attributes = None) -> Simplex:
        '''Add a simplex to the complex with the given faces. If there
        are no faces, a node is added; if there are two faces, an edge is added;
        if there are any more, an exception is raised.

        :param fs: (optional) a list of faces of the simplex
        :param id: (optional) explicit name for the simplex
        :param attr: (optional) dict of attributes
        :returns: the name of the new simplex
        '''

        # check dimensions
        if fs is None:
            # no faces, create an 0-simplex
            k  = 0
        else:
            # check dimensions are allowed
            k = max(len(fs) - 1, 0)
            if k > 1:
                raise ValueError("GraphRepresentation only allows nodes and edges")

        # fill in defaults
        if id is None:
            # no explicit identifier, make a unique one
            id = self.newSimplex(fs)
        else:
            # check we've got a new id -- can only get duplicates for
            # explicitly-given ids
            if k == 0:
                if self._graph.has_node(id):
                    raise KeyError(f'Duplicate node {id}')
            elif k == 1:
                if id in self._edges.keys():
                    raise KeyError(f'Duplicate edge {id}')
        if attr is None:
            # no attributes, use an empty dict
            attr = dict()

        # make sure all the faces are distinct and of the right order
        if k > 0:
            self.checkAllSimplicesAreUnique(fs)
            self.checkAllSimplicesHaveOrder(fs, k - 1)

        # add the simplex
        if k == 0:
            # add a new node
            self._graph.add_node(id, **attr)
        else:
            # add an edge
            self._graph.add_edge(fs[0], fs[1], **attr)
            self._edges[id] = (fs[0], fs[1])
            self._edgeOrder.append(id)

        # return the simplex' name
        return id


    def relabelSimplex(self, s: Simplex, q: Simplex):
        '''Relabel a simplex.

        :param s: the simplex
        :param q: the new name
        '''
        pass


    def forceDeleteSimplex(self, s: Simplex):
        '''Delete a simplex without sanity checking.

        :param s: the simplex'''
        k = self.orderOf(s)
        if k == 0:
            # delete a node
            self._graph.remove_node(s)
        else:
            # delete an edge
            (l, r) = self._edges[s]
            self._graph.remove_edge(l, r)
            del self._edges[s]
            del self._edgeOrder[self._edgeOrder.index(s)]


    def orderOf(self, s: Simplex) -> int:
        '''Return the order of the simplex, which will be either 0 or
        1.

        :param s: the simplex
        :returns: the simplex' order

        '''

        # nodes can be checked directly
        if self._graph.has_node(s):
            return 0

        # check edges
        if s in self._edges.keys():
            return 1

        # otherwise there's no such simplex
        raise KeyError(f'No simplex {s} in complex')


    def indexOf(self, s: Simplex) -> int:
        '''Return the index of the simplex.

        At present this operation is linear in the number of
        simplices: it should probably be optimised./

        :param s: the simplex
        :returns: its index within its order

        '''
        k= self.orderOf(s)
        if k == 0:
            return list(self._graph,nodes).indexOf(s)
        else:
            return self._edgeOrder.indexOf(s)


    def basisOf(self, s: Simplex) -> Set[Simplex]:
        '''Return the basis of a simplex.

        :param s: the simplex
        :returns: a set of simplices'''
        k = self.orderOf(s)
        if k == 0:
            return set([s])
        else:
            (l, r) = self._edges[s]
            return set([l, r])


    def maxOrder(self) -> int:
        '''The maximum order of an empty graph is -1 (by convention);
        of a graph with no edges is 0; and otherwise 1.

        :returns: the maximum order
        '''
        if self._graph.order() == 0:
            return -1
        elif len(self._graph.edges) == 0:
            return 0
        else:
            return 1


    def simplices(self, reverse = False) -> Iterator[Simplex]:
        '''Return all the simplices in the complex, in order: the
        low orders first (unless reverse is True), and in canonical
        order within each order.

        :param reverse: (optional) reverse the sort order if True
        :returns: a list of simplices'''
        if reverse:
            return chain.from_iterable([self.simplicesOfOrder(1), self.simplicesOfOrder(0)])
        else:
            return chain.from_iterable([self.simplicesOfOrder(0), self.simplicesOfOrder(1)])


    def simplicesOfOrder(self, k: int) -> Iterator[Simplex]:
        '''Return all the simplices of the given order. All orders
        greater than 1 are empty, but asking for them doesn't cause an
        exception. The simplices are returned in "canonical" order,
        meaning the order they appear in the boiundary operator
        matrices.

        :param k: the desired order
        :returns: a set of simplices, which may be empty

        '''
        if k == 0:
            # return the nodes in networkx order
            return iter(self._graph.nodes)
        elif k == 1:
            # return in the order we maintain
            return iter(self._edgeOrder)
        else:
            return iter([])


    def containsSimplex(self, s: Simplex) -> bool:
        '''Test whether the complex contains the given simplex.

        :param s: the simplex
        :returns: True if the simplex is in the complex'''
        return self._graph.has_node(s) or s in self._edges.keys()


    def getAttributes(self, s: Simplex) -> Attributes:
        """Return the attributes associated with the given simplex.

        :param s: the simplex
        :returns: a dict of attributes"""
        k = self.orderOf(s)
        if k == 0:
            return self._graph.nodes[s]
        else:
            (l, r) = self._edges[s]
            return self._graph.edges[l, r]


    def setAttributes(self, s: Simplex, attr: Attributes):
        '''Set the attributes associated with a simplex.

        :param s: the simplex
        :param attr: a dict of attributes'''
        k = self.orderOf(s)
        if k == 0:
            e = self._graph.nodes[s]
        else:
            (l, r) = self._edges[s]
            e = self._graph.edges[l, r]

        # add new attributes
        ks = list(attr.keys())
        oks = list(e.keys())
        for k in ks:
            e[k] = attr[k]

        # delete any attributes not in the new set
        for k in oks:
            if k not in ks:
                del e[k]


    def faces(self, s: Simplex) -> Set[Simplex]:
        '''Return the faces of a simplex.

        :param s: the simplex
        :returns: a set of faces'''
        k = self.orderOf(s)
        if k == 0:
            # nodes don;t have faces
            return set()
        else:
            # the faces of an edge are the same as its basis
            (l, r) = self._edges[s]
            return set([l, r])


    def cofaces(self, s: Simplex) -> Set[Simplex]:
        '''Return the simplices the given simnplex is a face of.

        :param s: the simplex
        :returns: a list of simplices'''
        k = self.orderOf(s)
        if k == 0:
            # the cofaces are all edges this node is incident on
            # (this isn't an efficient way to do this)
            es = [e for (e, (l, r)) in self._edges.items() if l == s or r == s]
            return set(es)
        else:
            # edges don't have any cofaces
            return set()


    def boundaryOperator(self, k: int) -> numpy.ndarray:
        '''Return the boundary operator of the k-simplices.

        :param k: the order of simplices
        :returns: the boundary matrix

        '''
        if k == 0:
            # return a row of zeros
            return numpy.zeros([1, self._graph.number_of_nodes()])
        elif k == 1:
            # construct the boundary matrix by enumeration
            b =  numpy.zeros([self._graph.number_of_edges(), self._graph.number_of_nodes()])
            nodes = list(self._graph.nodes)
            for e in self._edges.keys():
                (l, r) = self._edges[e]
                i = self._edgeOrder[e]
                b[i, self.nodes[l]] = 1
                b[i, self.nodes[r]] = 1
                return b
        else:
            # return a null boundary operator
            return numpy.zeros([0, 0])
