# ############################################################################
# |W|I|D|E|I|O|L|T|D|W|I|D|E|I|O|L|T|D|W|I|D|E|I|O|L|T|D|W|I|D|E|I|O|L|T|D|
# Copyright (c) 2016 - WIDE IO LTD
# 
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without 
# restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# |D|O|N|O|T|R|E|M|O|V|E|!|D|O|N|O|T|R|E|M|O|V|E|!|D|O|N|O|T|R|E|M|O|V|E|!|
# ############################################################################


# NOTE:
# DFract does not plan to handle serialization intrisically as resolving good
# serialization is a problem that is more general than just DFRACT
# issues at this stage but we think it may be useful to have this as
# a placeholder for future reference

import bz2
import json
import numpy
import os
import sys
import tempfile
from PIL import Image
from decimal import Decimal

if sys.version[0] == "2":
    from cStringIO import StringIO
else:
    from io import StringIO

import h5py
from iso8601ddb import iso8601

if sys.version[0] == "2":
    DIRECT_TYPES = [int, float, str, unicode]
else:
    DIRECT_TYPES = [int, float, str]

def _get_autoserialized(g):
    def ng(k, typesystem="native"):
        if typesystem in ["serialised", "serialized"]:
            return native2serialized(g(k, "native"))[1]
        if typesystem in ["b64serialised", "b64serialized"]:
            return b64encode(native2serialized(g(k, "native"))[1])

        return g(k, typesystem)

    return ng


def autoserialize_get(e0, get):
    return _get_autoserialized(get), native2serialized(e0)[0]


def parsedate(cdate):
    # iso8601.datetime(*re.match("(\d{4})-(\d{2})-(\d{2})(?:(T| ))(\d{2})\:(\d{2})\:(\d{2})(?:([+-](\d{2})\:(\d{2}))", cdate).groups()[1:])
    # cg1 = re.match("(\d{4})-(\d{2})-(\d{2})(?:(T| ))(\d{2})\:(\d{2})\:(\d{2})", cdate).groups()[1:]
    # return iso8601.datetime(*cg1)
    return iso8601.datetime(Decimal(0)).parse_iso8601(cdate)  # <FIXME: This does not seem right (check iso8601ddb)

def dump_numpy_array_hdf5(data):
    df, tmpfile = tempfile.mkstemp('hdf5')
    with h5py.File(tmpfile, libver='earliest') as f:
        f['static'] = data
    buf = open(tmpfile, "rb").read()
    os.unlink(tmpfile)
    return bz2.compress(buf)


def read_numpy_array_hdf5(data):
    df, tmpfile = tempfile.mkstemp('hdf5')
    open(tmpfile, "wb").write(bz2.decompress(data))
    with h5py.File(tmpfile, libver='latest') as f:
        data = numpy.asarray(f['static']).copy('C')
    os.unlink(tmpfile)
    return data


def dump_numpy_array_npz(data):
    f = StringIO()
    numpy.savez_compressed(f, x=data)
    f.seek(0)
    return f.read()


def read_numpy_array_npz(data):
    return numpy.load(StringIO(data))['x']


def dump_numpy_png_image(data):
    f = StringIO()
    # print data.dtype, data.shape
    if len(data.shape) == 2:
        data = data[:, :, numpy.newaxis]
    if data.shape[2] == 1:
        data = data.repeat(3, axis=2)
    img = Image.fromarray(data)
    img.save(f, format="PNG")
    f.seek(0)
    return f.read()


def read_numpy_png_image(data):
    return numpy.asarray(Image.open(StringIO(data)))


from dfract.utils import b64decode, b64encode

def smj_dumpx(x):
    """
    Transforms Python objects into objects that should be JSON serializable.
    """
    tx = type(x)
    if tx in [list, tuple]:
        return [smj_dumpx(e) for e in x]
    elif tx in [dict]:
        return dict([(e[0], smj_dumpx(e[1])) for e in x.items()])
    elif tx in [int, float, str]:
        return x
    else:
        t0n = tx.__name__
        t0m = tx.__module__
        tt = t0m + "." + t0n

        if tt in NAIVE_NATIVESERIALIZATION_MAP:
            t = native2serialized(x)
        else:
            raise ValueError(x)
        return {"$nativetype": t[0][0],
                "$serialization": t[0][1], "$static": b64encode(t[1])}


def smj_loadx(x):
    """
    Transforms objects that have been transformed to be JSON serializable into fully valid objects.
    """
    tx = type(x)
    if tx in DIRECT_TYPES:
        return x
    elif tx in [dict] and not "$serialization" in x:
        return dict([(e[0], smj_loadx(e[1])) for e in x.items()])
    elif tx in [list] and not "$serialization" in x:
        return [smj_loadx(e) for e in x]
    elif "$serialization" in x:
        return serialized2native(b64decode(x["$static"]), (x["$nativetype"], x["$serialization"]))
    else:
        raise ValueError((x, tx))


