.. _reference-implementation:

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


Interface/representation split
------------------------------

While representing a complex is quite tricky, only a small number of
operations are needed to do so. We can therefore split the
responsibilities between two sets of methods:

- those that access and manipulate the representation of the complex;
  and
- those that can work through this interface.

We therefore split the functions across two classes.
:class:`SimplicialComplex` provides all the main access methods for a
complex, but delegates the sub-set of operations that manipulate the
representation of a complex to a representation class.
Representations all inherit from :class:`Representation`, which
defines the interface and does some simple housekeeping.

The reference implementation,
:class:`ReferenceRepresentation`, uses the approach of
replicating information, despite its difficulties. This makes the
representation code harder, but the client code easier to understand
and often faster. The representation maintains several data structures
representing different aspects of the complex:

* The maximum order or simplices
* A mapping of simplex identifiers to their order and index
* An array of arrays of simplex identifiers in canonical index order
* A list of boundary matrices
* A list of basis matrices for efficient extraction of bases
* A dict of simplex attributes

The core operations of :class:`ReferenceRepresentation` have
to do more work to maintain these parallel structures, and there is
some repetition (one can extract the basis of a simplex by repeatedly
traversing the boundary matrices, for example) in pursuit of
efficiency. The core operations also perform a lot of sanity-checking
to maintain the integrity of the complex being manipulated.


The representation interface
----------------------------

To define a new representation we need only provide definitions for
the methods in the representation interface. One can do this by
sub-classing the reference implementation or (since this is Python) by
writing any class that supports the same interface.

*Addition and removal of simplices*:

- :meth:`Representation.addSimplex` to perform basic addition of
  simplices
- :meth:`Representation.forceDeleteSimplex` to delete
  individual simplices regardless of consequences
- :meth:`Representation.relabelSimplex` to relabel individual
  simplices

*Retrieving simplices*:

- :meth:`Representation.simplices` to enumerate simplices
- :meth:`Representation.simplicesOfOrder` to enumerate
  simplices of a given order
- :meth:`Representation.containsSimplex` to test for membership
- :meth:`Representation.maxOrder` to return the order of the
  largest simplex

*Accessing details of an individual simplex*:

- :meth:`Representation.orderOf` to return the order of a simplex
- :meth:`Representation.indexOf` to map a simplex to its index in
  the appropriate boundary operator
- :meth:`Representation.getAttribujtes` and
  :meth:`Representation.setAttributes` to get and set the attributes
  dict of a simplex
- :meth:`Representation.faces` to find the faces of a simplex
- :meth:`Representation.cofaces` to find the cofaces of a simplex
- :meth:`Representation.basisOf` to find the basis of a simplex

*Topological information*:

- :meth:`Representation.boundaryOperator` to compute the
  boundary operator matrix for a given order of simplices

This is still quite a surface area, but significantly less than the
overall surface area of complexes in general, and notably excludes
many quite complex operations such as those concerning :ref:`computing
homology <homology>`
