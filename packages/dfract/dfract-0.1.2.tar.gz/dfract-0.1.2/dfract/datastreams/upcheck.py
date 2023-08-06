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

import pyautogui
from dfract import config
from dfract.datastream import Datastream
from dfract.utils import sha256
from tornado import gen
from tornado import httpclient


class UpcheckDatastream(Datastream):
    """
    Simple datastream to monitor the status of hosts.
    """

    def __init__(self, url, period=60):
        self._url = url
        self._period = period
        super(UpcheckDatastream, self).__init__()

    @gen.coroutine
    def _generator_coroutine(self):
        c = httpclient.HTTPClient()
        try:
            req = httpclient.HTTPRequest(self._url)
            yield c.fetch(req)
            res = True
        except:
            res = False
        self._fifo.enqueue(res)
        yield gen.sleep(self._period)

    def signature(self):
        return sha256("upcheck@(%s,%s)" % (self._url, self._period)).hexdigest()


__call__ = UpcheckDatastream
