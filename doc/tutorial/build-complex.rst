.. _build-complex:

.. currentmodule:: simplicial

Building a complex
==================

Creating a simplicial complex is very straightforward:

..  code-block:: python

    from simplicial import *

    c = SimplicialComplex()

The resulting :term:`complex` is empty, containing no simplices.


Adding simplices
----------------

We can now start to add some simplices:

.. code-block:: python

    # add a simplex with a generated name
    s1 = c.addSimplex()

    # add simplices whose names we want to specify
    s2 = c.addSimplex(id = 2)
    s3 = c.addSimplex(id = 3)

These lines all add 0-simplices -- points -- to the complex. The :meth:`SimplicialComplex.addSimplex`
method returns the name of the simplex added, which will either be the one given in its `id` argument or
a synthetic one if no name is given explicitly. We can then build 1-simplices -- lines -- by
providing two 0-simplices as endpoints:

.. code-block:: python

    l23 = c.addSimplex(fs = [ 2, 3 ])

The `fs` ("faces") argument names each :term:`face` of the higher simplex. A 1-simplex (a line, a one-dimensional
structure) has two 0-simplices (points, 0-dimensional structures) as faces. A 2-simplex (a triangle, a 2-dimensional
structure) has three 1-simplices (lines) as faces:

.. code-block:: python

    l12 = c.addSimplex(fs = [ s1, 2 ])
    l31 = c.addSimplex(fs = [ s1, 3 ])

    # create the triangle
    t123 = c.addSimplex(fs = [l12, l23, l31])

So adding a new *k*-simplex requires providing *(k + 1)* *(k - 1)*-simplices as faces.
:meth:`SimplicialComplex.addSimplex` checks to make sure that the right nmumber of faces,
of the right :term:`order`, are provided.

If you just want a new simplex of a given order, entirely disjoint from the other
simplices in the complex, you can create one:

.. code-block:: python

    txyz = c.addSimplexOfOrder(2, id = 'xyz')

This will create all the necessary simplices: 1 2-simplex (a triangle), three 1-simplices (the edges),
and 3 0-simplices (the vertices), all with unique names. (In this case we provided a name for the
triangle.)

A *k*-simplex has $(k + 1) 0-simplices as its vertices, referred to as its :term:`basis`. We can create
a simplex directly by specifying its basis:

.. code-block:: python

    s5 = c.addSimplex(id = 5)
    s6 = c.addSimplex(id = 6)
    l56 = c.addSimplex(fs = [ s5, s6 ])

    tabc = c.addSimplexWithBasis(bs = [ s3, s5, s6 ], id = 'abc')

Like :meth:`SimplicialComplex.addSimplexOfOrder`, :meth:`SimplicialComplex.addSimplexWithBasis` will add
any simplices that are needed but that don't already exist in the complex: in the example above, in order
to cvreate the triangle `abc` it would need to create lines between `s3` and `s5` and between `s3` and `s6`,
but could use the existing line between `s5` and `s6` as the third face. (This works because there can be at
most one simplex with a given basis.) :meth:`SimplicialComplex.addSimplexWithBasis` will raise an exception if
a simplex with this basis already exists, unless its optional `ignoreDuplicate` argument is set to `True` whereupon
the duplicate simples will be silently ignored.


Deleting simplices
------------------

Simplices can be deleted from a complex very simply:

.. code-block:: python

    c.deleteSimplex(s5)

The same effect can be had through an operator interface:

.. code-block:: python

    del c[s5]

In either case, deleting `s5` would remove part of the basis for the triangle `tabc` as well as the endpoint
for two of its faces, and these simplices will automatically be deleted as well.

.. important::

    Deleting a simplex will delete all the simplices of which it is part. This implies
    that deleting a simplex may delete other simplices of higher orders than itself.
    The exact simplices deleted can be found using :meth:`SimplicialComplex.partOf`.

As well as adding and deleting simplices, we may want to store and retrieve :ref:`simplex-attributes`.


