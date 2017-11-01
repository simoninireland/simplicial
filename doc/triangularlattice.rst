:class:`TriangularLattice`: A 2D triangulation of a plane
=========================================================

.. currentmodule:: simplicial
   
.. autoclass:: TriangularLattice

.. automethod:: TriangularLattice.rows

.. automethod:: TriangularLattice.columns


Embedding the lattice
---------------------

.. autoclass:: TriangularLatticeEmbedding

.. automethod:: TriangularLatticeEmbedding.height

.. automethod:: TriangularLatticeEmbedding.width

The actual embedding divides the plane containing to lattice into
roiws and colums, indenting the position of each odd row to form even
triangles.
		
.. automethod:: TriangularLatticeEmbedding.computePositionOf

