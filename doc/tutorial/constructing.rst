.. _construct-complex:

.. currentmodule:: simplicial

Constructing a complex from other complexes
===========================================

We've previously seen how we can go about :ref:`build-complex` by adding
simplices. There is another method that's sometimes useful, which is to
build (or at least start bujilding) a complex by combining other complexes
and then gluing them together by fusing some of their 0-simplices.
``simplicial`` provides a small set of functions that create common kinds
of complex for this purpose.


Simplices
---------

The simplest generator constructs a k-simplex, either in an existing complex
or by creating a new, empty, complex and populating it with a single simplex
using :func:`k_simplex`:

.. code-block:: python

    c = k_simplex(3, id = 'new-3-simplex')

In this case a new complex c is created and populated with a single 3-simplex
(a tetrahedron), which is then given an identifier. (It could also be given
attributes.) The 3-simplex will of course require the construction of
4 0-simplices for its basis, 4 2-simplices (triangles) to be its immediate faces,
and 6 1-simplices (lines) to form the triangles.

.. code-block:: python

    print(c.numberOfSimplicesOfOrder())

    [4, 6, 4, 1]

These simplices are created automatically and are "anonymous" in the sense of
having names generated for them. (If no id is provided for the top-most k-simplex,
it will get an automatic name as well.)

.. warning::

    High-order simplices contain a huge amount of topological information as well
    as a *lot* of simplices for their faces. Creating such high-order structures
    can therefore be very time-consuming and use a lot of memory for the internal
    data structures.

    As an illustration, creating a 10-simplex on a reasonably powerful developer
    laptop takes about four minutes.

If we already had a complex c we could add the k-simplex to it directly:

.. code-block:: python

    c = k_simplex(3, id = 'new-3-simplex', c = c)

This would raise an exception if a simplex with that name already existed in c.
The complex returned is the same one passed in, now containing the new simplex.


Skeletons and voids
-------------------

We can also create the "skeleton" of a k-simplex :func:`k_skeleton`, consisting
just of points and lines (0- and 1-simplices) with no higher simplices filled in.

.. code-block:: python

    c = k_simplex_skeleton(3)
    print(c.numberOfSimplicesOfOrder())

    [4, 6]

Notice that, compared to :func:`k_simplex`, :func:`k_skeleton` does not create any
simplices of order greater than 1.

.. note::

    A high-order k-skeleton, unlike a high-dimensional k-simplex, is a
    relatively compact structure as it only contains 0- and 1-simplices
    regardles of the order of the skeleton overall.

    As an illustration, creating a 10-skeleton on the same laptop used
    for creating the 10-simplex above takes around 0.05s.

We can also create voids using :func:`k_void`, which creates the k-simplices needed
to surround a (k + 1)-dimensional void.

.. warning::

    The k in :func:`k_void` refers to the order of the simplices that *surround*
    the void, *not* the order of the void itself.

.. code-block:: python

    c = k_void(2)
    print(c.numberOfSimplicesOfOrder())

    [4, 6, 4]

Notice that we have the same numbers and orders of simplices in creating a 2-void
as we had earlier in the call to :func:`k_simplex` when creating a 3-simplex:
the 2-void surrounds the 3-simplex, which isn't itself created. (A call to
:func:`k_void` for order k is equivalent to to a call to :func:`k_simplex` for
order (k + 1) followed by calling :meth:`SimplicialComplex.deleteSimplex` to delete
the unwanted (k + 1)-simplex.)


Connecting complexes together
-----------------------------

TBD


