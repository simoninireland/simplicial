# Tests of simplicial utilities
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

import unittest
from simplicial import *


# ----------  Isomorphisms ----------

class IsomorphismTests(unittest.TestCase):

    def setUp(self):
        self._iso = Isomorphism()


    def testOneValue(self):
        '''Test we can store and retrieve a single value, forward and backward.'''
        self._iso['a'] = 12
        self.assertEqual(self._iso['a'], 12)
        self.assertEqual(self._iso.reverse[12], 'a')


    def testTwoValues(self):
        '''Test we can store and retrieve two values, forward and backward.'''
        self._iso['a'] = 12
        self._iso['b'] = 24
        self.assertEqual(self._iso['a'], 12)
        self.assertEqual(self._iso.reverse[12], 'a')
        self.assertEqual(self._iso['b'], 24)
        self.assertEqual(self._iso.reverse[24], 'b')


    def testKeys(self):
        '''Test we get the right key enumerations.'''
        self._iso['a'] = 12
        self._iso['b'] = 24
        self.assertCountEqual(['a', 'b'], self._iso.keys())
        self.assertCountEqual([12, 24], self._iso.reverse.keys())


    def testValues(self):
        '''Test we get the right value enumerations.'''
        self._iso['a'] = 12
        self._iso['b'] = 24
        self.assertCountEqual(['a', 'b'], self._iso.reverse.values())
        self.assertCountEqual([12, 24], self._iso.values())


    def testDelete(self):
        '''Test deletion deletes both ways.'''
        self._iso['a'] = 12
        self._iso['b'] = 24

        del self._iso['a']
        self.assertCountEqual(['b'], self._iso.keys())
        self.assertCountEqual([24], self._iso.reverse.keys())


    def testReverseDelete(self):
        '''Test deletion from the reverse deletes from the forward.'''
        self._iso['a'] = 12
        self._iso['b'] = 24

        del self._iso.reverse[12]
        self.assertCountEqual(['b'], self._iso.keys())
        self.assertCountEqual([24], self._iso.reverse.keys())


    def testIso(self):
        '''Test that reversing the reverse works as identity.'''
        self._iso['a'] = 12
        self._iso['b'] = 24

        self.assertCountEqual( self._iso.keys(), self._iso.reverse.reverse.keys())
        self.assertCountEqual(self._iso.values(), self._iso.reverse.reverse.values())


    def testInitialData(self):
        '''Test we can insert initial data.'''
        initial = dict(a=12, b=24)
        self._iso = Isomorphism(initial)

        self.assertEqual(self._iso['a'], 12)
        self.assertEqual(self._iso.reverse[12], 'a')
        self.assertEqual(self._iso['b'], 24)
        self.assertEqual(self._iso.reverse[24], 'b')


    def testDuplicateKey(self):
        '''Test that duplicate keys are detected.'''
        self._iso['a'] = 12
        with self.assertRaises(KeyError):
            self._iso['a'] = 24


    def testDuplicateValue(self):
        '''Test that duplicate values are detected.'''
        self._iso['a'] = 12
        with self.assertRaises(KeyError):
            self._iso['b'] = 12


    def testDuplicateInitial(self):
        '''Test that duplicate values in initial data are detected (there can't be duplicate keys)'''
        with self.assertRaises(KeyError):
            Isomorphism(dict(a=12, b=12))


if __name__ == '__main__':
    unittest.main()
