.. _sfrep:

Simplicial function representations
===================================

.. currentmodule:: simplicial

Representations provide the underlying implementations of
:ref:`simplicial functions <function>`, which need different
approaches to support different function types.


:class:`SFRepresentation`: Abstract base class for function representations
---------------------------------------------------------------------------

.. autoclass:: SFRepresentation

.. automethod:: SFRepresentation.setComplex

.. automethod:: SFRepresentation.complex

.. automethod:: SFRepresentation.valueForSimplex

.. automethod:: SFRepresentation.setValueForSimplex

.. automethod:: SFRepresentation.removeSimplex

.. automethod:: SFRepresentation.reset

.. automethod:: SFRepresentation.size

.. automethod:: SFRepresentation.allSimplices



:class:`AttributeSFRepresentation`: Functions from attributes
-------------------------------------------------------------

.. autoclass:: AttributeSFRepresentation
   :show-inheritance:

.. automethod:: AttributeSFRepresentation.valueForSimplex


:class:`LiteralSFRepresentation`: Functions with values given explicitly
------------------------------------------------------------------------

.. autoclass:: LiteralSFRepresentation
   :show-inheritance:


:class:`ComputedSFRepresentation`: Functions over simplices
-----------------------------------------------------------

.. autoclass:: ComputedSFRepresentation
   :show-inheritance:

.. automethod:: ComputedSFRepresentation.f


:class:`InferredSFRepresentation`: Functions over simplices and explicit values
-------------------------------------------------------------------------------

.. autoclass:: InferredSFRepresentation
   :show-inheritance:
