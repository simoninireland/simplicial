# Drawing routines for simplicial complexes
#
# Copyright (C) 2017--2019 Simon Dobson
#
# This file is part of simplicial, simplicial topology in Python.
#
# Simplicial is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Simplicial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Simplicial. If not, see <http://www.gnu.org/licenses/gpl.html>.

import collections
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Iterable, Callable, Union, Tuple
from simplicial import SimplicialComplex, Simplex, Embedding

# Helper type for colours (not defined by matplotlib)
Color = Union[str,                                # named colours
              Tuple[float, float, float],         # RGB triples
              Tuple[float, float, float, float]]  # RGBA quads


def draw_complex(c: SimplicialComplex, em: Embedding,
                 ax: mpl.axes.Axes = None,
                 color: Iterable[Color] = None,
                 color_simplex: Callable[[SimplicialComplex, Simplex, int], Color] = None,
                 node_size: float = 0.02):
    """Draw a simplicial complex embedded in space.

    The colours of the simplices are taken either from the color
    array or from the color_simplex function: the latter overrrides
    the former if both are provided.

    At present we only deal with simplices of order 2 and less.

    :param c: the complex
    :param em: embedding providing the positions of the 0-simplices
    :param ax: the axes to draw in (defaults to main axes)
    :param color: an array of colours for the different simplex orders (defaults to a "reasonable" scheme)
    :param color_simplex: a function from complex, simplex and order to a colour (defaults to order color)
    :param node_size: the size of the node (0-simplex) markers"""

    # fill in the argument defaults where not specified
    if ax is None:
        # main figure axes
        ax = plt.gca()
    no = c.maxOrder()
    if color is None:
        # a simple colour scheme that seems to work
        color = ['blue', 'black', 'red']
    else:
        if isinstance(color, collections.Sequence):
            # make sure we have enough colours for all the simplex orders
            if len(color) < no:
                color.append(['blue'] * ((no + 1) - len(color)))
    if color_simplex is None:
        # no per-node colours, default to the color array
        color_simplex = lambda a, b, o: color[o]

    # set up the axes
    ax.set_xlim([-0.2, 1.2])      # axes bounded around 1
    ax.set_ylim([-0.2, 1.2])
    ax.grid(False)                # no grid
    ax.get_xaxis().set_ticks([])  # no ticks on the axes
    ax.get_yaxis().set_ticks([])

    # draw the node markers
    for s in c.simplicesOfOrder(0):
        (x, y) = em[s]
        circ = plt.Circle([x, y],
                          radius=node_size,
                          edgecolor='black', facecolor=color_simplex(c, s, 0),
                          zorder=3)
        ax.add_patch(circ)

    # draw the edges
    for s in c.simplicesOfOrder(1):
        fs = list(c.basisOf(s))
        (x0, y0) = em[fs[0]]
        (x1, y1) = em[fs[1]]
        line = plt.Line2D([x0, x1], [y0, y1],
                          color='black', # color = color_simplex(c, s, 1),
                          zorder=2)
        ax.add_line(line)

    # fill in the triangles
    for s in c.simplicesOfOrder(2):
        fs = list(c.basisOf(s))
        (x0, y0) = em[fs[0]]
        (x1, y1) = em[fs[1]]
        (x2, y2) = em[fs[2]]
        tri = plt.Polygon([[x0, y0], [x1, y1], [x2, y2]],
                          edgecolor='black', facecolor=color_simplex(c, s, 2),
                          zorder=1)
        ax.add_patch(tri)
