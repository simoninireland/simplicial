.. _homology:

:class:`Homology`: Homology theories
====================================

.. currentmodule:: simplicial

A homology theory provides a way of describing, creating, and
manipulating chains with coefficients drawn from a specific type.
Different theories allow different properties to be expressed.

.. autoclass:: Homology


Coefficient testing
-------------------

.. automethod:: Homology.isValidCoefficient


Boundary extraction
-------------------

.. automethod:: Homology.boundary


:class:`HomologyZ2`: Homology over :math:`\mathbb{Z}_2`
-------------------------------------------------------

.. autoclass:: HomologyZ2
