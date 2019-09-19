.. _glossary:

Glossary
========

.. currentmodule:: simplicial
		   
.. glossary::

   basis
      The 0-simplices that lie at the "base" of a :term:`simplex`. A
      simplex of :term:`order` k has (k + 1) 0-simplices in its basis.

   Betti numbers
      The count of the number of holes of a given dimension in a complex,
      computed using :term:`homology`. The 0th Betti number is the number
      of disconnected components in the complex; the 1st Betti number
      counts the number of unfilled loops of edges; the 2nd the number
      of unfilled voids; and so on.

   boundary
      The set of faces of a :term:`simplex`.
      
   boundary operator
      A linear operator taking *k*-simplices to the their *(k - 1)*-simplex
      faces. The boundary operator extends this to a set (or :term:`p-chain`)
      of *k*-simplices, where it returns all the *(k - 1)*-simplices
      in the total boundary.

   closure
      The closure of a simplex is the set consisting of the simplex
      and all its component faces, their faces, and so on to its
      :term:`basis`.
	    
   complex
      A collection of simplices. In ``simplicial``, complexes are
      *closed*, in the sense that they contain every :term:`face` of
      every :term:`simplex` contained in the complex.

   embedding
      A geometry imposed on a topological space. Typically an
      embedding locates each 0-simplex at some point in a Euclidean
      space, and maps 1- and 2-simplices to lines, surfaces, and so on
      for higher dimensions. In simplicial topology it is often
      assumed that only the 0-simplices are located, with the
      locations of higher simplices being constructed linearly from
      their bases -- so a 1-simplex is a straight line between its
      endpoints, and so forth.
      
   Euler characteristic
      A :term:`topological invariant` of a complex computed from the
      alternating sum of the numbers of simplices of different orders:

      .. math::
   
         \chi(S) = \sum_{k = 0}^{\infty} (-1)^k \, \#S_k.

      The Euler characteristic is a sort of hole detector for simplicial
      complexes, in that "un-filled" spaces are counted. For a stronger
      amnd more sophisticated (but more computationally demanding) hole
      detector, use :term:`homology`.
      
   face
      A :term:`simplex` that lies on the boundary of another
      simplex. By definition each face has is of :term:`order` one
      less than the simplex of which it is a face: 2-simplices
      (triangle) have faces that are 1-simplices (edges).

   flag complex
      A flag complex is a complex with all "implied" simplices
      present. That is to say, if all the *(k + 1)* faces of a *k*-simplex
      are present in the complex, then so is the  *k*-simplex itself.
      Another way to think of this is that all possible
      triangles of three edges are filled, as are all possible
      tetrahedra of four triangles, and so forth for higher orders.

      If we construct a graph of 0- and 1-simplices such that there is
      an edge between two vertices whenever they are within a distance
      *d* of each other, then in the derived flag complex each *k*-simplex
      represents *(k + 1)* vertices mutually within *d* of each
      other. High-dimensional simplices thus capture the "density" of
      vertices.
   
   homology
      A :term:`topological invariant` of a complex that has a
      subtle ability to measure holes of different dimensions in a
      structure.

   order
      The "dimensionality" of a :term:`simplex`, A simplex of order 1
      (a 1-simplex) is a one-dimensional structure (an edge); a
      simplex of order 2 is a two-dimensional structure (a triangle);
      and so on.

   p-chain
      In homology, a set of *p*-simplices. The :term:`boundary operator`
      is defined on p-chains.

   simplex
      A component of a :term:`complex`. A simplex has an
      :term:`order` that defines the number of 0-simplices in its
      :term:`basis`. 

   star
      The set of simplices of which a given :term:`simplex` is a part.
      The star is not necessarily a closed simplicial complex, but the
      star of the :term:`closure` (or indeed the :term:`closure` of the star)
      is (and they are generally different).
      
   topology
      "The stratosphere of human thought! In the twenty-fourth
      century it might possibly be of use to someone..." (Alexander
      Solzhenitsyn, The First Circle).

   topological invariant
      A property that isn't changed by smooth changes in a complex, or
      by the details of how a shape is approximated by a complex.
      
   Vietoris-Rips complex
      A complex derived from an underlying distance metric. If
      0-simplices are given locations, then for a given distance eps
      the Vietoris-Rips complex at scale *eps* has a *k*-simplex for every
      collection of *(k + 1)* 0-simplices lying mutually within a distance *eps*
      of each other.

      Another of saying this is that the Vietoris-Rips complex is the
      :term:`flag complex` resulting from a complex consisting of
      1-simplices between all pairs of 0-simplices lying within a distance
      eps of each other.
