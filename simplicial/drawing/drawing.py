# Drawing routines for simplicial complexes
#
# Copyright (C) 2017--2024 Simon Dobson
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

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from matplotlib.patches import Circle, Polygon, PathPatch
from matplotlib.colors import Colormap
from simplicial import SimplicialComplex, Embedding, SimplicialFunction


# Default palette for simplices of different orders
palette = ['k', 'k', '0.75']


def patchesForComplex(c: SimplicialComplex, em: Embedding,
                      sf: SimplicialFunction = None,
                      simplexColours = None, simplexSize = 0.02):
    '''Return a list of patch collections for the complex.

    We currently only handle simplices up to and including :math:`k = 2`.

    :param c: the complex
    :param em: embedding providing the positions of the 0-simplices
    :param sf: (optional) the metric
    :param simplexColours: (optional) simplex colours
    :param simplexSize: (optional) the size of the node (0-simplex) markers

    '''

    # build the colour mapping as a function
    if simplexColours is None:
        # no colour, use the default palette
        col = lambda c, s, k: palette[k]
    elif isinstance(simplexColours, list):
        # list of colours per simplex order
        col = lambda c, s, k: simplexColours[k]
    elif isinstance(simplexColours, dict):
        # dict of individual simplex colours
        col = lambda c, s, k: simplexColours[s]
    elif isinstance(simplexColours, Colormap):
        # colour map accessed using metric
        if sf is None:
            raise ValueError('Need a metric to plot using a colourmap')
        col = lambda c, s, k: simplexColours(sf(s))
    elif callable(simplexColours):
        # function from complex, simplex, and order to colour
        col = simplexColours
    else:
        # fixed colour for all simplices
        col = lambda c, s, k: simplexColours

    # draw the node markers
    nodes = []
    for s in c.simplicesOfOrder(0):
        (x, y) = em[s]
        circ = Circle([x, y],
                      radius=simplexSize,
                      edgecolor='black', facecolor=col(c, s, 0))
        nodes.append(circ)

    # draw the edges
    edges = []
    for s in c.simplicesOfOrder(1):
        fs = list(c.basisOf(s))
        (x0, y0) = em[fs[0]]
        (x1, y1) = em[fs[1]]
        line = PathPatch(Path([(x0, y0), (x1, y1)]),
                         color=col(c, s, 1))
        edges.append(line)

    # fill in the triangles
    triangles = []
    for s in c.simplicesOfOrder(2):
        fs = list(c.basisOf(s))
        (x0, y0) = em[fs[0]]
        (x1, y1) = em[fs[1]]
        (x2, y2) = em[fs[2]]
        tri = Polygon([[x0, y0], [x1, y1], [x2, y2]],
                      edgecolor='None', facecolor=col(c, s, 2))
        triangles.append(tri)

    # construct the patch collections and return
    # (We ned to do this because the zorder binds to the patch collection,
    # not to the individual patches.)
    nodePatches = PatchCollection(nodes, zorder=3, match_original=True)
    edgePatches = PatchCollection(edges, zorder=2, match_original=True)
    trianglePatches = PatchCollection(triangles, zorder=1, match_original=True)
    return [nodePatches, edgePatches, trianglePatches]


def drawComplex(c: SimplicialComplex, em: Embedding,
                sf: SimplicialFunction = None,
                ax = None, backgroundColour = '0.95',
                subfieldXY = None, subfieldWH = None,
                simplexColour = None, simplexSize = 0.02):
    """Draw a simplicial complex embedded in space.

    The colours of simplices are taken from simplexColour which can be
    a none for a default palette, a constant, a list of colours per
    order, a dict mapping simplex to colour, a colourmap, or a
    function taking the complex, simplex, and order and returning a
    colour. When a colourmap is used, the simplicial function is
    used to extract the appropriate colour (and so muct be present)

    At present we only deal with simplices of order 2 and less.

    :param c: the complex
    :param em: embedding providing the positions of the 0-simplices
    :param sf: the metric
    :param ax: the axes to draw in (defaults to main axes)
    :param backgroundColour: the background colour for the field (default '0.95')
    :param subfieldXY: the bottom-left corner of the sub-field to draw (default all)
    :param subfieldWH: the width and heigh of the sub-field to draw (default all)
    :param simplexColour: simplex colours
    :param simplexSize: the size of the node (0-simplex) markers

    """

    # fill in the argument defaults where not specified
    if ax is None:
        # main figure axes
        ax = plt.gca()
    if subfieldXY is None:
        subfieldXY = [0.0, 0.0]
    if subfieldWH is None:
        subfieldWH = [1.0 - subfieldXY[0], 1.0 - subfieldXY[1]]

    # draw the complex
    pcs = patchesForComplex(c, em, sf, simplexColour, simplexSize)
    for pc in pcs:
        ax.add_collection(pc)

    # configure the axes
    ax.set_xlim(subfieldXY[0], subfieldXY[0] + subfieldWH[0])
    ax.set_ylim(subfieldXY[1], subfieldXY[1] + subfieldWH[1])

    if subfieldXY == [0.0, 0.0] and subfieldWH == [1.0, 1.0]:
        # no ticks for the full field
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        # show extent for a subfield
        ax.set_xticks([subfieldXY[0], subfieldXY[0] + subfieldWH[0]])
        ax.set_yticks([subfieldXY[1], subfieldXY[1] + subfieldWH[1]])

    # set the background colour
    ax.set_facecolor(backgroundColour)
