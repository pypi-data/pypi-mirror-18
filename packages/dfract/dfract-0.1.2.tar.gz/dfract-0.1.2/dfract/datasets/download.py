import requests
from dfract import serialization
from dfract.dataset import Dataset
from dfract.utils import sha256


class DownloadFilterForDataset(Dataset):
    _DISABLE_AUTOKEYS = True

    def __init__(self, dataset):
        self._dataset = dataset
        super(DownloadFilterForDataset, self).__init__()

    def keys(self, *args, **kwargs):
        return self._dataset.keys(*args, **kwargs)

    def _download(self, url):
        response = requests.get(url)
        typeinfo = "", "mimetype:" + response.headers['Content-Type']
        return serialization.serialized2native(response.content, typeinfo=typeinfo)

    def get(self, k, mode="native", *args, **kwargs):
        if mode == "native":
            x = self._dataset.get(k, mode, *args, **kwargs)
            return self._download(x)
        else:
            raise ValueError

    def signature(self):
        return sha256("download( %s)" % (self.dataset.signature())).hexdigest()


__call__ = DownloadFilterForDataset
