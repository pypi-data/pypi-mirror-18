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

import itertools
import logging
import random

from tornado import gen

from .events import EventHandler
from .object import DFractObject
from .serialization import autoserialize_get
from .utils import sha256, methodargs


# -------------------------------------------------------------------------------------------------------------------
#  L1 Dataset Model
#  ----------------
#  L1 Datasets are just collection files without additional structure.
#  They are not implementation here consult dfract-datafs to see implementation.
# -------------------------------------------------------------------------------------------------------------------


## L2 Dataset Model
## ----------------

def autokeys(keym):
    def new_keys(from_key=None, limit=-1, loop=False):
        kwargs = {}
        ma = methodargs(keym)
        if "from_key" in ma:
            kwargs["from_key"] = from_key
        if "limit" in ma:
            kwargs["limit"] = limit
        if "loop" in ma:
            kwargs["loop"] = loop

        rk = keym(**kwargs)
        if not isinstance(rk, list):
            # We force keys to be returned as list.
            # The idea here is that it is what the API will require ultimately - and even even pagination
            # is supported by the api.
            if limit != -1:
                rk = itertools.islice(rk, limit)
            rk = list(rk)
        if from_key != None:
            rk = rk[(rk.index(from_key) + 1):]
        if limit != -1:
            rk = rk[:limit]
        return rk

    return new_keys


