.. _navigating-complex:

.. currentmodule:: simplicial

Navigating and querying a complex
=================================

Order
-----

Any complex will have simplices of a maximum order:

.. code-block:: python

    maxk = c.maxOrder()

Given the constraints on a simplicial complex, a complex with maximum order *k* will
have simplices of all orders from *k* down to (and including) 0.

It is often handy to be able to query a given simplex for its order:

.. code-block:: python

    k = c.orderOf(l45)

It can also be useful to query a complex as to how many simplices it has of each order:

.. code-block:: python

    ks = c.numberOfSimplicesOfOrder()

:meth:`SimplicialComplex.numberOfSimplicesOfOrder` returns a dict mapping orders to the
number of simplices of that order. The simplices themselves can be retrieved using
:meth:`SimplicialComplex.simplicesOfOrder`.


Retrieving simplices
--------------------

The simplest opeartion for accessing a complex is to access all the simplex names:

.. code-block:: python

    ss = c.simplices()

It is also possible to access only those simplices of a given order, for example:

.. code-block:: python

    ss = c.simplicesOfOrder(2)

which retrieves the names of all 2-simplices (triangles). It is sometimes also useful to
filter the list of simplices by providing a suitable predicate, mapping a complex and a simplex
within it to a boolean:

.. code-block:: python

    def atleast(c, s):
        return (c[s]['value'] > 5])

    ss = c.allSimplices(atleast)

which would retrieve all simplices having a `value` attribute greater than 5.


Finding simplices
-----------------

Testing whether a simplex is in a complex can happen through a procedural or an
operator interface:

.. code-block:: python

    if c.contrainsSimplex(l23):
        print('yes')
    else:
        if l13 in c:
            print('but yes')

Another frequent operation is to check whether the complex contains a simplex
with a given basis:

.. code-block:: python

    if c.containsSimplexWithBasis([ s1, s2, s3 ]):
        print('yes')

The simplex itself can also be retrieved directly:

.. code-block:: python

    s = c.simplexWithBasis([ s1, s2, s3 ])
    if s is not None:
        print('we have simplex {s}'.format(s = s))
    else:
        print('no')


Traversing the simplex hierarchy
--------------------------------

Simplices are arranged in a hierarchy according to the face relationship. A *k*-simplex must
by definition have *(k + 1)* *(km- 1)*-simplices as its faces. We can traverse up and down
this hierarchy from a startign simplex. To find the faces of a simplex, we use:

.. code-block:: python

    fs = c.faces(l23)

:meth:`SimplicialComplex.faces` is "one-step". in the sense that it returns the
simplices that are faces of this simplex -- but not the faces of those simplices,
and so on. For this we nee the transitive closure of the operation:

.. code-block:: python

    fs = c.closureOf(l23)

which returns all the simplices that make up the given simplex, down to its :term:`basis`
(its :term:`closure`). We can, if desired, skip straight to the basis:

.. code-block:: python

    fs = c.basisOf(l23)

In the opposite direction, to find those simplices a simplex is a face of, we use:

.. code-block:: python

    fs = c.faceOf(l23)

This is again a "single-step" operation, and we may also need a transitive closure:

.. code-block:: python

    fs = c.partOf(l23)

(In the topology literature this operation if often called the :term:`star` of the
starting simplex.)

Building and navigating a complex are only building blocks to its :ref:`complex-analysis` using
various tools from topology.




