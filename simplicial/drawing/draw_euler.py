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
from simplicial import SimplicialComplex, Embedding
from simplicial.drawing import patchesForComplex


def drawEulerIntegral(c: SimplicialComplex, em: Embedding,
                      axs,
                      attr = 'count', backgroundColour = '0.95',
                      subfieldXY = None, subfieldWH = None,
                      simplexColour = None, simplexSize = 0.02,
                      showLevelSets = True, showEulerCharacteristics = False):
    '''Draw the sequence of subcomplexes induced by the Euler integral
    over the given complex, drawn using the embedding.

    There need to be one more axes provided than the maximum height of the
    complex, to allow for the base.

    At present we only deal with simplices of order 2 and less.

    :param c: the complex
    :param em: embedding providing the positions of the 0-simplices
    :param axs: the axes to draw each level set into
    :param attr: the attribute holding the height information (default 'count')
    :param backgroundColour: the background colour for the field (default '0.95')
    :param subfieldXY: the bottom-left corner of the sub-field to draw (default all)
    :param subfieldWH: the width and heigh of the sub-field to draw (default all)
    :param simplexColour: simplex colours
    :param simplexSize: the size of the node (0-simplex) markers
    :param showLevelSets: show the level set of each plot (defaul True)
    :param showEulerCharacteristics: show trhe Euler characteristics of each level set (default False)

    '''

    # fill out defaults
    if subfieldXY is None:
        subfieldXY = [0.0, 0.0]
    if subfieldWH is None:
        subfieldWH = [1.0 - subfieldXY[0], 1.0 - subfieldXY[1]]

    # extract the maximum height and sanbitry-check the axes
    maxHeight = max([c[s][attr] for s in c.simplicesOfOrder(0)])
    if len(axs) < maxHeight + 1:
        raise ValueError(f'Not enough axes to draw integral ($h_{max} = {maxHeight}$)')

    # plot each level set
    h = -1
    for i in range(len(axs)):
        ax = axs[i]
        bs = [s for s in c.simplicesOfOrder(0) if c[s][attr] > h]
        levelSet = deepcopy(c).restrictBasisTo(bs)
        pcs = patchesForComplex(levelSet, em, simplexColour, simplexSize)
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
                            (0.05, 0.05), xycoords='axes fraction')

        h += 1