class L2Dataset(DFractObject):
    """
    DFRACT Datasets.

    NOTE: This is the level 2 of dataset hierarchy

    LEVEL 1: The actual static (files/memory on a server).                                                                      # a proprietary representation/ path
    LEVEL 2: Object allowing to access the static in a uniform way. (any implementation LEVEL 0 should be valid with L0)        # an instance in local memory
    LEVEL 3: An expression instantiating dataset object in a dataset language and instantiated as service (served as an API)) # a URL
    LEVEL 4: A publicly referenceable to a shared instance of a service giving access to a dataset build in a specific way and eventually extended in various way by crowd power.
                                                                                                                              # a resolvable URL linking numerous elements
    # NOTE regarding link between level 3 and 4 :
    # in language expressions:  "pair(caltech256(), annotations)" each subdataset is instantiated in dflow
    # and will have its own URL so that composite expressions can be created.
    # It is important to understand that providing a new dataset expression creates a new datasets and does not reuse
    # commonly well known datasets unless stated.

    Properties:

    - For a specific key the return value is functional
    - The list of keys is constant (ordered)
    - The keys are string that respect the rules for key syntax.
        - [A-Za-z0-9_.] must be used for constants and utf8 letterst
        - [/] must not be used in keys as it is used in file systems in URI
        - [$@,;+-] unary modifiers must always be used between brackets to ensure they can be associated and parsed
         by the right module at parsing time
        - No quotes
        - It is recommended to base64 encode binary contents
    """
    _typesystems = ["native"]

    def __init__(self):
        """
        Construct a dataset.
        The private fields are internal and not part of specification.
        """
        super(L2Dataset, self).__init__()

        self._dataset_url = None
        self._dataset_datatype_native = None
        self._dataset_datatype_serialized = None

        self._dataset_version = None
        self._dataset_previous_version = None
        self._dataset_changes_since_previous_version = None  # Optional list describing changes that have occured since last version # this may also contain a special value
        # to indicate that the compute of the diff is being undertaken by a specific worker and that normally other workers can rely on this worker to compute the diff
        self._dataset_next_version = None

        ##
        ## FIXME: It can be discussed whether LEVEL 2 objects have already datasets, aggregates, etc or whether it should be reserved to level 3
        ## objects. On one side it seems reasonable that no service should be required to have links between columns, indexes and aggregates
        ## on the other ide the key point of LEVEL 3 and 4 is to ensure much larger collection of links attached to datasets, and consequently
        ## the proxy of a level 3 object shall normally return much more information.
        ##
        self._dataset_indexes = {}  # query to list of keys
        self._dataset_indexes_collection_eh = EventHandler()
        self._dataset_aggregate = {}  # alt_key_space to alt_value_space
        self._dataset_aggregate_eh = EventHandler()

        self._dataset_links = {}  # ontology-following
        # Slinks to some other columns (non exhaustive)
        self._dataset_links_eh = EventHandler()

        self._dataset_metadata = {}
        self._dataset_metadata_eh = EventHandler()

        self._dataset_versioninfo_eh = EventHandler()
        self._dataset_mimetype = "applications/octet-stream"

        if (not getattr(self, "_DISABLE_AUTOKEYS", None)) and "from_key" not in methodargs(self.keys):
            self.keys = autokeys(self.keys)

        if "serialized" not in self._typesystems:
            self._typesystems = self._typesystems[:]
            self._typesystems.append("serialized")
            e0 = self.get(next(iter(self.keys(limit=1))))
            self.get, self._dataset_mimetype = autoserialize_get(e0, self.get)

    def get_typesystems(self):
        return self._typesystems

    def register_adjunct_objects(self, context=None):
        for x in dir(self):
            if x[0] != '_':
                v = getattr(self, x)
                if callable(v) and not hasattr(v, "co_code") and isinstance(v, type) and issubclass(v, Dataset):
                    logging.info("registering adjunct dataset " + x)

                    class NV(v):
                        def keys(nvself, *args, **kwargs):
                            return self.keys(*args, **kwargs)

                    instance = NV()
                    self.dfract_slave.ipc_object_register(instance, uuid=self.dfract_uuid, subobject=x, type="dataset")
                    self.dfract_master.object_add_reference(context, self.dfract_uuid, x, "dataset")
    ##
    ## STATIC METADATA
    ##

    def metadata(self):
        """
        Returns read only information about this dataset.

        Ideally including, version, previous_version , next_version, changeset
        API pattern must be {DATASET}/metadata/
        """
        return self._dataset_metadata

    ## DATASET ABSTRACT METHODS THAT NEED TO BE IMPLEMENTED
    def keys(self, from_key=None, limit=-1, loop=False):
        """
        Return an iterable of keys.

        For portability reasons, we recommend to consider all keys as strings.
        For performance reasons it is also recommended to return the keys as list
        or arrays although wrapper datasets can always be added to implement this behavior.

        Expected behavior:
        - keys are returned always in the same order
        - keys for a specific dataset are always the same
        - keys are always strings
        - There are some special characters that should not be used at the beginning of keys :
          These are : "@" (methods)  and "~" (linked object) and ":" (reserved)

        Typical output: [ "a", "b", "c", "d", "e" ]

        API pattern must be {DATASET}/@keys?per_page=n&page=x
        """
        assert False

    def get(self, key, typesystem="native"):
        """
        Implementation speficic returns an instance of the static in the native format.

        NOTE: Serialisation to other formats should be undertook by separate module ?

        API pattern must be {DATASET}/:id
        """
        assert False
        if self._last_result_time:
            return self._last_result

    @gen.coroutine
    def generative_coroutine(self):
        return False

    def elementtype(self, typesystem="native"):
        """
        Return the type of the elements in the dataset.

        AT THIS STAGE TYPESYSTEM MUST BE EITHER
        "native" if native a type descriptor specific to the system
        or
        "serialized" if serialized a serialisation of the static must be offered, default serialisation
        for structured static may YAML or MIMEJSON.

        The format in which we return the information about the type does matter.
        There is no good cross-platform standard to describe datatype. Hence,
        we recommend to return by default the native language type, and to also
        support a typesystem : "mimetype", which is if this static was to be serialised
        in file how would it be serialised.

        TODO: The link between the type and the serialisation shall be considered outside of
        the scope of this documentation but weill be implemented in a module.

        NOTE: Keep in mind that the goal of this function is multiple. It should on one
        side allow to infer the type of complex dataset and on the other side it should

        Expected behavior:
        elementtype("python")   -> numpy.ndarray
        elementtype("mimetype") -> "application/hdf5"
        elementtype("python")   -> int
        elementtype("mimetype") -> "text/int" ## application / json
        elementtype("python")   -> dict
        elementtype("mimetype") -> application / json

        API pattern must be {DATASET}/@elementtype/
        """
        if typesystem == "native":
            return type(self.get(iter(self.keys()).next()))
        elif typesystem == "serialized":
            return self._dataset_mimetype
        else:
            raise ValueError("Unsupported serialization")

    def hash(self, key, typesystem="native"):
        """
        Returns the hash associated with an item.

        NOTE: Eventually allow to speed up indexing during index change
        """
        return sha256(self.get(key, "serialized")).hexdigest()

    def count(self):
        """
        Return the number of elements in the dataset

        Ideally this should be overrident by the dataset
        """
        return len(list(self.keys()))

    def key_space_signature(self):
        """
        Hash key allowing to identify the key space.
        This allow to quickly ensure that datasets are compatible and can be linked together.
        """
        r = ""
        for k in self.keys():
            r += "%s##" % (hash(k))
        return sha256(r).hexdigest()

    def signature(self):
        r = ""
        for k in self.keys():
            r += "%s@%s##" % (k, self.hash(k))
        return sha256(r).hexdigest()

    def values(self):
        """
        Return the values of the element in the dataset.

        Ideally, this should be overrident by the dataset when additional performance are needed.
        """
        for k in self.keys():
            yield self.get(k)

    def items(self):
        """
        Return the pairs of (key,value).

        Ideally this should be overrident by the dataset
        """
        for k in self.keys():
            yield (k, self.get(k))

    # convenience sugar in python

    def get_adjunct_datasets(self):
        return []

    def __len__(self):
        return self.count()

    def validate(self, completeness=1):
        """
        Validate an object is a valid set.

        :return: True if the dataset is valid, False otherwise.
        """
        keys = self.keys()
        if completeness != 1:
            keys = filter(lambda: random.random() <= completeness, keys)
        if not len(set(keys)) == len(keys):
            return False, "Duplicate in keys"

        for k in keys:
            if isinstance(type(k), str):
                return False, "All keys need to be string"
            if "/" in k:
                return False, "Forbidden character in static key"

        # assert we support from_key
        lk0 = len(keys)

        if len(keys):
            keys = self.keys(from_key=keys[0])
            lk1 = len(keys)
            assert (lk0 == lk1 + 1)

        # Assert other kwargs are supported
        keys = self.keys(limit=2, loop=False)

        return True, "Valid dataset"


