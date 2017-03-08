:class:`SimplicialComplex`: An abstract topological space
=========================================================

.. currentmodule:: simplicial
   
.. autoclass:: SimplicialComplex


Creating a complex
------------------

.. automethod:: SimplicialComplex.__init__
	       
	       
Adding simplices
----------------

A :term:`simplex` is added to a complex by providing some or all of
the following information: a name for the simplex, a list of its
faces, and a dict of attributes.

.. automethod:: SimplicialComplex.addSimplex

It is also possible to copy simplices from one complex to
another. This will cause problems if the two complexes share simplices
with common names (since names must be unique), in which case  a
renaming mapping can be applied automatically during the copy process.

.. automethod:: SimplicialComplex.addSimplicesFrom


Deleting simplices
------------------

Since :class:`SimplicialComplex` represents closed simplicial
complexes -- in which all the faces of all the simplices in a complex
are also in the complex -- deletion requires that we cascade deletions
to delete all the simplices of which a to-be-deleted simplex is a part
(a face, or the face of a face, ad so forth).

.. automethod:: SimplicialComplex.deleteSimplex


Querying simplices
------------------

.. automethod:: SimplicialComplex.order

.. automethod:: SimplicialComplex.maxOrder

.. automethod:: SimplicialComplex.numberOfSimplicesOfOrder

.. automethod:: SimplicialComplex.disjoint


Retrieving simplices
--------------------

.. automethod:: SimplicialComplex.simplices

.. automethod:: SimplicialComplex.simplicesOfOrder

.. automethod:: SimplicialComplex.allSimplices

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

(For more details see :ref:`Baryshnikov and Ghrist <BG09a>`.)
