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
import os

import Pyro4
import requests
from dfract.cache_utils import lru_cache
from dfract.dataset import Dataset
from dfract.serialization import serialized2native
    # native2serialized


# import dfract.config as config


def L3Proxy(url):
    return Pyro4.Proxy(url)


class L4Proxy(Dataset):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.args = args
        self.kwargs = kwargs
        self.s = requests.Session()
        self._ik = 0

    @lru_cache
    def _get_kpage(self, i):
        r = requests.Request("GET", self.url, data={'page': i, 'perpage': 20}, *self.args, **self.kwargs).json()
        resp = self.s.send(r)
        return resp.json()

    def _get_key(self, i):
        pi, ci = i / 20, i % 20
        return [ci]

    def keys(self):
        self._ik = 0
        while True:
            yield self._get_keys(self._ik)

    # def _typeinfo_from_headers(self, x):
    #    return resp.headers['Content-Type']

    @lru_cache
    def get(self, k):
        r = requests.Request("GET", os.path.join(self.url, k), data={}, *self.args, **self.kwargs).json()
        resp = self.s.send(r)
        # check mimetype
        typeinfo = self._typeinfo_from_headers(resp)
        serialized2native(resp, typeinfo=typeinfo)


def GenProxy(url):
    if url.lower().startswith("pyro"):
        return L3Proxy(url)
    else:
        return L4Proxy(url)


__call__ = L3Proxy