class L3Dataset(L2Dataset):
    ##
    ## LINKED DATA
    ##

    def table_links(self):
        """
        Return a list of dataset that share the same index space as this dataset and that can be considered as userful for various reasons.
        The dataset relationships should follow relation eventually defined in an ontology.

        The reference to the dataset is passed as a link to an online DFRACT dataset and not directly as an object.

        NOTE: Due to SoC, we assume that dataset once they are in the links are working and available object.
              In reality this may be more complex. There may be requirement for process that will ensure dataset remain viable.

        NOTE: each table_link must have a name.
        """
        return list(self._dataset_links.items())

    def index_links(self):
        """
        Return a list of indexes that share the same key space as this dataset and that can be considered as useful to
        look for information on this dataset.

        The reference to the index is passed as a link as link to an online DFRACT index and not directly as an object.
        NOTE: Due to SoC, we assume that dataset once they are in the links are working and available object.
              In reality this may be more complex. There may be requirement for process that will ensure dataset remain viable.

        NOTE: each index_link must have a name.
        """
        return list(self._dataset_indexes.items())

    ##
    ## VERSIONNING
    ##
    def get_previous_version(self):
        """
        A link to a previouss version of the dataset.
        """
        return self._dataset_previous_version

    def next_version(self):
        """
        A link to the next version of the dataset.
        """
        return self._dataset_next_version

    ##
    ## SERVICE AND METADATA PERSISTENCY
    ##
    def dump_object(self):
        """
        Save information associated with a dataset.
        """
        metadata = {
            "metadata": self._dataset_metadata,
            "mimetype": self._dataset_mimetype,
        }

        eh_info = {
            "links_eh": self._dataset_links_eh.dumps(),
            "aggregate_eh": self._dataset_aggregate_eh.dumps(),
            "index_eh": self._dataset_index_eh.dumps(),
            "metadata_eh": self._dataset_metadata_eh.dumps(),
            "versioninfo_eh": self._dataset_versioninfo_eh.dumps(),

        }
        metadata.update(eh_info)

        version_info = {
            "version": self._dataset_version,
            "previous_version": self._dataset_previous_version,
            "next_version": self._dataset_next_version,
            "changes": self._dataset_changes_since_previous_version,
        }
        metadata.update(version_info)

        links = {
            "links": self._dataset_links,
            "indexes": self._dataset_indexes,
            "aggregates": self._dataset_aggregate,
        }

        metadata.update(links)

        return metadata

    def load_object(self, data):
        """
        Update meta based on save information.
        """
        # metadata
        self._dataset_metadata = data.get("metadata")
        self._dataset_mimetype = data.get("mimetype")

        # versions
        self._dataset_version = data.get("version")
        self._dataset_previous_version = data.get("previous_version")
        self._dataset_next_version = data.get("previous_version")
        self._dataset_changes = data.get("changes")

        # links
        self._dataset_links = data.get("links")
        self._dataset_indexes = data.get("indexes")
        self._dataset_metadata = data.get("metadata")

        # event handler


class L4Dataset(L3Dataset):
    def get_url(self):
        """
        Returns the URL of this dataset - useful when building reference to elements inside this dataset.

        Returns:
        None -> If the dataset associated with this dataset is not known yet or if the dataset is not shared

        """
        return self._dataset_url


Dataset = L2Dataset
