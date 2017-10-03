.. _glossary:

Glossary
========

.. currentmodule:: simplicial
		   
.. glossary::

   basis
      The 0-simplices that lie at the "base" of a :term:`simplex`. A
      simplex of :term:`order` n has n 0-simplices in its basis.

   boundary operator
      A linear operator taking k-simplices to the their (k-1)-simplex
      faces. The boundary operator extends to sets (chains) of k-simplices,
      where it returns all the (k-1)-simplices in the total boundary.

   closure
      The closure of a simplex is the set consisting of the simplex
      and all its component faces, their faces, and so on to its
      :term:`basis`.
	    
   complex
      A collection of simplices. In `simplicial`, complexes are
      closed, in the sense that they contain every :term:`face` of
      every :term:`simplex` contained in the complex.

   Euler characteristic
      A :term:`topological invariant` of a complex computed from the
      alternating sum of the numbers of simplices of different orders:

      .. math::
   
         \chi(S) = \sum_{k = 0}^{\infty} (-1)^k \, \#S_k.

      The Euler characteristic is a hole detector for simplicial
      complexes, in that "un-filled" spaces are counted.
      
   face
      A :term:`simplex` that lies on the boundary of another
      simplex. By definition each face has is of :term:`order` one
      less than the simplex of which it is a face: 2-simplices
      (triangle) have faces that are 1-simplices (edges).

   homology
      A :term:`topological invariant` of a complex that has a
      subtle ability to measure holes of different dimensions in a
      structure.
      
   order
      The "dimensionality" of a :term:`simplex`, A simplex of order 1
      (a 1-simplex) is a one-dimensional structure (an edge); a
      simplex of order 2 is a two-dimensional structure (a triangle);
      and so on.
   
   simplex
      A component of a :term:`complex`. A simplex has an
      :term:`order` that defines the number of 0-simplices in its
      :term:`basis`. 

   star
      The set of simplices of which a given :term:`simplex` is a part.
      The star is not necessarily a closed simplicial complex, but the
      star of the :term:`closure` of a simplex is.
      
   topology
      "The stratosphere of human thought! In the twenty-fourth
      century it might possibly be of use to someone..." (Alexander
      Solzhenitsyn, The First Circle).

   topological invariant
      A property that isn't changed by smooth changes in a complex, or
      by the details of how a shape is approximated by a complex.
      
