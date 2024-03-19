# Euler characteristic integration
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

import copy
from simplicial import SimplicialComplex, SimplicialFunction


class EulerIntegrator:
    """Integration for simplicial complexes.

    The :term:`Euler characteristic` is a global value defined over
    simplicial complexes. It can also be used as the basis for
    integration, by generating sub-complexes and summing the
    characteristic over them. By choosing a suitable collection of
    sub-complexes, different problems can be represented as integrals
    of this kind.

    The metric should be a non-negative integer. The metric assignment
    has to be monotone with respect to simplex order: the metric
    associated with a simplex `s` should be greater than or equal to
    the values associated with all simplices in the closure of `s`,
    i.e., all faces of `s`, or faces of those faces, and so
    forth. This isn't (currently) checked, but the integration will
    behave unpredictably if the condition doesn't hold.

    Metrics can be defined using any :class:`SimplicialFunction`.

    """

    def levelSet(self, c: SimplicialComplex, sf: SimplicialFunction[int], l: int) -> SimplicialComplex:
        """Form the level set of the complex c at the value l. The level set
        is the sub-complex for which the metrics associated with all simplices
        are greater than l. This is guaranteed to be a valid simplicial
        complex as long as the metric respects the orders of simplices.

        This method is destructive, in that the complex c is reduced to the level
        set. Be sure to copy the complex first if it's going to be needed later.

        :param c: the complex
        :param sf: the metric
        :param l: the level
        :returns: the sub-complex at level l"""

        # extract all the basis simplices whose associated metric
        # is greater than l
        bs = c.allSimplices(lambda c, s: c.orderOf(s) == 0 and sf(s) > l)

        # create a sub-complex at this level
        return c.restrictBasisTo(bs)


    def integrate(self, c: SimplicialComplex, sf: SimplicialFunction[int]) -> int:
        """Perform an integration of the Euler characteristic across the
        simplicial complex c under the integrator's metric.

        :param c: the complex
        :param sf: the metric
        :returns: the value of the integral"""

        # the initial level set is the whole complex, and we take a copy
        # because levelSet() is destructive
        d = copy.deepcopy(c)

        # compute maximum "height"
        maxHeight = max([sf(s) for s in d.simplices()])

        # perform the integration over the level sets
        levelSet = d
        a = 0
        for l in range(maxHeight):
            # compute the Euler characteristic of the level set
            levelSet = self.levelSet(levelSet, sf, l)
            chi = levelSet.eulerCharacteristic()
            #print('level {level}, chi = {chi}'.format(level = l, chi = chi))

            # add to the integral
            a += chi

        # return the accumulated integral
        return a
