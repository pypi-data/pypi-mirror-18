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
import re
import sys

from .dataset import Dataset
from .datastream import Datastream

if sys.version[0] == '2':
    def iter_next(iter):
        return iter.next()
else:
    def iter_next(iter):
        return iter.__next__()

class IRange:
    """
    Provide a range between two range of keys involving and integer.
    """

    def __init__(self, si, se, re_key=r"(\d+)", format=None):
        """
        Creates a new interger range.
        :param si: start index
        :param se: end index
        :param re_key: regular expression allowing to d
        :param format: if re_key uses .* then this optional
        """
        self._re_key = re_key
        self._format = format
        self.si = int(re.match(self._re_key, si).groups()[0])
        self.se = int(re.match(self._re_key, se).groups()[0])

    def __contains__(self, x):
        sx = self.decode(x)
        return (sx >= self.si) and (sx < self.se)

    def decode(self, x):
        return int(re.match(self._re_key, x).groups()[0])

    def encode(self, x):
        return self._re_key.replace(r'(\d+)', str(x))

    def __iter__(self):
        for i in range(self.si, self.se):
            yield self.encode(i)


class MRange:
    """
    Multidimentional mrange when multiple ranges are involed.
    """

    def __init__(self, ranges, _re_key="\((\d+),(\d+)\)", format=None):
        """
        Creates a new multidimentional range.
        (Based on a list of enums/ ranges)

        :param ranges: a list of enums ranges
        :param _re_key: regular expression identifying each of the group "(?p1(\d+))"
        :param _format:
        """
        self._ranges = ranges
        self._re_key = _re_key
        self._format = format

    def decode(self, x, i):
        return map(int, re.match(self._re_key, x).groups())

    def encode(self, x, i):
        def get_next_sub():
            for i in j:
                yield str(i)

        return re.sub("@@@@", get_next_sub, self._re_key.replace(r'(\d+)', "@@@@"))

    def __contains__(self, x):
        dx = self.decode(x)
        return reduce(lambda a, b: a and (b[1] in b[0]), zip(self._ranges, dx), True)

    def __iter__(self):
        iters = [ iter(r) for r in self._ranges ]
        pos = [iter_next(i) for i in iters]
        while True:
            yield self.encode(pos)
            c = -1
            while True:
                try:
                    pos[c] = iters[c].next()
                    break
                except:
                    iters[c] = iter(self._ranges[c])
                    pos[c] = iters[c].next()



class MBall:
    """
    Multidimensional ball.
    # think geo deta
    """
    def __init__(self, center, distance):
        pass

    
class MUnion:
    """
    Union of one or many elements
    """
    pass

class DatasetAggregateManager(Dataset):
    """
    Aggregates are datasets (even for datastreams!) that provide various statistics on
    subset of the collections of all combinations of keys on the dataset.

    The subset must be computed by the function "key_transform".
    Aggregate contain also special keys such as "p:whole()".
    Aggregate keys may also contain additional parameter for the AggregateManager.
    
    For instance, it should be possible to implement an aggregate maneger that provide arbitrary percentiles
    value on various subsets of the datasets.

    We want all Aggregate keys to obey to a framework "logic" so that it is easy to ask for any 
    aggregates on any dataset.

    The aggregates are implemented in any of the language supported by dfract and receive static from the datasets
    and datastreams in an unserialised format. It is the responsibility of the dfract framework to ensure that the
    static provided by the static source will be compatible with the aggregate and checks based on metadata and other
    static must be performed as soon as possible.
    
    Aggregate are often computed on the entire datasets, but more sophisticated space definitionvare possible.
    Aggregates are meant to exist has elements that can be computed online or why a "map-reduce" scheme.
    
    NOTE: It is not a requirement for aggregates to be available for all possible partition of the key space.
    
    The convention used would be to provide an expression for a generator that can be understood by
    the dfract aggregate framework. As keys are string they need to be parsable.


    Many aggregates function generally in a simple way they compute a function that bin keys together.
    And compute a function of all the element that arrive in the same bin.
    As a  consequence of this there is no need to recompute the aggregate if the bins used to aggregate
    the keys have not seen their content change.

    Aggregates for datastreams are naturally attached to time, and therefore are considered as new datastreams.

    'p:whole()'/':' # all the keys
    p:slice(minkey,maxkey) / 'minkey:maxkey' : interval/slice
    #:,: multidimensional indexes
    #[a,b,c]  explicit enumeration of values
    # ALL-[a,b,c] # substraction of elements from the set considered
    # : should be replaced by ALL[:]


    we expect most aggregate to create pyramids on linear space.
    """
    WHOLE = "p:whole()"
    NONE = "p:none()"

    def __init__(self):
        super(DataSet, self).__init__()


    def _slice_key(self, k1, k2):
        return "p:slice(%s,%s)" % (k1, k2)

    def _enum_key(self, k1, k2):
        return "p:slice(%s,%s)" % (k1, k2)

    def _dataset_keys(self):
        return self._dataset.keys()


    def _register_on_update(self):
        dfract = self._find_dfract()
        dfract._callback_create_for_object.register_on_update(self._id, "on_update")

    def on_update(self, x):
        pass

    def key_transform(self, keys_generator):
        return [ "p:whole()" ]

    def keys(self):
        return self.key_transform(self._dataset_keys)

    
class DatastreamAggregateManager(Datastream):
    """
    Datastream aggregate and models are different from the dataset part. 
    While dataset aggregate focus on aggregating on invariant space definition.
    Datastream aggregate are focus on dynamic aggregate that change over time
    in a same way as the underlying datastream changes.
    
    The datastream aggregate rely on the push notifications,
    and hence are meant to be indicative and not necessarily accurate.
    """

    def __init__(self):
        super(Datastream, self).__init__()


    def _slice_key(self, k1, k2):
        return "p:slice(%s,%s)" % (k1, k2)

    def _enum_key(self, k1, k2):
        return "p:slice(%s,%s)" % (k1, k2)

    def _dataset_keys(self):
        return self._dataset.keys()


    def _register_on_update(self):
        dfract = self._find_dfract()
        dfract._callback_create_for_object.register_on_update(self._id, "on_update")

    def on_update(self, x):
        pass

    def key_transform(self, keys_generator):
        return [ "p:whole()" ]

    def keys(self):
        return self.key_transform(self._dataset_keys)
