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

.. automethod:: SimplicialFunction.reset


Calling the function
--------------------

Simplicial functions export two interfaces: as functions that can be
called, and as dicts that can be accessed. Some representations also
allow setting through the dict interface.

.. automethod:: SimplicialFunction.__call__

.. automethod:: SimplicialFunction.__getitem__

.. automethod:: SimplicialFunction.__setitem__


Morse theory support
--------------------

.. automethod:: SimplicialFunction.isMorse

.. automethod:: SimplicialFunction.isMorseCritical
