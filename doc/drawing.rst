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

This routine is a wrapper for a more basic routine that creates patch
collections representing the simplices of different orders.

.. autofunction:: patchesForComplex

This function is the building block for :func:`drawComplex`
and other plotting functions. It only needs to be called directly if
some more complicated plotting is required.


Drawing an Euler characteristic integration
-------------------------------------------

Euler characteristic integration using :class:`EulerIntegrator` can be
hard to understand. This function draws the "flooding landscape"
associated with the integral based on the level sets for the
integration metric.

.. autofunction:: drawEulerIntegral
