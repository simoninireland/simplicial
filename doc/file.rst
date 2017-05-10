.. _file:

Saving and loading simplicial complexes
=======================================

.. currentmodule:: simplicial.file

There are lots of standard formats for networks, but none (as far as I
know) for simplicial complexes. In the absence of a standard,
`simplicial` uses the most portable storage format, which would be
JSON. We may add new formats if required, since JSON isn't very
efficient especially for large complexes.

File I/O
--------

The basic functions read and write JSON-encoded complexes.

.. autofunction:: read_json

.. autofunction:: write_json

		  
Conversion routines
-------------------

For special cases, the raw conversion routines are also available.

.. autofunction:: as_json

.. autofunction:: as_simplicial_complex

	       
Encoding
--------

.. autoclass:: JSONSimplicialComplexEncoder
	       
