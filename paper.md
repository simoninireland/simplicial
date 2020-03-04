---
title: 'simplicial: Simplicial topology in Python'
tags:
  - Python
  - computational science
  - data analytics
  - topology
  - homology
 authors:
  - name: Simon Dobson
    email: simon.dobson@computer.org
    orcid: 0000-0001-9633-2103
    affiliation: 1
 affiliations:
  - name: School of Computer Science, University of St Andrews UK
    index: 1
 date: 19 September 2019
 ---
 
 # Summary
 
Topology is the study of shapes [@Edel2014]. It is different from geometry
in that it studies properties that are invariant under transformations
such as scaling, folding and rotation -- but not to tearing. Topology
can be used to model and analyse lots of important phenomena, including the
relationships inside datasets, the objects represented by point clouds, the
constraints on solutions to problems, and so forth. It is therefore a
potentially important tool for scientific data analysis.
 
Classical topology is built around sets and continuous
functions between them, but this can be awkward for computational
applications. A number of discrete approaches to topology exist, however,
which turn problems in analysis into problems of combinatorics,
which are much more amenable to computational approaches. The simplest
such approach is simplicial topology, in which topological spaces are
represented using points, line, triangles, tetrahedra, and their higher-dimensional
analogues. We can then define various topological operations over these spaces.

``simplicial`` is an implementation of simplicial topology in Python. It can
create, represent, and evolve simplicial complexes, and provides a library
of topological operations that be used to analyse the resulting structures. It
scales moderately, up to systems with several thousand points and higher simplices:
it's probably not suitable for maniupulating huge point clouds or other very
large datasets, which require different programming techniques.
 
# Compatibility and availability

``simplicial`` works with both Python 2.7 and Python 3.7, and can be installed directly
from [PyPy](https://pypi.org/project/epyc/) using ``pip``. API and tutorial
documentation can be found on [ReadTheDocs](https://simplicial.readthedocs.io/en/latest/).
Source code is available on [GitHub](https://github.com/simoninireland/simplicial), where
issues can also be reported.

# References
