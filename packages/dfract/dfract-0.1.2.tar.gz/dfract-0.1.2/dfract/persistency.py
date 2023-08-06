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
import copy
import itertools
import logging
import os
import shelve

import motor
import pymongo
from dfract import config
from tornado import gen


def _proto(expr):
    try:
        i = expr.index(":")
        return expr[:i]
    except ValueError:
        return ""


def _skip_proto(expr):
    try:
        i = expr.index(":")
        return expr[(i + 1):]
    except ValueError:
        return expr


class ROdict(object):
    def __init__(self, d):
        self._d = d

    def get(self, *args, **kwargs):
        res = self._d.get(*args, **kwargs)
        if isinstance(res, dict):
            return ROdict(res)
        return res

    def __getitem__(self, item):
        res = self._d[item]
        if isinstance(res, dict):
            return ROdict(res)
        return res

    def __len__(self):
        return len(self._d)

    def __dict__(self):
        return copy.deepcopy(self._d)


class MongoPersistentDict:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self._collection_a = None
        self._collection_s = None
        self._mongo_db_sync = None
        self._mongo_db_async = None

    @property
    def mongo_db_sync(self):
        if self._mongo_db_sync is None:
            self._mongo_db_sync = pymongo.MongoClient((config.get("persistent-storage")))["dfract"]
        return self._mongo_db_sync

    @property
    def mongo_db_async(self):
        if self._mongo_db_async is None:
            self._mongo_db_async = motor.motor_tornado.MotorClient((config.get("persistent-storage")))["dfract"]
        return self._mongo_db_async

    @property
    def collection_a(self):
        if self._collection_a is None:
            self._collection_a = getattr(self.mongo_db_async, self.collection_name)
        return self._collection_a

    @property
    def collection_s(self):
        if self._collection_s is None:
            self._collection_s = getattr(self.mongo_db_sync, self.collection_name)
            self._collection_s.ensure_index("@@key", unique=True)
        return self._collection_s

    ##
    ## Sync primitives
    ##
    def __getitem__(self, n):
        r = self.collection_s.find({"@@key": n})[0]
        if '@@value' in r:
            r = r['@@value']
        if isinstance(r, dict):
            return ROdict(r)
        return r

    def __contains__(self, n):
        return self.collection_s.find({"@@key": n}).count() != 0

    def __setitem__(self, n, v):
        if isinstance(v, ROdict):
            v = v.__dict__
            if callable(v):
                v = v()
        if not isinstance(v, dict):
            v = {'@@value': v}
        else:
            v = copy.copy(v)
        v["@@key"] = n
        if n in self:
            return self.collection_s.find_and_modify({"@@key": n}, update={"$set": v})
        else:
            self.collection_s.insert(v)

    def __delitem__(self, n):
        return self.collection_s.find_and_modify({"@@key": n}, remove=True)

    def keys(self):
        return itertools.imap(lambda x: x["@@key"],
                              self.collection_s.find({})
                              )

    def _sanitize_value(self, x):
        x = copy.copy(x)
        if '@@key' in x:
            del x['@@key']
        if '_id' in x:
            del x['_id']
        return x

    def values(self):
        return itertools.imap(lambda x: self._sanitize_value(x), self.collection_s.find({}))

    def items(self):
        return itertools.imap(lambda x: (x["@@key"], self._sanitize_value(x)), self.collection_s.find({}))

    ##
    ## Async primitives (not yet used/tested)
    ##
    @gen.coroutine
    def async__getitem__(self, n):
        r = yield self.collection_a.find({"@@key": n}).tolist()
        r = r[0]
        if '@@value' in r:
            r = r['@@value']
        raise gen.Return(r)

    @gen.coroutine
    def async__contains__(self, n):
        r = yield self.collection_a.find({"@@key": n}).count()
        raise gen.Return(r != 0)

    @gen.coroutine
    def async__setitem__(self, n, v):
        if not isinstance(v, dict):
            v = {'@@value': v}
        else:
            v = copy.copy(v)
        v["@@key"] = n
        if n in self:
            yield self.collection_a.find_and_modify({"@@key": n}, update={"$set": v})
        else:
            yield self.collection_a.insert(v)
        raise gen.Return(v)

    @gen.coroutine
    def async__delitem__(self, n):
        yield self.collection_a.find_and_modify({"@@key": n}, remove=True)

    @gen.coroutine
    def async_keys(self):
        docs = self.collection_a.find({})
        raise gen.Return(itertools.imap(lambda x: x["@@key"], docs))

    @gen.coroutine
    def async_values(self):
        docs = yield self.collection_a.find({})
        raise gen.Return(itertools.imap(lambda x: x, docs))

    @gen.coroutine
    def async_items(self):
        docs = yield self.collection_a.find({})
        raise gen.Return(itertools.imap(lambda x: (x["@@key"], x), docs))

    def close(self):
        pass

    def get(self, k, default):
        if k in self._shelve:
            return self._shelve[k]
        else:
            return default


class ShelvedPersistentDict:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.__shelve = None

    @property
    def _filename(self):
        return os.path.join(_skip_proto(config.get("persistent-storage")), self.collection_name + ".shelve")

    @property
    def _shelve(self):
        if self.__shelve is None:
            if not os.path.exists(_skip_proto(config.get("persistent-storage"))):
                os.makedirs(_skip_proto(config.get("persistent-storage")))
            self.__shelve = shelve.open(self._filename)
        return self.__shelve

    def close(self):
        if self.__shelve:
            self.__shelve.close()
        self.__shelve = None

    def destroy(self):
        self.close()
        success = True
        try:
            os.unlink(self._filename)
        except Exception as e:
            logging.warning("Failed to remove shelve:" + repr(e) + ":" + self._filename)
            success = False
        try:
            os.rmdir(_skip_proto(config.get("persistent-storage")))
        except:
            pass
        return success

    ##
    ## Sync primitives
    ##
    def _nk(self, n):
        return str(n)

    def __getitem__(self, n):
        n = self._nk(n)
        res = self._shelve[n]
        if isinstance(res, dict):
            return ROdict(res)
        return res

    def __contains__(self, n):
        n = self._nk(n)
        return n in self._shelve[n]

    def __setitem__(self, n, v):
        n = self._nk(n)
        if isinstance(v, ROdict):
            v = v.__dict__
            if callable(v):
                v = v()
        self._shelve[n] = v

    def __delitem__(self, n):
        del self._shelve[n]

    def keys(self):
        return self._shelve.keys()

    def values(self):
        return self._shelve.values()

    def items(self):
        return self._shelve.items()

    def get(self, k, default):
        if k in self._shelve:
            return self._shelve[k]
        else:
            return default


__proto = _proto(config.get("persistent-storage"))

if __proto == "mongodb":
    logging.debug("Using mongodb as backend for persistency")
    PersistentDict = MongoPersistentDict
elif __proto == "shelve":
    logging.debug("Using shelve as backend for persistency")
    PersistentDict = ShelvedPersistentDict
else:
    raise ValueError("Unknown persistency protocol")
