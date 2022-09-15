:class:`SimplicialComplex`: An abstract topological space
=========================================================

.. currentmodule:: simplicial

.. autoclass:: SimplicialComplex


Adding simplices
----------------

A :term:`simplex` is added to a complex by providing some or all of
the following information: a name for the simplex, a list of its
faces, and a dict of attributes.

.. automethod:: SimplicialComplex.addSimplex

Since a simplex is uniquely defined by its :term:`basis`, we can
simply provide the basis and let `simplicial` work out all the
other simplices that need to be added. This can be a major simplification
for higher-order simplices.

.. automethod:: SimplicialComplex.ensureBasis

.. automethod:: SimplicialComplex.addSimplexWithBasis

There are some operations that create new simplices from old.

.. automethod:: SimplicialComplex.barycentricSubdivide

Finally, it is also possible to copy simplices from one complex to
another. This will cause problems if the two complexes share simplices
with common names (since names must be unique), in which case  a
renaming mapping can be applied automatically during the copy process.

.. automethod:: SimplicialComplex.addSimplicesFrom


Deleting simplices
------------------

Since :class:`SimplicialComplex` represents closed simplicial
complexes -- in which all the faces of all the simplices in a complex
are also in the complex -- deletion requires that we cascade deletions
to delete all the simplices of which the to-be-deleted simplex is a part
(a face, or the face of a face, and so forth).

.. automethod:: SimplicialComplex.deleteSimplex

.. automethod:: SimplicialComplex.deleteSimplices

.. automethod:: SimplicialComplex.deleteSimplexWithBasis


.. _relabelling-complexes:

Relabelling simplices
---------------------

Simplex labels are often meaningful -- but not always. They can be
relabelled using either functions or dicts, or simply to make them
all unique relative to another complex. This is handy when
:ref:`composing complexes <composing-complexes>`.

.. automethod:: SimplicialComplex.relabel

.. automethod:: SimplicialComplex.relabelDisjointFrom


Copying and equality
--------------------

Complexes can be freely copied, creating independent versions of the same complex.

.. automethod:: SimplicialComplex.copy

They can also be tested for equality.

.. automethod:: SimplicialComplex.__eq__

.. automethod:: SimplicialComplex.__ne__

(See later for other comparison operators relating to sub-complexes.)


Querying the structure of the complex
-------------------------------------

.. automethod:: SimplicialComplex.orderOf

.. automethod:: SimplicialComplex.indexOf

.. automethod:: SimplicialComplex.maxOrder

.. automethod:: SimplicialComplex.numberOfSimplices

.. automethod:: SimplicialComplex.__len__

.. automethod:: SimplicialComplex.numberOfSimplicesOfOrder

.. automethod:: SimplicialComplex.isBasis


Retrieving simplices
--------------------

Simplices can be retrieved in a large number of ways. When we return a
collection of simplices that are always of the same order (such as
faces or basis) we return a Python set; if we potentially return
simplices of different orders we return a list, sorted in terms of the
simplex order (low-order simplices first by default).

.. automethod:: SimplicialComplex.simplices

.. automethod:: SimplicialComplex.simplicesOfOrder

.. automethod:: SimplicialComplex.allSimplices

.. automethod:: SimplicialComplex.simplexWithBasis

.. automethod:: SimplicialComplex.containsSimplex

.. automethod:: SimplicialComplex.containsSimplexWithBasis

.. automethod:: SimplicialComplex.faces

.. automethod:: SimplicialComplex.faceOf

.. automethod:: SimplicialComplex.partOf

.. automethod:: SimplicialComplex.basisOf

.. automethod:: SimplicialComplex.closureOf


Sub-complexes
-------------

A sub-complex is created by removing some (or all) of the simplices
from an existing complex. The most common approach is to restrict the
basis of the complex to some sub-set of 0-simplices; another common
approach is to select this basis using some predicate (for example
using :meth:`allSimplices`) and then restricting the complex to all
simplices that can be built from this basis.

.. automethod:: SimplicialComplex.restrictBasisTo

We define several relationships related to sub-complexes, all based
around the idea of one complex being "less than" another when the latter
contains all for former's simplices in the same topological rrelationships.

.. automethod:: SimplicialComplex.isSubComplexOf

.. automethod:: SimplicialComplex.__lt__

.. automethod:: SimplicialComplex.__le__

.. automethod:: SimplicialComplex.__gt__

.. automethod:: SimplicialComplex.__ge__


Global properties
------------------

Various global properties of complexes can be defined that provide an
overview of its topological structure.

.. automethod:: SimplicialComplex.eulerCharacteristic


Homology
--------

One can regard :term:`homology` simply as a more sophisticated version
of the :term:`Euler characteristic`: a way of counting the holes in a
structure at various dimensions. Unlike the Euler characteristic,
homology is able to differentiate between a triangulated portion of
the plane and two triangulated "islands" one of which contains a hole.
The Euler characteristic of both these structures is 1, but they have
different homology groups and therefore different Betti numbers.

In ``simplicial`` we implement the simplest possible version of
simplicial homology in which simplices are treated as un-oriented, which
leads to chain coefficients over a field :math:`[0, 1]`. This massively
simplifies both the calculations and the explanations.

.. automethod:: SimplicialComplex.isChain

.. automethod:: SimplicialComplex.boundary

.. automethod:: SimplicialComplex.boundaryOperator

.. automethod:: SimplicialComplex.disjoint

.. automethod:: SimplicialComplex.smithNormalForm

.. automethod:: SimplicialComplex.bettiNumbers

.. automethod:: SimplicialComplex.Z


Deriving new complexes
----------------------

New complexes can be derived from old ones by various processes. These
operations are also used to create abstract complexes from "concrete"
complexes that have an associated geometric embedding via the
:class:`Embedding` class.

The :term:`flag complex` is a complex that includes all higher
simplices whose faces are present. Essentially it "fills in the
holes": three sides of a triangle will result in the triangle
2-simplex being created, and so on. It is possible to create the flag
complex from scratch, or incrementally by filling-in any holes left
after creating new simplices.

.. automethod:: SimplicialComplex.flagComplex

.. automethod:: SimplicialComplex.growFlagComplex


.. _composing-complexes:

Composing complexes
-------------------

Complexes can be combined to form larger complexes. The basic
operation works by fusing two complexes on the basis of simplex
labels: use :ref:`relabelling <relabelling-complexes>` to make
disjoint complexes, and then set the corresponding simplices.

.. automethod:: SimplicialComplex.compose


Use of exceptions
-----------------

:class:`SimplicialComplex` does not define any new exceptions. It
raises ``KeyError`` if a simplex if referenced that is not present, or
if a basis is used to retrieve a simplex that isn't defined for it. It
raises ``ValueError`` for problems with the orders of simplices and
other structure errors.
