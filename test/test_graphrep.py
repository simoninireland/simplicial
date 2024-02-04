# Tests of simplicial complex graph representation
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

import unittest
import copy
import numpy
from simplicial import *
from networkx import Graph


class GraphRepTests(unittest.TestCase):

    def testEmptyGraph(self):
        '''Test an empty graph works as it should.'''
        rep = GraphRepresentation()

        # check we're order -1
        self.assertEqual(rep.maxOrder(), -1)

        # count the simplices
        self.assertEqual(len(list(rep.simplices())), 0)

        # count the simplices of actual orders
        self.assertEqual(len(list(rep.simplicesOfOrder(0))), 0)
        self.assertEqual(len(list(rep.simplicesOfOrder(1))), 0)

        # check no extraneous orders
        self.assertEqual(len(list(rep.simplicesOfOrder(2))), 0)


    def testSingletonGraph(self):
        '''Test a graph with a single node.'''
        rep = GraphRepresentation()
        rep.addSimplex()

        # check at the underlying graph level
        self.assertEqual(rep._graph.number_of_nodes(), 1)
        self.assertEqual(rep._graph.number_of_edges(), 0)

        # check at the representation level
        self.assertEqual(rep.maxOrder(), 0)
        self.assertEqual(len(list(rep.simplicesOfOrder(0))), 1)
        self.assertEqual(len(list(rep.simplicesOfOrder(1))), 0)
        self.assertEqual(len(list(rep.simplices())), 1)


    def testPairGraph(self):
        '''Test a graph with two nodes and one edge.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2])

        # check at the underlying graph level
        self.assertEqual(rep._graph.number_of_nodes(), 2)
        self.assertEqual(rep._graph.number_of_edges(), 1)

        # check at the representation level
        self.assertEqual(rep.maxOrder(), 1)
        self.assertEqual(len(list(rep.simplicesOfOrder(0))), 2)
        self.assertEqual(len(list(rep.simplicesOfOrder(1))), 1)
        self.assertEqual(len(list(rep.simplices())), 3)


    def testInitialGraphCopy(self):
        '''Test we can create a complex from a graph.'''
        g = Graph()
        g.add_nodes_from([1, 2, 3])
        g.add_edges_from([(1, 2), (2, 3), (3, 1)])
        g.nodes[1]['a'] = 12
        g.edges[2, 3]['b'] = 2

        # we do this test through a "proper" complex (using the
        # GraphRepresentation) so we can retrieve a simplex from its
        # basis, since the edges we added have synthetic (and
        # therefore unknown) simplex names

        # check the simplices
        c = SimplicialComplex(GraphRepresentation(g))
        self.assertCountEqual(c.simplicesOfOrder(0), [1, 2, 3])
        self.assertEqual(len(list(c.simplices())), 6)
        self.assertEqual(len(list(c.simplicesOfOrder(1))), 3)

        # check we copied attributes
        self.assertEqual(c.getAttributes(1)['a'], 12)
        e1 = c.simplexWithBasis([2, 3])
        self.assertEqual(c.getAttributes(e1)['b'], 2)

        # check the graph was ion fcact copied by adding a node and
        # making sure it doesn't turn up as an 0-simplex
        g.add_node(4)
        self.assertCountEqual(c.simplicesOfOrder(0), [1, 2, 3])


    def testAddHigherSimplex(self):
        '''Test we can't add higher simplices.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        n3 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2])
        e2 = rep.addSimplex(fs=[n2, n3])
        e3 = rep.addSimplex(fs=[n3, n1])

        with self.assertRaises(ValueError):
            rep.addSimplex(fs=[e1, e2, e3])


    def testNodeAttributes(self):
        '''Test we can store, retrieve, and update node attributes.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex(attr=dict(a=12, b=20))
        n2 = rep.addSimplex(attr=dict(a=1, b=2))

        # test access
        self.assertEqual(rep.getAttributes(n1)['a'], 12)
        self.assertEqual(rep.getAttributes(n1)['b'], 20)
        self.assertEqual(rep.getAttributes(n2)['a'], 1)
        self.assertEqual(rep.getAttributes(n2)['b'], 2)

        # test update
        rep.setAttributes(n1, dict(a=100, c=200))
        self.assertEqual(rep.getAttributes(n1)['a'], 100)
        self.assertEqual(rep.getAttributes(n1)['c'], 200)
        self.assertCountEqual(rep.getAttributes(n1).keys(), ['a', 'c'])

        # attributes of other node were unchanged
        self.assertEqual(rep.getAttributes(n2)['a'], 1)
        self.assertEqual(rep.getAttributes(n2)['b'], 2)


    def testEdgeAttributes(self):
        '''Test we can store, retrieve, and update edge attributes.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        n3 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2], attr=dict(a=12, b=20))
        e2 = rep.addSimplex(fs=[n2, n3], attr=dict(a=1, b=2))

        # test access
        self.assertEqual(rep.getAttributes(e1)['a'], 12)
        self.assertEqual(rep.getAttributes(e1)['b'], 20)
        self.assertEqual(rep.getAttributes(e2)['a'], 1)
        self.assertEqual(rep.getAttributes(e2)['b'], 2)

        # test update
        rep.setAttributes(e1, dict(a=100, c=200))
        self.assertEqual(rep.getAttributes(e1)['a'], 100)
        self.assertEqual(rep.getAttributes(e1)['c'], 200)
        self.assertCountEqual(rep.getAttributes(e1).keys(), ['a', 'c'])

        # attributes of other node were unchanged
        self.assertEqual(rep.getAttributes(e2)['a'], 1)
        self.assertEqual(rep.getAttributes(e2)['b'], 2)


    def testContains(self):
        '''Test we can check for the presence of simplices (positive and negative).'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2])

        self.assertTrue(rep.containsSimplex(n1))
        self.assertTrue(rep.containsSimplex(n2))
        self.assertTrue(rep.containsSimplex(e1))
        self.assertFalse(rep.containsSimplex(1234))


    def testOrder(self):
        '''Test the orders of simplices.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2])

        self.assertEqual(rep.orderOf(n1), 0)
        self.assertEqual(rep.orderOf(n2), 0)
        self.assertEqual(rep.orderOf(e1), 1)


    def testBasisNode(self):
        '''Test extracting the basis of a node.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()

        self.assertCountEqual(rep.basisOf(n1), [n1])


    def testBasisEdge(self):
        '''Test extracting the basis of an edge.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2])

        self.assertCountEqual(rep.basisOf(e1), [n1, n2])


    def testDeleteNode(self):
        '''Test we can delete a node.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()

        rep.forceDeleteSimplex(n1)
        self.assertEqual(rep.maxOrder(), 0)
        self.assertCountEqual(rep.simplicesOfOrder(0), [n2])
        self.assertEqual(len(list(rep.simplicesOfOrder(1))), 0)


    def testDeleteEdge(self):
        '''Test we can delete an edge.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2])

        rep.forceDeleteSimplex(e1)
        self.assertEqual(rep.maxOrder(), 0)
        self.assertCountEqual(rep.simplicesOfOrder(0), [n1, n2])
        self.assertEqual(len(list(rep.simplicesOfOrder(1))), 0)


    def testDeleteNodeCascade(self):
        '''Test we can delete a node and the edges in its star.'''

        # we do this test through a "proper" complex (using the
        # GraphRepresentation) so that the deletion semantics are
        # followed properly

        c = SimplicialComplex(GraphRepresentation())
        n1 = c.addSimplex()
        n2 = c.addSimplex()
        n3 = c.addSimplex()
        e1 = c.addSimplex(fs=[n1, n2])
        e2 = c.addSimplex(fs=[n1, n3])

        c.deleteSimplex(n1)    # deletes the simplex and its star
        self.assertEqual(c.maxOrder(), 0)
        self.assertCountEqual(c.simplicesOfOrder(0), [n3, n2])
        self.assertEqual(len(list(c.simplicesOfOrder(1))), 0)


    def testBoundaryMatrix(self):
        '''Test we build the correct boundary matrices.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        n3 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2])
        e2 = rep.addSimplex(fs=[n1, n3])

        # boundaries of nodes should all be empty
        b0 = rep.boundaryOperator(0)
        self.assertEqual(b0.shape, (1, 3))
        self.assertTrue(not b0.any())

        # check boundaries of edges
        b1 = rep.boundaryOperator(1)
        self.assertEqual(b1.shape, (3, 2))
        in1 = rep.indexOf(n1)
        in2 = rep.indexOf(n2)
        in3 = rep.indexOf(n3)
        ie1 = rep.indexOf(e1)
        ie2 = rep.indexOf(e2)
        self.assertEqual(b1[in1, ie1], 1)
        self.assertEqual(b1[in1, ie2], 1)
        self.assertEqual(b1[in2, ie1], 1)
        self.assertEqual(b1[in2, ie2], 0)
        self.assertEqual(b1[in3, ie1], 0)
        self.assertEqual(b1[in3, ie2], 1)


    def testBoundaryChains(self):
        '''Test the boundary of a boundary is empty.'''
        rep = GraphRepresentation()
        n1 = rep.addSimplex()
        n2 = rep.addSimplex()
        n3 = rep.addSimplex()
        e1 = rep.addSimplex(fs=[n1, n2])
        e2 = rep.addSimplex(fs=[n1, n3])

        b0 = rep.boundaryOperator(0)
        b1 = rep.boundaryOperator(1)
        in1 = rep.indexOf(n1)
        in2 = rep.indexOf(n2)
        in3 = rep.indexOf(n3)
        ie1 = rep.indexOf(e1)
        ie2 = rep.indexOf(e2)

        # an edge (in matrix form)
        e = numpy.zeros([2, 1])
        e[ie1, 0] = 1

        # boundary of an edge
        b = b1 @ e
        self.assertEqual(b[in1, 0], 1)
        self.assertEqual(b[in2, 0], 1)
        self.assertEqual(b[in3, 0], 0)

        # boundary of boundary
        bb = b0 @ b1 @ e
        self.assertTrue(not bb.any())

        # boundary of the two edges (using modulo 2 homology)
        et = numpy.ones([2, 1])
        bt = (b1 @ et) % 2
        self.assertEqual(bt[in1, 0], 0)
        self.assertEqual(bt[in2, 0], 1)
        self.assertEqual(bt[in3, 0], 1)



    # def testCoboundaryMatrix(self):
    #     '''Test we build the correct coboundary matrices.'''

    #     # we do this test through a "proper" complex (using the
    #     # GraphRepresentation) to call the cobundaryMatrix() operator

    #     c = SimplicialComplex(GraphRepresentation())
    #     n1 = c.addSimplex()
    #     n2 = c.addSimplex()
    #     n3 = c.addSimplex()
    #     e1 = c.addSimplex(fs=[n1, n2])
    #     e2 = caddSimplex(fs=[n1, n3])

    #     # check coboundaries of nodes
    #     b1 = ccoboundaryOperator(1)
    #     self.assertEqual(b1.shape, (2, 3))
    #     in1 = cindexOf(n1)
    #     in2 = cindexOf(n2)
    #     in3 = cindexOf(n3)
    #     ie1 = cindexOf(e1)
    #     ie2 = cindexOf(e2)
    #     self.assertEqual(b1[in1, ie1], 1)
    #     self.assertEqual(b1[in1, ie2], 1)
    #     self.assertEqual(b1[in2, ie1], 1)
    #     self.assertEqual(b1[in2, ie2], 0)
    #     self.assertEqual(b1[in3, ie1], 0)
    #     self.assertEqual(b1[in3, ie2], 1)


if __name__ == '__main__':
    unittest.main()
