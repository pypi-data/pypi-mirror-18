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
import bisect
import functools
import logging
import sys
import threading
import time
import traceback
import uuid

from dfract import config
from dfract.cache_utils import lru_cache
from tornado import gen
from tornado.ioloop import IOLoop

from .events import EventHandler
from .object import DFractObject
from .serialization import autoserialize_get
from .utils import md5sum
from .utils import sha256


def run_eh_chain():
    def _run_eh_chain(c, *args, **kwargs):
        for eh in c:
            eh(*args, **kwargs)

    return _run_eh_chain


def eh_chain(orig, cf):
    if not hasattr(orig, "_eh_chain"):
        neh = run_eh_chain()
        if orig is None:
            rl = []
        else:
            rl = [orig]
        neh._eh_chain = rl + [cf]
        neh = functools.partial(neh, neh._eh_chain)
    else:
        orig._eh_chain.append(cf)
        neh = orig

    return neh


def eh_unchain(orig, cf):
    if hasattr(orig, "_eh_chain"):
        orig._eh_chain = filter(lambda x: x != cf, orig._eh_chain)
        return orig
    print("empty chain")
    return None


class FifoQueue(object):
    """
    Simple container managing providing static persistency for datastreams.
    """

    def __init__(self, capacity=10, persistency=600, clock=None, verbose=False, strict_near=False):
        self.clock = clock or time.time
        self.capacity = capacity
        self.persistency = persistency
        self._q = []  # NOTE: An out-of-core container should also be provided for very large datastreams
        self._qv = []
        self._c = 0
        self.on_add = None
        self.on_remove = None
        self.lock = threading.RLock()
        self.sem = threading.Semaphore(0)
        self._verbose = verbose
        self._strict_near = strict_near

    def enqueue(self, value):
        with self.lock:
            while (self.capacity > 0) and len(self._q) >= self.capacity:
                self.dequeue()
                if self._verbose:
                    logging.warning("an object is being dequeued and discarded as fifo has reached maximum capacity")
            when = self.clock()
            if self.capacity > 0:
                self._q.append(when)
                self._qv.append(value)
                self._c += 1
                self.sem.release()
            if self.on_add is not None:
                self.on_add((when, value))

    def _clear_expired(self, now):
        with self.lock:
            while len(self._q) and ((now - self._q[0]) > self.persistency):
                self.sem.acquire()
                w = self._q.pop(0)
                v = self._qv.pop(0)
                self._c -= 1
                if self.on_remove:
                    self.on_remove((w, v))

    def dequeue(self):
        res = None
        fetched = False
        with self.lock:
            now = self.clock()
            self._clear_expired(now)
            if len(self._q):
                self.sem.acquire()
                res = self._q.pop(0)
                resv = self._qv.pop(0)
                self._c -= 1
                if self.on_remove:
                    self.on_remove((res, resv))
                fetched = True
        if not fetched:
            raise KeyError
        return res, resv

    def near_left(self, k):
        """
        Returns the key closest to k on the left.
        :param k:
        :return:
        """
        if self.capacity <= 0:
            return None
        with self.lock:
            now = self.clock()
            self._clear_expired(now)
            if not len(self._q):
                return None
                # raise LookupError, "Empty queue"
            i = bisect.bisect(self._q, k)
            if i < 0:
                if self._strict_near:
                    return None
                i = 0
            if i >= len(self._q):
                if self._strict_near:
                    return None
                i = len(self._q) - 1

            return self._q[i], self._qv[i]

    def near_right(self, k):
        if self.capacity <= 0:
            return None
        with self.lock:
            now = self.clock()
            self._clear_expired(now)
            if not len(self._q):
                return None
            i = bisect.bisect_right(self._q, k)
            if i < 0:
                if self._strict_near:
                    return None
                i = 0
            if i >= len(self._q):
                if self._strict_near:
                    return None
                i = len(self._q) - 1
            return self._q[i], self._qv[i]

    def pending_mutex(self, wait=False):
        self._clear_expired(self.clock())
        with self.lock:
            if self._c == 0:
                if not wait:
                    raise KeyError
            else:
                return self._q[0], self._qv[0]
        self.sem.acquire(blocking=True)
        with self.lock:
            res = self._q[0], self._qv[0]
            self.sem.release()
            return res

    # @gen.coroutine()
    # def pending_coroutine(self, wait=False):

    def __len__(self):
        with self.lock:
            now = self.clock()
            self._clear_expired(now)
        return len(self._q)

    def keys(self, from_key=0):
        with self.lock:
            now = self.clock()
            self._clear_expired(now)
            res = [i for i in self._q if i > from_key]
        return res