NAIVE_NATIVESERIALIZATION_MAP = {
    '__builtin__.NoneType': [
        ('xml:reference', lambda x: "null", lambda x: None, lambda x: True)
    ],
    '__builtin__.bool': [
        ('xml:boolean', lambda x: ("true" if x else "false"), lambda x: (x.lower() == "true"), lambda x: True)
    ],
    '__builtin__.str': [
        ('xml:string', lambda x: x, lambda x: x, lambda x: True)
    ],
    '__builtin__.unicode': [
        ('xml:string', lambda x: x, lambda x: x, lambda x: True)
    ],
    '__builtin__.int': [
        ('xml:int', str, int, lambda x: True)
    ],
    '__builtin__.float': [
        ('xml:float', str, float, lambda x: True)
    ],
    'numpy.float64': [
        ('xml:float', str, float, lambda x: True)
    ],
    '__builtin__.list': [
        ('mimetype:application/json+mimejson', lambda x: json.dumps(smj_dumpx(x)), lambda x: smj_loadx(json.loads(x)),
         lambda x: True)
    ],
    '__builtin__.dict': [
        ('mimetype:application/json+mimejson', lambda x: json.dumps(smj_dumpx(x)), lambda x: smj_loadx(json.loads(x)),
         lambda x: True)
    ],
    'builtins.NoneType': [
        ('xml:reference', lambda x: "null", lambda x: None, lambda x: True)
    ],
    'builtins.bool': [
        ('xml:boolean', lambda x: ("true" if x else "false"), lambda x: (x.lower() == "true"), lambda x: True)
    ],
    'builtins.str': [
        ('xml:string', lambda x: x, lambda x: x, lambda x: True)
    ],
    'builtins.int': [
        ('xml:int', str, int, lambda x: True)
    ],
    'builtins.float': [
        ('xml:float', str, float, lambda x: True)
    ],
    'builtins.list': [
        ('mimetype:application/json+mimejson', lambda x: json.dumps(smj_dumpx(x)), lambda x: smj_loadx(json.loads(x)),
         lambda x: True)
    ],
    'builtins.dict': [
        ('mimetype:application/json+mimejson', lambda x: json.dumps(smj_dumpx(x)), lambda x: smj_loadx(json.loads(x)),
         lambda x: True)
    ],
    'decimal.Decimal': [
        ('xml:decimal', str, Decimal, lambda x: True)
    ],
    'iso8601ddb.iso8601.datetime': [
        ('xml:datetime', str, parsedate, lambda x: True)
    ],
    'datetime.datetime': [
        ('xml:datetime', str, parsedate, lambda x: True)
    ],
    'numpy.ndarray': [
        ('mimetype:image/png', dump_numpy_png_image, read_numpy_png_image,
         lambda x: (len(x.shape) == 3 and x.shape[-1] in [1, 3] and x.dtype == numpy.uint8)),
        ('mimetype:image/jpeg', None, read_numpy_png_image,
         lambda x: False),
        ('mimetype:application/x-hdf;subtype=bag', dump_numpy_array_hdf5, read_numpy_array_hdf5, lambda x: True),
        ('mimetype:application/x-npz', dump_numpy_array_npz, read_numpy_array_npz, lambda x: True)
    ]
}

if sys.version[0] == '2':
    NAIVE_NATIVESERIALIZATION_MAP['__builtin__.long'] = [
                                                            ('xml:integer', str, long, lambda x: True)
                                                        ],


def serialized2native(v0, typeinfo=None):
    if typeinfo is None:
        if isinstance(v0, tuple):
            typeinfo, v0 = v0
    nativetype, mimetype = typeinfo
    if not nativetype.startswith("python:"):
        nativetype = None
    if nativetype and len(nativetype):
        nativetype = nativetype[7:]
        for c in NAIVE_NATIVESERIALIZATION_MAP[nativetype]:
            if c[0] == mimetype:
                return c[2](v0)

    for xt in NAIVE_NATIVESERIALIZATION_MAP.items():
        for c in xt[1]:
            if c[0] == mimetype:
                try:
                    return c[2](v0)
                except Exception:
                    pass

    raise ValueError(mimetype)


def native2serialized(e0):
    t0 = type(e0)
    t0n = t0.__name__
    t0m = t0.__module__
    t = t0m + "." + t0n
    res = None
    for cvt in NAIVE_NATIVESERIALIZATION_MAP.get(t, []):
        if not cvt[3](e0):
            continue
        try:
            ser = cvt[1](e0)
            res = (("python:" + t, cvt[0]), ser)

        except Exception as e:
            # traceback.print_tb(e)
            raise
            continue
        # assert(isinstance(ser, str))
        # import serpent
        # serpent.loads(serpent.dumps(dict(X=ser)))
        break

    if res is None:
        ## attempt other serialization (marshal ?)
        # NOTE: NOT YET IMPLEMENTED
        sys.stderr.write(repr(type(e0)) + "\n")
        sys.stderr.write(repr(e0) + "\n")
        raise ValueError

    return res
