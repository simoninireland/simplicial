# Drawing routine  for Euler integrals
#
# Copyright (c) 2024 Simon Dobson
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

from copy import deepcopy
from simplicial import SimplicialComplex, Embedding, SimplicialFunction
from simplicial.drawing import patchesForComplex
from matplotlib.colors import BoundaryNorm
from matplotlib.cm import ScalarMappable
from matplotlib import colormaps
import matplotlib.pyplot as plt


def drawEulerIntegral(c: SimplicialComplex, em: Embedding,
                      sf: SimplicialFunction[int],
                      axs = None,
                      backgroundColour = '0.95',
                      subfieldXY = None, subfieldWH = None,
                      simplexSize = 0.02,
                      showLevelSets = True,
                      showEulerCharacteristics = False,
                      eulerCharacteristicsColour ='k', eulerCharacteristicsFontSize = 'small',
                      showMetrics = False,
                      metricsColour = 'k', metricsFontSize = 'small',
                      cax = None, cmap = None):
    '''Draw the sequence of subcomplexes induced by the Euler integral
    over the given complex, drawn using the embedding.

    There need to be one more set of axes provided than the maximum
    height of the complex, to allow for the base complex to be drawn
    as well.

    At present we only deal with simplices of order 2 and less.

    :param c: the complex
    :param em: embedding providing the positions of the 0-simplices
    :param sf: the metric
    :param axs: (optional) the axes to draw into (defaults to create a new figure)
    :param backgroundColour: the background colour for the field (default '0.95')
    :param subfieldXY: the bottom-left corner of the sub-field to draw (default all)
    :param subfieldWH: the width and heigh of the sub-field to draw (default all)
    :param simplexSize: the size of the node (0-simplex) markers
    :param showLevelSets: show the level set of each plot (defaul True)
    :param showEulerCharacteristics: show the Euler characteristics of each level set (default False)
    :param eulerCharacteristicsColour: annotation colour (default black)
    :param eulerCharacteristicsFontSize: annotation font size (default 'small')
    :param showMetrics: show metric at each 0-simplex (default False)
    :param metricsColour: colour for metrics (default black)
    :param metricsFontSize: font size for metrics (default 'small')
    :param cax: axes to draw colourbar into (defaults to None)
    :param cmap: colourmap (defaults to matplotlib.colormaps['Set1'])
    '''
    maxHeight = max([sf[s] for s in c.simplicesOfOrder(0)])

    # fill out defaults
    if subfieldXY is None:
        subfieldXY = [0.0, 0.0]
    if subfieldWH is None:
        subfieldWH = [1.0 - subfieldXY[0], 1.0 - subfieldXY[1]]
    if axs is None:
        # default is a side-by-side plot with a narrow colourbar on the right
        plotWidth = 1.0 - 0.02 / (maxHeight + 1)
        _, axs = plt.subplots(nrows=1, ncols=(maxHeight + 1) + 1,
                              width_ratios=[plotWidth] * (maxHeight + 1) + [0.02],
                              figsize=(2 * (maxHeight + 1), 2))
        cax = axs[-1]
    else:
        # sanity-check that we have enough axes
        needAxes = (maxHeight + 1) + (1 if cax is not None else 0)
        if len(axs) < needAxes:
            raise ValueError(f'Not enough axes to draw integral ($h_{max} = {maxHeight}$)')
    if cmap is None:
        cmap = colormaps['Set1']

    # plot each level set
    h = -1
    for i in range(maxHeight + 1):
        ax = axs[i]
        bs = [s for s in c.simplicesOfOrder(0) if sf(s) > h]
        levelSet = deepcopy(c).restrictBasisTo(bs)
        pcs = patchesForComplex(levelSet, em, sf, cmap, simplexSize)
        for pc in pcs:
            ax.add_collection(pc)

        # add metric
        if showMetrics:
            for s in c.simplicesOfOrder(0):
                ax.annotate(sf[s],
                            xy=em[s],
                            xytext=(-simplexSize, -simplexSize), textcoords='offset pixels',
                            color=metricsColour, fontsize=metricsFontSize)

        # add level set
        if showLevelSets:
            if h == -1:
                ax.set_title(f'Base')
            else:
                ax.set_title('$\\{ h > ' + f'{h}' + ' \\}$')

        # add Euler characteristic
        if showEulerCharacteristics:
            chi = levelSet.eulerCharacteristic()
            if h > -1:
                chiString = '$\\chi(\\{ h > ' + f'{h}' + ' \\}) = ' + f'{chi}' + '$'
                ax.annotate(chiString,
                            (0.05, 0.05), xycoords='axes fraction',
                            color=eulerCharacteristicsColour, fontsize=eulerCharacteristicsFontSize)

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

        h += 1

    # draw the colourbar if requested
    if cax is not None:
        bounds = list(range(maxHeight + 1))
        norm = BoundaryNorm(bounds, maxHeight + 1)
        cbar = plt.colorbar(ScalarMappable(norm=norm, cmap=cmap),
                            location='right',
                            cax=cax,
                            ticks=[i + 0.49 for i in bounds[:-1]],
                            drawedges=True,
                            label='Target count',
                            format='{x:.0f}')
