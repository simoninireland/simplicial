:class:`Representation`: The repreesentation of complexes
==========================================================

.. currentmodule:: simplicial

.. autoclass:: Representation


Complex
-------

.. automethod:: Representation.setComplex


Adding and deleting simplices
-----------------------------

.. automethod:: Representation.addSimplex

.. automethod:: Representation.newSimplex

.. automethod:: Representation.forceDeleteSimplex

.. automethod:: Representation.relabelSimplex


Retrieving simplices
--------------------

.. automethod:: Representation.simplices

.. automethod:: Representation.simplicesOfOrder

.. automethod:: Representation.containsSimplex

.. automethod:: Representation.maxOrder


Details of individual simplices
-------------------------------

.. automethod:: Representation.orderOf

.. automethod:: Representation.indexOf

.. automethod:: Representation.getAttributes

.. automethod:: Representation.setAttributes

.. automethod:: Representation.faces

.. automethod:: Representation.cofaces

.. automethod:: Representation.basisOf


Topological information
-----------------------

.. automethod:: Representation.boundaryOperator
