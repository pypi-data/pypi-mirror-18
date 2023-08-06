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
from dfract.dataset import Dataset
from dfract.utils import sha256


class PyTransformDataset(Dataset):
    """
    Use this dataset to transform any dataset in a new one.

    Thanks to the magic of eval and autoimport, it allows to any python module you want.

    TODO: The transform shall also generate transformed mapped metadata for metadata matching
    the structure of the initial static.
    """

    def __init__(self, transform, dataset):
        """
        Transform is a single transform specified as a string or a dict associating key suffixes to transforms.
        """
        self.transform = transform
        self.dataset = dataset
        super(PyTransformDataset, self).__init__()

    def keys(self, *args, **kwargs):
        return self.dataset.keys(*args, **kwargs)

    def get(self, k, mode="native", *args, **kwargs):
        if mode == "native":
            x = self.dataset.get(k, mode, *args, **kwargs)
            if isinstance(self.transform, str):
                r = eval(self.transform, autoimp.__dict__, locals())
            else:
                return self.transform(x)
        else:
            raise ValueError

    def signature(self):
        return sha256("pytransform(%s, %s)" % (self.transform, self.dataset.signature())).hexdigest()


__call__ = PyTransformDataset
