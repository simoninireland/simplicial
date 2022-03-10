.. simplicial documentation master file, created by
   sphinx-quickstart on Wed Mar  8 12:51:43 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

simplicial: Simplicial topology in Python
=========================================

What is simplicial topology?
----------------------------

*Topology* is the study of shapes. It is separate from *geometry* in
that it is interested in properties that are preserved under smooth
transformations such as stretching, bending, and rotating -- but not
tearing. Classical point-set topology forms shapes using sets of
points and functions between them.  The theory is extremely elegant,
but often not particularly tractable for computational use.

There are various forms of *discrete* or *cellular* topology that are
more computation-friendly.  *Simplicial* topology is a discrete
topology based around collections of points, lines, triangles,
tetrahedra, and their extensions to higher dimensions. It is probably
the simplest topological machine there is that's amenable to
computation, since its built from combinatorial, rather than
continuous, operations and functions.

You can use simplicial topology to model any number of things:
approximations of curved surfaces, point-cloud data, the relationships
between elements of a dataset, constraints on solutions to a problem,
and so forth. Once you've modelled a problem in this way, you can use
topological techniques to study it.


What is ``simplicial``?
-----------------------

``simplicial`` is a Python library for creating, manipulating, and
exploring simplicial complexes. It aims to provide a useful set of
features for programmers and mathematicians while remaining scalable
to deal with large complexes. "Large" here means a few-thousands of
points and simplices: ``simplicial`` isn't suitable for dealing with
large image datasets or extremely high-dimensional spaces, which
require more advanced programming techniques.


Current features
----------------

* Compatible with Python 3.7 (and later)
* Represents finite closed simplicial complexes, with a lot of
  checking to ensure that that they stay legal as simplices are added
  and removed (a common source of errors)
* Allows complexes to be embedded into spaces of arbitrary dimension
  to allow geometric as well as topological calculations to be
  performed
* Computes derived structures such as flag complexes, Vietoris-Rips
  complexes, and the like
* Performs homology computations, computes Euler characteristics, does
  Euler characteristic integration, and other interesting operations
* Annotated with ``typing`` type annotations


.. toctree::
   :hidden:

   installation
   tutorial
   reference
   implementation
   glossary
   zbibliography
   acknowledgements
   contributing
