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

import diskcache
import redis
from dfract.dataset import Dataset
from dfract.utils import sha256


#
class CacheDataset(Dataset):
    """
    This cache dataset implementation that uses REDIS or a diskcache

    To my knowledge, diskcache is not designed to support
    to concurrent access so it is assumed that no other
    process are accessing the diskcache.


    It is assumed that REDIS is config as an LRU CACHE.
    Otherwise rune LRU_CACHE
    """

    def __init__(self, dataset, mode="diskcache"):
        self._dataset = dataset
        self._mode = mode

        if mode == "diskcache":
            self._diskcache = diskcache.Cache('/tmp/cache-%s' % (str(self.signature())),
                                              size_limit=int(4e9),
                                              cull_limit=100000,
                                              eviction_policy=u'least-recently-used'
                                              )

            self._diskcache.size_limit = 4000000000
            self.get = self._get_diskcache
            self.keys = self._keys_diskcache
        elif mode == "redis":
            self._redis = redis.Client()
            self.get = self._get_redis
        else:
            raise ValueError
        super(CacheDataset, self).__init__()

    def config_redis(self):
        self._redis.command("CONFIG SET maxmemory 1gb")
        self._redis.command("CONFIG SET maxmemory-policy allkeys-lru")

    def _keys_diskcache(self, *args, **kwargs):
        if "/@keys" not in self._diskcache:
            self._diskcache.add("/@keys", self._dataset.keys(*args, **kwargs))
        return self._diskcache.get("/@keys")

    def _keys_redis(self, *args, **kwargs):
        raise NotImplemented

    def _get_diskcache(self, key, *args, **kwargs):
        if key not in self._diskcache:
            self._diskcache.add(key, self._dataset.get(key))
        return self._diskcache.get(key)

    def _get_redis(self, key, *args, **kwargs):
        raise NotImplemented

    def signature(self):
        return sha256("cache(%s, %s)" % (self._mode, self._dataset.signature())).hexdigest()


__call__ = CacheDataset
