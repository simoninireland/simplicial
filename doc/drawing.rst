.. _drawing:

Drawing simplicial complexes
============================

.. currentmodule:: simplicial.drawing

Drawing a simplicial complex involves imposing a geometry onto the
topological structure. This is typically very difficult for
high-dimensional complexes -- and can be tricky even for
two-dimensional complexes with lots of strange connections.

At the moment ``simplicial``'s drawing functions are very
rudimentary. They are based on the drawing functions of the
``networkx`` complex networks package, but without the automatic
layout algorithms: we may add them at some point. At present, the
programmer is responsible for defining a decent layout, and we have a
layout for triangular planar lattices. We also only deal with
complexes of limited complexity, again mainly because of the lack of
decent automated layout tools. 


Generating a layout
-------------------

A layout places the 0-simplices of a complex into the drawing space,
thereby endowing the topological structure complex with a
geometry. 

.. autofunction:: triangular_lattice_positions
	  
		   
Drawing a complex
-----------------

Once a layout has been defined, the :func:`draw_complex` function will
draw the complex using ``matplotlib``.

.. autofunction:: draw_complex
		  
	       
