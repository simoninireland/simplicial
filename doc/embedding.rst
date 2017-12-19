:class:`Embedding`: Embedding an abstract complex into space
============================================================

.. currentmodule:: simplicial
   
.. autoclass:: Embedding


Basic properties of the embedding space
---------------------------------------

The embedding space can have any number of dimensions, defaulting to
two. (At present `simplicial` only supports Euclidian embedding
spaces.)

.. automethod:: Embedding.dimension

.. automethod:: Embedding.origin

.. automethod:: Embedding.complex


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



