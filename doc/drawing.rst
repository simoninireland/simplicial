Drawing simplicial complexes
============================

.. currentmodule:: simplicial.drawing

Drawing a simplicial complex involves imposing a geometry onto the
topological structure. This is typically very difficult for
high-dimensional complexes -- and can be tricky even for
two-dimensional complexes with lots of strange connections.

At the moment ``simplicial``'s drawing functions are very
rudimentary. They are based on the drawing functions of the
``networkx`` networks package, but without the automatic layout
algorithms (we may add them at some point). At present, the programmer
is responsible for defining a decent layout, and we have a layout for
triangular planar lattices.


Generating a layout
-------------------

TBD

		   
Drawing a complex
-----------------

Once a layout has been defined, the :func:`draw_complex` function will
draw the complex using ``matplotlib``.

.. autofunction:: draw_complex
		  
	       
