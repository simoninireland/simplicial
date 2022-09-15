# Read and write simplicial complexes as JSON objects
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

import json
from typing import Any, Union
from simplicial import SimplicialComplex, Simplex

json_simplicial_version = 0.1


class JSONSimplicialComplexEncoder(json.JSONEncoder):

    """JSON is a portable format for exchanging simplicial complexes. The
    encoding represents the complex as a JSON object consistting of three
    top-level fields:

    * "__simplicialcomplex__": a type marker, always True
    * "__version__": the JSON encoding version in use
    * "simplices": a list of simplices

    Each entry in the "simplices" list is a simplex, with simplices
    appearing in ascending order (0-simplices followed by 1-simplices
    and so forth). Note that this implices that, for any simplex, its
    faces (if any) will already have been encountered.

    Each simplex is a JSON object with three fields:

    * "id": the unique identifier of the simplex
    * "faces": a list of the names of the faces of the simplex
    * "attributes": a JSON object reprsenting the attributes hash
      of the simplex

    Note that because of the restrictions of JSON the encoding of attributes
    may not preserve their (Python) types. In particular, Python tuples will
    become JSON arrays, and will be reconstructed as such when the complex
    is read back in.
    """

    def json_simplex(self, c: SimplicialComplex, s: Simplex):
        """Return a simplex as an object suitable for writing out as JSON.

        :param c: the complex
        :param s: the simplex
        :returns: an object that can be stored as JSON"""
        return dict(id=s,
                    faces=list(c.faces(s)),
                    attributes=c[s])

    def default(self, o: SimplicialComplex):
        """Encode a simplicial complex.

        :param o: the object to encode
        :returns: a JSON encoding of the complex"""
        if isinstance(o, SimplicialComplex):
            # a simplicial complex, create an array to hold the simplices
            json_simplices = []

            # expand each simplex
            for s in o.simplices():
                json_simplices.append(self.json_simplex(o, s))

            # wrap-up the simplices in a suitable wrapper
            rep = dict()
            rep['__simplicialcomplex__'] = True
            rep['__version__'] = json_simplicial_version
            rep['simplices'] = json_simplices

            # return the wrapper as the encoding for the complex
            return rep
        else:
            # not something we can handle, pass through
            return json.JSONEncoder.default(self, o)


def as_json(c: SimplicialComplex) -> str:
    """Return a JSON string representation of a simplicial complex.

    :param c: the complex
    :returns: a JSON representation of the complex"""
    return json.dumps(c,
                      indent=4,
                      cls=JSONSimplicialComplexEncoder)


def as_simplicial_complex(o: Any) -> Union[SimplicialComplex, Any]:
    """Decode a given dict as a simplicial complex. The most common usage
    for this function is as an object hook in the :meth:`json.loads` and
    :meth:`json.load` methods, for example:

    .. code-block:: python

       json.load(fp, object_hook=simplicial.as_simplicial_complex)

    :param o: the dict
    :returns: a simplicial complex"""
    if (('__simplicialcomplex__' in o.keys()) and
        ('__version__' in o.keys()) and
        (o['__version__'] == json_simplicial_version)):

        # create a new complex
        c = SimplicialComplex()

        # import all the simplices into the complex
        for s in o['simplices']:
            c.addSimplex(id=s['id'],
                         fs=s['faces'],
                         attr=s['attributes'])

        # return the complex
        return c
    else:
        # not one of ours, return it
        return o


def write_json(c: SimplicialComplex, path: str):
    """Write a complex in JSON format to the named file.

    :param c: the complex
    :param path: path to the file"""

    with open(path, 'w') as f:
        f.write(as_json(c))


def read_json(path: str) -> Union[SimplicialComplex, Any]:
    """Read a complex in JSON format from the name file.

    :param path: the file to read
    :returns: a complex"""
    with open(path, 'r') as f:
        c = json.load(f, object_hook=as_simplicial_complex)
    return c
