.. _simplex-attributes:

.. currentmodule:: simplicial

Simplex attributes
==================

Simplices can also have a dict of attriobutes associated with them, which can be useful
for storing metadata about the underlying data being modelled by the simplicial complex.
Attributes aren't used by other parts of ``simplicial``, but they're very common for
applications.


Setting attributes when adding a simplex
----------------------------------------

The :meth:`SimplicialComplex.addSimplex` operation can add attributes to a simplex when
it is created:

.. code-block:: python

    l45 = c.addSimplex(fs = [ 4, 5 ], id = 45, attr = dict(value = 6))

Similarly :meth:`SimplicialComplex.addSimplexWithBasis` and :meth:`SimplicialComplex.addSimplexOfOrder`
also have an optional `attr` argument to provide attributes.

.. important::

    For :meth:`SimplicialComplex.addSimplexWithBasis` and :meth:`SimplicialComplex.addSimplexOfOrder`
    any attributes will be added to *all* simplices created, not just the "intended" one.


Changing and accessing attributes
---------------------------------

:class:`SimplicialComplex` presents a dict-like interface for accessing attributes:

.. code-block:: python

    v = c[l45]['value']
    c[l45]['value'] = v + 1

Now we can add, delete, and manipulate metadata for simplices, we will also
want to understand :ref:`navigating-complex`.
