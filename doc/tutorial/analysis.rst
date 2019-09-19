.. _complex-analysis:

.. currentmodule:: simplicial

Analysing a complex
===================

Unlike the operations for :ref:`navigating-complex` which are *local*, beginning from
a single simplex, analysis operations are typically *global*, saying something about the
properties of the entire complex. Often each property is a :term:`topological invariant`
of a :term:`complex`, immune to "unimportant" changes.


Euler characteristics
---------------------

The :term:`Euler characteristic` for a complex :math:`S` is defined as:

.. math::

    \chi(S) = \sum_{k = 0}^{\infty} (-1)^k \, \#S_k

where :math:`\#S_k` represents number of *k*-simplices in :math:`S`. More intuitively,
we compute "points minus lines plus triangles minus tetrahedra plus..." and so on, for
all the orders in the complex. ``simplicial`` computes the Euler characteristic directly:

.. code-block:: python

    chi = c.eulerCharacteristic()


Homology and Betti numbers
--------------------------

The idea of :term:`homology` is to detect "holes of different dimensions" in a complex. Homology
works by creating groups that reflect the hole structure at each different order of simplex in the
complex. ``simplicial`` includes a particular implementation of simplicial homology that can be used
to perform such analyses.

The simplest interface is used to compute the :term:`Betti numbers` of a complex, returning a dict
for each order:

.. code-block:: python

    bs = c.bettiNumbers()

One can optionally provide a list of the dimensions of interest.

Given a set of *k*-simplices, the :term:`boundary` is the set of *(k - 1)*-simplices that appear "unconnected"
at the edge; The boundary of a single 1-simples, for example, is trhe set of two 0-simplices that are
its endpoints; a triangle of 1-simplices has no boundary. We can compute boundaries directly:

.. code-block:: python

    bs = c.boundary([ l12, l23 ])


