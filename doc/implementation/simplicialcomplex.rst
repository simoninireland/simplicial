.. currentmodule:: simplicial

Representing simplicial complexes
=================================

Simplicial complexes are like graphs, from a data structure perspective: they
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
matrices, for example) in pursuit of efficiency. Thee core operations also
perform a lot of sanity-checking to maintain the integrity of the complex
being manipulated.


The sub-class interface
-----------------------

The interface to :class:`SimplicialComplex` is quite large -- over forty methods --
which poses a challenge for sub-classing. However, most of these methods are either
variations syntactic sugar for other, more basic, methods, or are completely defined
in terms of other methods. One can therefore often create s sub-class by
sub-classing a much smaller number of methods. These will typically be:

* :meth:`SimplicialComplex.addSimplex` to perform basic addition of simplices

* :meth:`SimplicialComplex.deleteSimplex` to delete simplices

* :meth:`SimplicialComplex.simplices` to enumerate simplices

* :meth:`SimplicialComplex.simplicesOfOrder` to enumerate simplices of a given order

* :meth:`SimplicialComplex.numberOfSimplices` to get the scale of the complex

* :meth:`SimplicialComplex.numberOfSimplicesOfOrder` to get the scale of the
  complex at a given order

* :meth:`SimplicialComplex.containsSimplex` to test for membership

And possibly also:

* :meth:`SimplicialComplex.copy` to create a deep copy of a complex

* :meth:`SimplicialComplex.maxOrder` to get the maximum order

* :meth:`SimplicialComplex.isSubComplexOf` to test for inclusion

* :meth:`SimplicialComplex.boundaryOperator` for constructing boundary matrices

As a general rule, all the operators (<, ==, len, in, ...) are defined in terms
of a "proper" function which can be overridden. So :meth:`SimplicialComplex._len__`
is a synonym for :meth:`SimplicialComplex.numberOfSimplices`, and so on.
Similarly :meth:`SimplicialComplex._le__` is defined in terms of
:meth:`SimplicialComplex.isSubComplexOf`. while the other operators like
:meth:`SimplicialComplex._gt__` and :meth:`SimplicialComplex._eq__` are defined
in terms of :meth:`SimplicialComplex._le__`.


