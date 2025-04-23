.. _function:

:class:`SimplicialFunction`: Functions over complexes
=====================================================

.. currentmodule:: simplicial

Simplicial functions form the basis for a lot of advanced
functionality in ``simplicial``.

.. autoclass:: SimplicialFunction

Each simplicial function has an underlying :ref:`representation <sfrep>`
that provides the underlying functionality.


Setting and resetting the complex
---------------------------------

.. automethod:: SimplicialFunction.setComplex

.. automethod:: SimplicialFunction.complex

.. automethod:: SimplicialFunction.representation

.. automethod:: SimplicialFunction.reset


The domain and values
---------------------

.. automethod:: SimplicialFunction.domain

.. automethod:: SimplicialFunction.simplices

.. automethod:: SimplicialFunction.valueForSimplex

.. automethod:: SimplicialFunction.removeSimplex

.. automethod:: SimplicialFunction.setValueForSimplex

.. automethod:: SimplicialFunction.setValuesForSimplices

.. automethod:: SimplicialFunction.allSimplices


Calling the function
--------------------

Simplicial functions export two interfaces: as functions that can be
called, and as dicts that can be accessed. Some representations also
allow setting through the dict interface. The number of simplices can
be queried, and the simplices iterated.

.. automethod:: SimplicialFunction.__call__

.. automethod:: SimplicialFunction.__getitem__

.. automethod:: SimplicialFunction.__setitem__

.. automethod:: SimplicialFunction.__contains__

.. automethod:: SimplicialFunction.__len__

.. automethod:: SimplicialFunction.__iter__


Morse theory support
--------------------

.. automethod:: SimplicialFunction.isMorse

.. automethod:: SimplicialFunction.isMorseCritical
