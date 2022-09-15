.. currentmodule:: simplicial

Representing simplicial complexes
=================================

Simplicial complexes are interesting from a data structure perspective: they
perfectly illustrate Marvin Minsky's dictum that "if you only have a single
representation of something, you have a poor one". The various operations
one might want to perform on a complex often require different views of
the complex in order to be efficient; creating one view from another,
while possible, can be unacceptably slow; while keeping multiple parallel
representations is both memory-hungry and a an invitation to inconsistency.


Internal representation
-----------------------

``simplicial`` chooses the last approach, despite its difficulties. The
complex maintains several data structures repesenting different aspects of
the complex:

* The maximum order or simplices

* A mapping of simplex identifiers to their order and index

* An array of arrays of simplex identifiers in canonical index order

* A list of boundary matrices

* A list of basis matrices for efficient extraction of bases

* A dict of simplex attributes

The core operations of :class:`SimplicialComplex` have to do more work to
maintain these parallel structures, and there is some repetition (one
can extract the basis of a simplex by repeatedly traversing the boundary
matrices, for example) in pursuit of efficiency. The core operations also
perform a lot of sanity-checking to maintain the integrity of the complex
being manipulated.


The sub-class interface
-----------------------

The interface to :class:`SimplicialComplex` is quite large -- over
forty methods -- which poses a challenge for sub-classing. However,
most of these methods are either variations or syntactic sugar for
other, more basic, methods, or are completely defined in terms of
other methods. One can therefore often create s sub-class by
sub-classing a much smaller number of methods.

There are two classes of methods to override. The first are the
methods that manage the default internal data structures of a complex:

* :meth:`SimplicialComplex.addSimplex` to perform basic addition of
  simplices

* :meth:`SimplicialComplex._deleteSimplex` (private method) to delete
  individual simplices

* :meth:`SimplicialComplex.relabelSimplex` to relabel individual
  simplices

* :meth:`SimplicialComplex.containsSimplex` to test for membership

* :meth:`SimplicialComplex.restrictBasisTo` to cull all simplices that
  have basis 0-simplices not in the given set

* :meth:`SimplicialComplex.simplices` to enumerate simplices

* :meth:`SimplicialComplex.maxOrder` to return the order of the
  largest simplex

* :meth:`SimplicialComplex.orderOf` to return the order of a simplex

* :meth:`SimplicialComplex.indexOf` to map a simplex to its index in
  the appropriate boundary operator

* :meth:`SimplicialComplex.simplicesOfOrder` to enumerate simplices of a given order

* :meth:`SimplicialComplex.simplexWithBasis` to find a simplex with
  the given basis

* :meth:`SimplicialComplex.basisOf` to find the basis of a simplex

* :meth:`SimplicialComplex.numberOfSimplices` to get the scale of the complex

* :meth:`SimplicialComplex.numberOfSimplicesOfOrder` to get the scale of the
  complex at a given order

* :meth:`SimplicialComplex.copy` to create a deep copy of a complex

* :meth:`SimplicialComplex.isSubComplexOf` to test for inclusion

* :meth:`SimplicialComplex.boundaryOperator` for constructing boundary matrices

* :meth:`SimplicialComplex.getAttribujtes` and
  :meth:`SimplicialComplex.setAttribujtes` to get and set the attributes
  dict of a simplex

* :meth:`SimplicialComplex.boundaryOperator` for constructing boundary matrices

* :meth:`SimplicialComplex.faces` and
  :meth:`SimplicialComplex,cofaces` to navigate up and down the face
  structure

* :meth:`SimplicialComplex.smithNormalForm` to extract the Smith
  normal form of the boundary operator at a given order

* :meth:`SimplicialComplex.Z` to extract the basis of the homology
  groups at the various orders
