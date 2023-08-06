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
import Pyro4
from dfract.dataset import Dataset


@Pyro4.expose
class DFractExposedDataset(Dataset):
    """
    Pyro4 expose wrapper seem to have difficulty handling polymorphism.
    So we provide a wrapper object that describes the interface that Pyro exposes

    FIXME: Eventually - remove this.
    """

    def __init__(self, dataset):
        # super(Dataset, self).__init__()
        self.__dfract_dataset = dataset
        # for x in dir(self.__dfract_dataset):
        #    Pyro4.expose()
        self.__setattr__ = self.__setattr

    def __getattr__(self, item):
        return getattr(self.__dfract_dataset, item)

    def __setattr(self, key, value):
        if key == "__dfract_dataset":
            return super(DFractExposedDataset, self).__setattr__(key, value)
        return setattr(self.__dfract_dataset, key, value)

    def __hasattr__(self, item):
        return hasattr(self, item)

    # Wrap dataset method that we want to expose
    def get_typesystems(self):
        return self.__dfract_dataset.get_typesystems(*args, **kwargs)

    def metadata(self):
        return self.__dfract_dataset.metadata(*args, **kwargs)

    def keys(self, *args, **kwargs):
        return self.__dfract_dataset.keys(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.__dfract_dataset.get(*args, **kwargs)

    def values(self, *args, **kwargs):
        return self.__dfract_dataset.values(*args, **kwargs)

    def items(self, *args, **kwargs):
        return self.__dfract_dataset.items(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self.__dfract_dataset.count(*args, **kwargs)

    def register_adjunct_objects(self, *args, **kwargs):
        return self.__dfract_dataset.register_adjunct_objects(*args, **kwargs)

    def dfract_set_uuid_master_and_slave(self, *args, **kwargs):
        self.__dfract_dataset.dfract_set_uuid_master_and_slave(*args, **kwargs)
        super(DFractExposedDataset, self).dfract_set_uuid_master_and_slave(*args, **kwargs)

__call__ = DFractExposedDataset
