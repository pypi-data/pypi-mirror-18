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

from dfract import autoimp


from dfract.datastream import Datastream
from dfract.serialization import native2serialized
from dfract.utils import sha256, b64encode

from tornado import gen


# FIXME: There is no usage _fifo in this datastream...

class PyTransformDatastream(Datastream):
    """
    Use this dataset to transform any dataset in a new one.
    Thanks to the magic of eval and autoimports you can use any python module you want.
    """
    _FUNCTIONAL = True

    def __init__(self, transform, datastream):
        self.transform = transform
        self._datastream = datastream
        self._e0 = None
        super(PyTransformDatastream, self).__init__()
        self._datastream._datastream_streamactivity_eh.add_on_add(self._datastream_streamactivity_eh.on_add)
        self._datastream._datastream_streamactivity_eh.add_on_remove(self._datastream_streamactivity_eh.on_remove)

    def keys(self, *args, **kwargs):
        return self._datastream.keys(*args, **kwargs)

    def get(self, *args, **kwargs):
        mode = kwargs.get("typesystem", "native")
        if mode == "native":
            x = self._datastream.get(*args, **kwargs)
            r = eval(self.transform, autoimp.__dict__, locals())
            if self._e0 is None:
                self._e0 = r
            return r
        elif mode == "serialized":
            kwargs["typesystem"] = "native"
            r = self.get(*args, **kwargs)
            r = native2serialized(r)[1]
            return r
        elif mode in ["b64serialised", "b64serialized"]:
            kwargs["typesystem"] = "native"
            r = self.get(*args, **kwargs)
            r = b64encode(native2serialized(r)[1])
            return r
        else:
            raise ValueError

    @gen.coroutine
    def _generator_coroutine(self):
        yield self._datastream._generator_coroutine()

    def signature(self):
        return sha256("pytransform(%s, %s)" % (self.transform, self._datastream.signature())).hexdigest()

__call__ = PyTransformDatastream