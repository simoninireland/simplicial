:class:`Filtration`: A filtered sequence of complexes
=====================================================

.. currentmodule:: simplicial
   
.. autoclass:: Filtration


Building the filtration
------------------------

Filtrations are built in the same way as ordinary complexes, by adding
(and possibly deleting) simplices. The main difference is simplices
are added to a filtration at a specific index, with the complex associated
with each index growing as the index grows.

.. automethod:: Filtration.addSimplex

The index is managed by selecting the appropriate value for the filtration.

.. automethod:: Filtration.getIndex

.. automethod:: Filtration.setIndex

.. automethod:: Filtration.setPreviousIndex

.. automethod:: Filtration.setNextIndex

.. automethod:: Filtration.setMinimumIndex

.. automethod:: Filtration.setMaximumIndex

.. automethod:: Filtration.indices

.. automethod:: Filtration.isIndex


Copying the filtration
----------------------

Filtrations can be freely copied, either completely or by extracting the simplicial
complex equivalent to the filtration at its current index.

.. automethod:: Filtration.copy

.. automethod:: Filtration.snap


Accessing the filtration
------------------------

The filtration can be accessed using all the normal methods of a simplicial
complex. All the operations occur relative to the current index of the filtration.

.. automethod:: Filtration.containsSimplex

.. automethod:: Filtration.orderOf

.. automethod:: Filtration.indexOf

.. automethod:: Filtration.simplices

.. automethod:: Filtration.numberOfSimplices

.. automethod:: Filtration.numberOfSimplicesOfOrder

It is also possible to examine the structure of the filtration as it is
constructed, by looking at the indexed complexes individually or by examining
the simplices added at each index.

.. automethod:: Filtration.simplicesAddedAtIndex

.. automethod:: Filtration.addedAtIndex

.. automethod:: Filtration.complexes






