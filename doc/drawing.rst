.. _drawing:

.. currentmodule:: simplicial.drawing

Drawing simplicial complexes
============================

Drawing a simplicial complex involves imposing a geometry onto the
topological structure. This is typically very difficult for
high-dimensional complexes -- and can be tricky even for
two-dimensional complexes with lots of strange connections.

.. important::

   At present the drawing routines are very basic.

The drawing routines in `simplicial` are based around the use of the
:class:`simplicial.Embedding` class, which specifies the embedding of a
simplicial complex into a space. Various sub-classes of
:class:`simplicial.Embedding` provide different positionings, which the drawing
sub-system then renders. Note that there is no decent default or
automatic layout generation yet.


Drawing a complex
-----------------

.. autofunction:: drawComplex