class Datastream(DFractObject):
    """
    The most minimal implementation of datastreams we can think at .

    NOTE: This is the level 1 of datastream hierarchy

    LEVEL 1: The actual static (files/memory on a server).
    LEVEL 2: Object allowing to access the static in a uniform way.
    LEVEL 3: An expression instantiating datastream object in a datastream language.
    LEVEL 4: A publicly referenceable to a shared instance of a service giving access to a datastream build in a specific way.

    # NOTE regarding link between level 3 and 4 :
    # in language expressions:  "pair(caltech256(), annotations)" each subdatastream is instantiated in dflow
    # and will have its own URL so that composite expressions can be created.
    # It is important to understand that providing a new datastream expression creates a new datastreams and does not reuse
    # commonly well known datastreams unless stated.

    Properties:

    For a specific key the return value is functional.

    Datasteams may come from different sources.
    """
    _typesystems = ["native"]
    _persistency = 600  # allow access to last 10 minutes of static by default
    _FIFO_ARGS = {}
    _FUNCTIONAL = False

    def __init__(self):
        super(Datastream, self).__init__()

        self._state = "initializing"
        self._running = True
        self._datastream_url = None
        self._datastream_datatype_native = None
        self._datastream_datatype_serialized = None
        self._datastream_version = None
        self._datastream_previous_version = None
        self._datastream_next_version = None
        self._datastream_version_eh = EventHandler()  # event handler for the version collection
        self._datastream_indexes = []
        self._datastream_indexes_collection_eh = EventHandler()  # event handler for the index collection
        self._datastream_links = []
        self._datastream_links_collection_eh = EventHandler()  # event handler for the links collection
        self._datastream_metadata = {}
        self._datastream_streamactivity_eh = EventHandler()  # event handler to handle new events on the str
        self._callbacks = {}

        if not self._FUNCTIONAL:
            self._fifo = FifoQueue(**self._FIFO_ARGS)
            self._fifo.on_add = eh_chain(self._fifo.on_add,
                                         lambda obs: self._datastream_streamactivity_eh.on_add(obs[0]))
            self._fifo.on_remove = eh_chain(self._fifo.on_remove,
                                            lambda obs: self._datastream_streamactivity_eh.on_remove(obs[0]))
            # self._fifo.enqueue("x")

        self.start()

    def on_start(self):
        # if True and  not self._FUNCTIONAL:
        #    self._on_first_data_uuid = None
        #    self._fifo.on_add = eh_chain(self._fifo.on_add, self.on_first_data)
        # else:
        self._on_first_data_uuid = self._datastream_streamactivity_eh.add_on_add(self.on_first_data)

    def on_first_data(self, data):
        if len(self._typesystems) == 1 and self._typesystems[0] == "native":
            self._typesystems.append("serialized")
            e0 = self.get(next(iter(self.keys())))
            self.get, self._dataset_mimetype = autoserialize_get(e0, self.get)
            # if self._on_first_data_uuid is None:
            #    self._fifo.on_add = eh_unchain(self._fifo.on_add, self.on_first_data)
            # else:
            self._datastream_streamactivity_eh.del_on_add(self._on_first_data_uuid)
            self._state = "ready"
            logging.info("Datastream %s : %r : set state to ready" % (self.__class__.__name__, self))

    def keys(self, from_key=0, limit=-1, loop=False):
        """
        Return a list of keys. (NOT AN ITERABLE !)

        There is no warranty that these key will be resolvable as entries in will be discarded over time.

        Expected behavior:
        - keys are returned always in the same order
        - keys for a specific datastream are always the same
        - keys are always strings

        Typical output: [ "a", "b", "c", "d", "e" ]
        """
        repeat = True
        res = []
        if loop:
            assert (limit >= 0)

        while repeat:
            repeat = False
            for f in self._fifo.keys(from_key=from_key):
                if limit == 0:
                    repeat = False
                    loop = False
                    break

                res.append(f)
                limit -= 1

            if loop:
                if (config.get("datastream-mode") == "thread"):
                    time.sleep(0.01)  # FIXME: Add config variable
                elif config.get("datastream-mode") == "coroutine":
                    raise NotImplementedError
                else:
                    raise ValueError
                repeat = True

        return res

    def register_callback(self, callback, callback_id=None):
        if callback_id is None:
            callback_id = str(uuid.uuid4()).replace('-', '')

        self._callbacks[callback_id] = callback
        return callback_id

    def items(self):
        for k in self.keys():
            yield (k, self.get(k))

    def elementtype(self, typesystem="native"):
        """
        Return the type of the elements in the datastream.

        AT THIS STAGE TYPESYSTEM MUST BE EITHER
        "native" if native a type descriptor specific to the system
        or
        "serialized" if serialized a serialisation of the static must be offered, default serialisation
        for structured static may YAML or MIMEJSON as both formats allow link to subobjects stored at other URLs.

        The format in which we return the information about the type does matter
        ultimately we would like this type information to be sufficient to instantiate a similar
        proxy object in any language.

        Unfortunately there is no good cross-platform standard to describe datatype.
        The type of constraints that may be expressed on static are very diverse and there
        is no way, we can make everyone agree.

        TODO: The link between the type and the serialisation shall be considered outside of
        the scope of this documentation but will be hopefully implemented in a module. of dfract

        NOTE: Keep in mind that the goal of this function is multiple. It should on one
        side allow to infer the type of complex datastream and on the other side it should

        Expected behavior:
        elementtype("python")   -> numpy.ndarray
        elementtype("serialised") -> "application/hdf5"
        elementtype("python")   -> int
        elementtype("serialised") -> "text/int" ## application / json
        elementtype("python")   -> dict
        elementtype("serialised") -> application/json # reference to schema ??
        """
        assert (False)

    def get(self, key, typesystem="native", wait=True):
        """
        Implementation speficic returns an instance of the static in the native format.

        NOTE: Serialisation to other formats should be undertook by separate module ?
        """
        res = None
        if typesystem == "native":
            if len(self._fifo):
                res = self._fifo.near_left(float(key))[1]
            else:
                logging.warning("Datastream queue is empty")
            return res

        assert (False)

    def get_latest(self, since, typesystem="native", wait=False):
        """
        Implementation speficic returns an instance of the static in the native format.

        Specify if the call should be blocking/yieleding if no element is currently present in the queue

        NOTE: Serialisation to other formats should be undertook by separate module ?
        """
        if wait:
            return self._fifo.pending_mutex(wait=wait)
        else:
            return self._fifo.near_left(0)[1]

    def hash(self, key, typesystem="native"):
        """
        Returns the hash associated with an item.

        NOTE: Eventually allow to speed up indexing during index change
        """
        return sha256(self.get(key, "serialized")).hexdigest()

    def table_links(self):
        """
        Return a list of datastream that share the same index space as this datastream and that can be considered as userful for various reasons.
        The datastream relationships should follow relation eventually defined in an ontology.

        The reference to the datastream is passed as a link to an online DFRACT datastream and not directly as an object.
        NOTE: Due to SoC, we assume that datastream once they are in the links are working and available object.
              In reality this may be more complex. There may be requirement for process that will ensure datastream remain viable.
        """
        return self._datastream_links

    def index_links(self):
        """
        Return a list of indexes that share the same key space as this datastream and that can be considered as useful to
        look for information on this datastream.

        The reference to the index is passed as a link as link to an online DFRACT index and not directly as an object.
        NOTE: Due to SoC, we assume that datastream once they are in the links are working and available object.
              In reality this may be more complex. There may be requirement for process that will ensure datastream remain viable.
        """
        return self._datastream_indexes

    def count(self):
        """
        Return the number of elements in the datastream

        Ideally this should be overrident by the datastream
        """
        return len(self.keys())

    def get_url(self):
        """
        Returns the URL of this datastream - useful when building reference to elements inside this datastream.

        Returns:
        None -> If the datastream associated with this datastream is not known yet or if the datastream is not shared

        """
        return self._datastream_url

    def get_previous_version(self):
        """
        A link to a previous version of the datastream.
        """
        return self._datastream_previous_version

    def next_version(self):
        """
        A link to the next version of the datastream.
        """
        return self._datastream_next_version

    def versioned_signature(self):
        return sha256("%s-%s" % (self._module_hash(), self.signature())).hexdigest()

    def signature(self):
        return sha256(self.__type__.__name__).hexdigest()

    @lru_cache
    def _module_hash(self):
        return md5sum(open(sys.modules[self.__module__].__file__).read()).hexdigest()

    @gen.coroutine
    def _generator_coroutine(self):
        self.on_start()
        try:
            while True:
                yield self._generator_coroutine()
        except Exception as e:
            traceback.print_exc(e)

    def _generator_thread(self):
        self.on_start()
        try:
            ioloop = IOLoop()
            while self._running:
                ioloop.run_sync(self._generator_coroutine)
        except Exception:
            traceback.print_exc()

    def start(self):
        """
        Start the datastream process. i.e. the generation of the data.

        :return: True if success
        """
        if (config.get("datastream-mode") == "thread"):
            self._nt = threading.Thread(target=self._generator_thread)
            self._nt.daemon = True
            self._nt.start()
        elif config.get("datastream-mode") == "coroutine":
            raise NotImplementedError
        else:
            raise ValueError("invalid dataset-mode")
        return True

    def stop(self):
        if (config.get("datastream-mode") == "thread"):
            self._nt.join(0)
        elif config.get("datastream-mode") == "coroutine":
            raise NotImplementedError
        else:
            raise ValueError("invalid dataset-mode")

    def validate(self):
        """
        Validate an object is a valid stream.

        :return: True if the datastream is valid, False otherwise.
        """
        keys = self.keys()
        try:
            for k in keys:
                f = float(k)
        except:
            return False, "Invalid key : %r" % (k,)

        # FIXME: add more tests.
        return True, "Valid datastream"
