# Euler characteristic integration
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

import copy
from simplicial import SimplicialComplex, Simplex


class EulerIntegrator:
    """Integration for simplicial complexes.

    The :term:`Euler characteristic` is a global value defined over
    simplicial complexes. It can also be used as the basis for
    integration, by generating sub-complexes and summing the
    characteristic over them. By choosing a suitable collection of
    sub-complexes, different problems can be represented as integrals
    of this kind.

    The default implementation integrates using the value of a
    selected attribute of simplices, which should contain a
    number. Overriding the :meth:`metric` method generates different
    metrics.

     The metric should be a non-negative number. The metric assignment
     has to be monotone with respect to simplex order: the metric
     associated with a simplex `s` should be greater than or equal to
     the values associated with all simplices in the closure of `s`,
     i.e., all faces of `s`, or faces of those faces, and so
     forth. This isn't (currently) checked, but the integration will
     behave unpredictably if the condition doesn't hold.

    :param a: the attribute on simplices defining the metric to integrate against
    :param default_value: the default value if the attribute is missing (defaults to 0)

    """

    def __init__(self, a: str = None, default_value: int = 0):
        self._attribute = a
        self._defaultValue = 0

    def metric(self, c: SimplicialComplex, s: Simplex):
        """Return the metric for the given simplex. The default reads the value
        of the attribute given when the integrator was created: if the simplex
        has no such attribute then the metric is 0.

        :param c: the complex
        :param s: the simplex
        :returns: the metric"""
        if self._attribute in c[s].keys():
            return c[s][self._attribute]
        else:
            return self._defaultValue

    def levelSet(self, c: SimplicialComplex, l: int) -> SimplicialComplex:
        """Form the level set of the complex c at the value l. The level set
        is the sub-complex for which the metrics associated with all simplices
        are greater than l. This is guaranteed to be a valid simplicial
        complex as long as the metric respects the orders of simplices.

        This method is destructive, in that the complex c is reduced to the level
        set. Be sure to copy the complex first if it's going to be needed later.

        :param c: the complex
        :param l: the level
        :returns: the sub-complex at level l"""

        # extract all the basis simplices whose associated metric
        # is greater than l
        bs = c.allSimplices(lambda c, s: c.orderOf(s) == 0 and self.metric(c, s) > l)

        # create a sub-complex at this level
        return c.restrictBasisTo(bs)

    def integrate(self, c: SimplicialComplex) -> int:
        """Perform an integration of the Euler characteristic across the
        simplicial complex c under the integrator's metric.

        :param c: the complex
        :returns: the value of the integral"""

        # the initial level set is the whole complex, and we take a copy
        # because levelSet() is destructive
        levelSet = copy.deepcopy(c)

        # compute maximum "height"
        maxHeight = max([self.metric(levelSet, s) for s in levelSet.simplices()])

        # perform the integration over the level sets
        a = 0
        for l in range(maxHeight):
            # compute the Euler characteristic of the level set
            chi = levelSet.eulerCharacteristic()
            #print('level {level}, chi = {chi}'.format(level = l, chi = chi))

            # add to the integral
            a += chi

            # form the next level set from this one
            levelSet = self.levelSet(levelSet, l)

        # return the accumulated integral
        return a
