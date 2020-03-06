.. currentmodule:: simplicial


Computing homology
==================

The notion of :term:`homology` is central to topology.


The homology theory we use
--------------------------

Since ``simplicial`` is about simplicial complexes we're clearly implementing some
form of simplicial homology. Unfortunately things aren't quite that simple.

Homology is defined in terms of p-chains, collections of simplices of order p.
Different applications care about different properties of these p-chains.
The most basic thing we might care about is: can a chain contain a given simplex
more than once? This would let us define a path that went around a loop twice,
where every simplex would appear twice. Another thing we might care about is:
which direction do we pass over a simplex when traversing a chain? That would let
us describe paths that fully or partially reversed themselves.

Mathematically these choices of "what we care about" are represented as a choice
of what coefficients are allowed for each simplex in the chain. If we care about
multiple occurrances, we need to count the number of those occurrances; if we care
about direction of travel, we need to be able to use positive and negative coefficients to
represent the directions. A general homology theory will typically allow coefficients
to be taken from any field, with the integers usually being adequate. You'll see
this referred to as "homology over :math:`\mathbb{Z}`" in the literature.

``simplicial`` instead uses the simplest possible homology theory where coefficients
are taken from a boolean field 0 or 1: a simplex either appears in a p-chain or doesn't,
with no repetition and no consideration of direction. (Formally this is "homology
over :math:`\mathbb{Z}/2`"). This is adequate for many applications, notably those in
data analytics -- but it isn't adequate for some, so care may be needed.


Boundary operators
------------------

Every k-simplex has, by definition, (k + 1) faces each of which is a (k - 1)-simplex:
a triangle (a 2-simplex) is defined by three faces, each of which is a line (a 1-simplex),
each of which is in turn defined by two endpoints (0-simplices). For any order k we
can therefore define a boundary operator, usually denoted :math:`\partial_k` in the
literature that maps a simplex of order k to the set of (k + 1) (k - 1)-simplices
that form its boundary.

For any order k the boundary operator can be represented as an n*m matrix for a complex
having n (k - 1)-simplices and m k-simplices. Each column of the matrix represents
a k-simplex, each row a (k - 1)-simplex, and there is a 1 at position (i, j) if
simplex i is a face of simplex j: the matrix is zero everywhere else.

Since the boundary operator encodes a lot of information we maintain it as
the complex is constructed: the :meth:`SimplicialComplex.addSimplex` and related
methods all update both the lists of simplices and the boundary operator matrices.


Betti numbers and Smith normal form
------------------------------------

A basic use of homology is to compute the number of holes of different dimensions in
a complex, where a (p + 1)-dimensional hole is defined by a p-chain that is a cycle
(returing to its starting point) but not the boundary of a (p + 1)-simplex. Three
lines that form a triangle define a 1-hole if the triangle itself isn't "filled
in" as a 2-simplex. The :term:`Betti numbers` count the holes at different dimensions: the p'th Betti
number is the number of p-dimensional holes. The 0th Betti number returns the number
of connected components in the complex; the 1st Betti number returns the number of
holes sorrounded by lines; 2nd the number of voids surrounded by triangles; and so forth.

We compute the Betti numbers from the boundary matrices. We reduce each boundary matrix
to its Smith normal form, by re-arranging it using row and column operations until
it consists of a matrix that has 1 for some prefix of its diagonal and is zero
elsewhere. The numbers of zero columns, and the number of non-zero rows, provide
the sizes of the kernel and boundary groups needed to compute the Betti number.

The reduction to Smith normal form uses an algorithm due to Herbert Edelsbrunner described 
`here <https://www.cs.duke.edu/courses/fall06/cps296.1/Lectures/sec-IV-3.pdf>`_.
It is simpler than many others found in the literature because of our use
of homology over :math:`\mathbb{Z}/2`. (A more general homology theory would have a Smith
normal form with the same structure but with more general non-zero elements
instead of only ones.) It still however has a computational complexity of roughly
:math:`O(n_k^3)` for a complex with :math:`n_k` k-simplices.


The :math:`Z_k` sub-group
-------------------------

Betti numbers only identify the number of holes at each dimension. The structure of the
boundary operators actually provides more information than this, in that we can compute
the basis for all the k-chains in the complex that are cycles without being boundaries --
in other words, the holes bounded by simplices of order k.

The computation involes making use of the linear algebra implicit in the computation of
the Smith normal form. The row and column operators used to reduce the matrix are
also implicitly changing the basis for the underlying group. If we keep track of the operations
and reflect them into the set of simplices of the right order, we can find the basis for
the sub-group of non-boundary cycles, usually denoted :math:`Z_k`.

Imagine that the rows and columns of the boundary operator are labelled with the simplices
that they represent: for :math:`\partial_k` this means that rows represent (k - 1)-simplices
and columns represent k-simplices. Reduction to Smith normal form works by exchanging pairs
of rows (or columns), and adding one row (or column) to another row (or column). Extend these
matrix operations to work on the labels as well as the elements. When the matrix is fully
reduced, the number of zero columns represents the degree of :math:`Z_k` (which we use
when computing the Betti numbers); the labels on these columns form a basis for :math:`Z_k`,
which is to say that any cycle around a hole can be constructed as some combination of the
basis elements.

