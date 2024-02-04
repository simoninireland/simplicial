:class:`ReferenceRepresentation`: In-memory simplicial complexes
================================================================

.. currentmodule:: simplicial

.. autoclass:: ReferenceRepresentation
   :show-inheritance:


Adding and deleting simplices
-----------------------------

.. automethod:: ReferenceRepresentation.addSimplex

.. automethod:: ReferenceRepresentation.newSimplex

.. automethod:: ReferenceRepresentation.forceDeleteSimplex

.. automethod:: ReferenceRepresentation.relabelSimplex


Retrieving simplices
--------------------

.. automethod:: ReferenceRepresentation.simplices

.. automethod:: ReferenceRepresentation.simplicesOfOrder

.. automethod:: ReferenceRepresentation.containsSimplex

.. automethod:: ReferenceRepresentation.maxOrder


Details of individual simplices
-------------------------------

.. automethod:: ReferenceRepresentation.orderOf

.. automethod:: ReferenceRepresentation.indexOf

.. automethod:: ReferenceRepresentation.getAttributes

.. automethod:: ReferenceRepresentation.setAttributes

.. automethod:: ReferenceRepresentation.faces

.. automethod:: ReferenceRepresentation.cofaces

.. automethod:: ReferenceRepresentation.basisOf


Topological information
-----------------------

.. automethod:: ReferenceRepresentation.boundaryOperator
