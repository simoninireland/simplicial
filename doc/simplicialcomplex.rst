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

If we just want a new simplex with a given order, we can get one
and `simplicial` will build all the component simplices, all of
which will new new.

.. automethod:: SimplicialComplex.addSimplexOfOrder

Since a simplex is uniquely defined by its :term:`basis`, we can
simply provide the basis and let `simplicial` work out all the
other simplices that need to be added. This can be a major simplification
for higher-order simplices.

.. automethod:: SimplicialComplex.ensureBasis

.. automethod:: SimplicialComplex.addSimplexWithBasis
		
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


Querying the structure of the complex
-------------------------------------

.. automethod:: SimplicialComplex.orderOf

.. automethod:: SimplicialComplex.maxOrder

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


Euler operations
----------------

The Euler operations are based around the :term:`Euler characteristic`
and its numerical derivatives. These are useful for computing various
global topological properties.

Euler integrals are (as the name suggests) integrals computed against
the Euler characteristic of a space.

.. automethod:: SimplicialComplex.eulerCharacteristic

.. automethod:: SimplicialComplex.eulerIntegral

(For more details about Euler integration see :ref:`Baryshnikov and
Ghrist <BG09a>` or :ref:`Curry <CGR14>`.)


Homology
--------

One can regard :term:`homology` simply as a more sophisticated version
of the :term:`Euler characteristic`: a way of counting the holes in a
structure at various dimensions. Unlike the Euler characteristic,
homology is able to differentiate between a triangulated portion of
the plane and two triangulated "islands" one of which contains a hole.
The Euler characteristic of both these structures is 1, but they have
different homology groups and therefore different Betti numbers. 

In `simplicial` we implement the simplest possible version of
simplicial homology in which simplices are treated as un-oriented, which
leads to chain coefficients over a field of [0, 1]. This massively
simplifies both the calculations and the explanations.

.. automethod:: SimplicialComplex.isChain

.. automethod:: SimplicialComplex.boundary

.. automethod:: SimplicialComplex.boundaryMatrix

.. automethod:: SimplicialComplex.disjoint

.. automethod:: SimplicialComplex.smithNormalForm

.. automethod:: SimplicialComplex.bettiNumbers
		

Deriving new complexes
----------------------

New complexes can be derived from old ones by various processes. These
operations are also used to create abstract complexes from "concrete"
complexes that have an associated geometric embedding via the
:class:`Embedding` class.

.. automethod:: SimplicialComplex.flagComplex
