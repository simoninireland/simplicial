:class:`Embedding`: Embedding an abstract complex into space
============================================================

.. currentmodule:: simplicial

.. autoclass:: Embedding

.. important::

   Embeddings are also used to support ``simplicial``'s
   :ref:`drawing routines <drawing>`.


Basic properties of the embedding space
---------------------------------------

The embedding space can have any number of dimensions, defaulting to
two. (At present `simplicial` only supports Euclidian embedding
spaces.)

.. automethod:: Embedding.dimension

.. automethod:: Embedding.origin

.. automethod:: Embedding.complex

The locations give rise to a notion of distance between positions.

.. automethod:: Embedding.distance


Positioning simplices
---------------------

An embedding works by specifying the positions of the 0-simplices of a
complex. Since all higher simplices have a :term:`basis` constructed
of 0-simplices, these positions then induce positions for all the
higher-order simplices.

There are two ways to specify an embedding. The first is to provide
explicit co-ordinates for every 0-simplex in a complex. This is very
general but misses some frequent commonalities, and so the second way
is to provide a sub-class of :class:`Embedding` that overrides the
:meth:`Embedding.computePositionOf` method. The two methods play well
together: one can provide a sub-class to capture the regularities, and
then perturb the complex by moving individual points if
required. (Client code should only use :meth:`Embedding.positionOf` to
access simplex positions, and not access to computation method
directly. This ensures that explicit positions are returned correctly
and cached.)

.. automethod:: Embedding.positionSimplex

.. automethod:: Embedding.computePositionOf

.. automethod:: Embedding.positionOf

.. automethod:: Embedding.positionsOf

.. automethod:: Embedding.clearPositions


Dict-like interface
-------------------

:class:`Embedding` also exports a dict-like interface.

.. automethod:: Embedding.__len__

.. automethod:: Embedding.__getitem__

.. automethod:: Embedding.__setitem__

.. automethod:: Embedding.__contains__


Spatial constructions
---------------------

Embeddings apply a geometry to a topological structure. It can be
useful to go the other way: to take some geometric or spatial
information and create a topological structure from it, where the
topological structure encodes useful information. Typically this
depends on a notion of distance between the located 0-simplices.
The distance metric can then provide a way of constructing
higher-dimensional simplices.

.. automethod:: Embedding.vietorisRipsComplex
