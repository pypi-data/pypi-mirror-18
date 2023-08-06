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

import functools

from dfract.datastream import Datastream
from dfract.serialization import native2serialized
from dfract.utils import b64encode
from tornado import gen


class MuxDatastream(Datastream):
    """
    Send predefined event at predefined interval.
    """
    _FUNCTIONAL = True

    def __init__(self, **kwargs):
        self._datastreams = kwargs

        super(MuxDatastream, self).__init__()

        for d in self._datastreams.values():
            d._datastream_streamactivity_eh.add_on_add(self._datastream_streamactivity_eh.on_add)
            d._datastream_streamactivity_eh.add_on_remove(self._datastream_streamactivity_eh.on_remove)

    def keys(self, *args, **kwargs):
        return sorted(
            functools.reduce(lambda b, d: b.union(d.keys(*args, **kwargs)), self._datastreams.values(), set()))

    def get(self, *args, **kwargs):
        mode = kwargs.get("typesystem", "native")
        r = {}
        kwargs["typesystem"] = "native"
        for d in self._datastreams.items():
            r[d[0]] = d[1].get(*args, **kwargs)

        if mode == "native":
            return r
        elif mode == "serialized":
            r = native2serialized(r)[1]
            return r
        elif mode in ["b64serialised", "b64serialized"]:
            r = b64encode(native2serialized(r)[1])
            return r
        else:
            raise ValueError

    @gen.coroutine
    def _generator_coroutine(self):
        yield [d._generator_coroutine() for d in self._datastreams.values()]

        # FIXME : Implement signature


__call__ = MuxDatastream
