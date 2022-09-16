:class:`ReferenceRepresentation`: The reference implementation of complexes
===================================================================================

.. currentmodule:: simplicial

.. autoclass:: ReferenceRepresentation

.. important::

   More useful methods for manipulating complexes are described under
   :class:`SimplicialComplex`. The descriptions below are mainly for
   the aid of those wanting to write new representations


Complex
-------

.. automethod:: ReferenceRepresentation.setComplex


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


Optimised versions of core methods
----------------------------------

.. automethod:: ReferenceRepresentation.simplexWithBasis
