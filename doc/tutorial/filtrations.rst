.. _filtrations:

.. currentmodule:: simplicial

Filtrations
===========

In topology, a filtration is sequence of simplicial complexes that are
ordered by inclusion. That is to say, if :math:`C_1` and  :math:`C_2`
are complexes where :math:`C_1` appears before :math:`C_2` in the filtration,
then :math:`C_1 \le C_2`: :math:`C_1` is a sub-complex of :math:`C_2`.

Another way to think of this is that there is an index set :math:`I` that
is used to index a collection of simplicial complexes :math:`C_i` such that
:math:`i \le j \implies C_1 \le C2`.

The index set might represent time, in which case the filtration models how
a complex grows over time. (Note that it *has* to grow, and can't shrink, as
each complex has to be a sub-complex of those that come after.) Or it might
represent distance in some underlying geometry which is being used to define
a progressively richer simplicial complex. (The :term:`Vietoris-Rips complex`
is usually built like this.) Or one could forget the index set altogether
and treat the filtration simply as a list of complexes with inclusion.

``simplicial``'s :class:`Filtration` class supports all these views, allowing
a filtration to be built from existing complexes or by adding and deleting
simplicies subject to some correctness checking.


Building the filtration from complexes
--------------------------------------

We can construct a sequence of complexes and glue them together into a filtration:

.. code-block:: python

    f = Filtration()

    c = SimplicialComplex()
    c.addSimplex(id = 1)
    c.addSimplex(id = 2)
    c.addSimplex(id = 3)
    f.addComplex(0.0, c)

    c.addSimplex(id = 4)
    c.addSimplex([ 1, 2 ], id = 12)
    f.addComplex(1.0, c)

This creates a filtration with two complexes, indexed by an real number. We can
access the sequence of complexes in the filtration either as a list or by
enumeration:

.. code-block:: python

    for c in f:
       print(c.maxOrder())

    0
    1

Notice that when we built the filtration we created a single complex and added it
twice, having added some simplices; but when we accessed it, we saw two complexes
having different maximum orders. :class:`Filtration` copies any complex that's
added to it into an internal data structure, and so doesn't see any subsequent
changes. The complexes are sanity-checked to make sure that we meet the criteria 
for a filtration, so the following code won't work: 

.. code-block:: python

    c.deleteSimplex(12)
    f.addComplex(2.0, c)

This will fail because the complex being added with index 2.0 isn't a super-complex
of the complex at index 1.0.


Building the filtration from simplices
--------------------------------------

The above example treats the filtration as a sequence of complexes built outside.   
In other circumstances it's easier to build the filtration as a single complex
at different "stages of definition", where we advance the index and add some
simplices. The above example would then look like:

.. code-block:: python

    f = Filtration()

    f.setIndex(0.0)
    f.addSimplex(id = 1)
    f.addSimplex(id = 2)
    f.addSimplex(id = 3)

    f.setIndex(1.0)
    f.addSimplex(id = 4)
    f.addSimplex([ 1, 2 ], id = 12)


Accessing the filtration as a complex
-------------------------------------

The value of the index defines the simplices that are "in scope". The filtration
has the same interface as :class:`SimplicialComplex` and so can be queried about
its contents and so forth:

.. code-block:: python

    print(f.maxOrder())

    1

    f.setIndex(0.0)
    print(f.maxOrder())

    0

Setting the index to 0.0 took the later simplices added at index 1.0 "out of scope"
as far as the behavior of the filtration is concerned. This applies to all the
functions that access the filtration as a complex:

.. code-block:: python

    f.setIndex(0.0)
    3 in f

    False

    f.setIndex(1.0)
    3 in f

    True

You can also delete simplices:

.. code-block:: python

    f.setIndex(0.0)
    f.deleteSimplex(3)

If you delete a simplex that's used within another, higher-order simplex, then those
simplices are also deleted. (This is the standard behaviour of
:meth:`SimplicialComplex.deleteSimplex`.) However, for a filtration this happens
even if the higher-order simplices appear at a later index:

.. code-block:: python

    f.setIndex(0.0)
    f.deleteSimplex(1)
    f.setIndex(1.0)
    12 in f

    False

where the simplex 12 has been deleted along with the simplex in its basis. This
ensures that the filtration respects its inclusion rules.


Accessing the filtration as a sequence of complexes
---------------------------------------------------

You can extract a copy of the filtration at any index value:

.. code-block:: python

    f.setIndex(0.0)
    c = f.snap()

You can also get iterators over the index set:

.. code-block:: python

    for i in f.indices():
       print(i)

    0.0
    1.0

or over the sequence of complexes:

.. code-block:: python

    for c in f.complexes():
       print(len(c))

    3
    5

Accessing the filtration in either of these ways generates "clean" copies of the
complexes, detached from the filtration, whcih can then be changed as required.
The iterators returned by  :meth:`Filtration.indices` and
:meth:`Filtration.complexes` are compatible, in the sense that the order of
complexes matches the order of indices.





