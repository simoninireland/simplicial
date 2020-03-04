# Eukler characteristic integration
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

import numpy
import copy
import itertools


class EulerIntegrator(object):
    """Integration for simplicial complexes.

    The :term:`Euler characteristic` is a global value defined over simplicial
    complexes. It can also be used as the basis for integration, by generating
    sub-complexes and summing the characteristic over them. By choosing a suitable
    collection of sub-complexes, different problems can be represented as
    integrals of this kind.

    """

    def eulerIntegral(self, observation_key='height'):
        """Perform an Euler integraton across a simplicial complex
        using the value of a particular attribute.

        :param c: the complex
        :param observation_key: the attribute to integrate over (defaults to 'height')"""

        # compute maximum "height"
        maxHeight = max([self[s][observation_key] for s in self.simplices()])

        # perform the integration over the level sets
        a = 0
        for s in xrange(maxHeight + 1):
            # form the level set
            # sd TODO: the level set is uniformly growing as s decreases, so we can optimise?
            cprime = copy.deepcopy(self)
            bs = cprime.allSimplices(lambda csp: self.orderOf(csp[1]) == 0 and
                                                 self[csp[1]][observation_key] > s)
            cprime.restrictBasisTo(bs)

            # compute the Euler characteristic of the level set
            chi = cprime.eulerCharacteristic()
            # print 'level {level}, chi = {chi}'.format(level = s, chi = chi)

            # add to the integral
            a = a + chi

        # return the accumulated integral
        return a
