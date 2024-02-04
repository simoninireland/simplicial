:class:`GraphRepresentation`: Low-dimensional complexes
=======================================================

.. currentmodule:: simplicial

.. autoclass:: GraphRepresentation
   :show-inheritance:


Adding and deleting simplices
-----------------------------

.. automethod:: GraphRepresentation.addSimplex

.. automethod:: GraphRepresentation.newSimplex

.. automethod:: GraphRepresentation.forceDeleteSimplex

.. automethod:: GraphRepresentation.relabelSimplex


Retrieving simplices
--------------------

.. automethod:: GraphRepresentation.simplices

.. automethod:: GraphRepresentation.simplicesOfOrder

.. automethod:: GraphRepresentation.containsSimplex

.. automethod:: GraphRepresentation.maxOrder


Details of individual simplices
-------------------------------

.. automethod:: GraphRepresentation.orderOf

.. automethod:: GraphRepresentation.indexOf

.. automethod:: GraphRepresentation.getAttributes

.. automethod:: GraphRepresentation.setAttributes

.. automethod:: GraphRepresentation.faces

.. automethod:: GraphRepresentation.cofaces

.. automethod:: GraphRepresentation.basisOf


Topological information
-----------------------

.. automethod:: GraphRepresentation.boundaryOperator
