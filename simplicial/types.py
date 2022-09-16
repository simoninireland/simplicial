# Helper types
#
# Copyright (C) 2017--2022 Simon Dobson
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

from typing import Dict, Callable, Union, Any


Simplex = Any                                   #: A simplex in a complex, which may be any object.
Attributes = Dict[str, Any]                     #: Attributes of a simplex, mapping strings to values.
Renaming = Union[Dict[Simplex, Simplex],
                 Callable[[Simplex], Simplex]]  #: A renaming of simplices, either a dict or a function.
