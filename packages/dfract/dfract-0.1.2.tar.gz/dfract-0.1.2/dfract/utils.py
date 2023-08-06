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
import base64
import hashlib
import inspect
import itertools
import sys
import uuid

if sys.version[0] == '2':
    import mdv
else:
    mdv = None


def _gen_uuid():
    return str(uuid.uuid4()).replace('-', '')[:24]

def pretty_print(value, do_print=True):
    text = value
    if value is None:
        text = ""
    elif isinstance(value, list):
        text = ""
        for i in value:
            text += ("* " + repr(i) + "\n")
        if len(text):
            if mdv is not None:
                text = mdv.main(text)

    if do_print:
        print(text)
    else:
        return text


def paginate(context, kwargs, sliceable):
    if not context.get("paginate", False):
        return sliceable
    else:
        page = kwargs.get("page", 1) - 1
        per_page = kwargs.get("per_page", 20)

        if not hasattr(sliceable, "__getitem__"):
            sliceable = list(sliceable)
        return sliceable[page * per_page:(page + 1) * per_page]


if sys.version[0] == '3':
    imap = map

    def sha256(x):
        # if isinstance(x, bytes):
        if hasattr(x, "encode"):
            x = x.encode('utf8')
        return hashlib.sha256(x)


    def md5sum(x):
        if hasattr(x, "encode"):
            x = x.encode('utf8')
        return hashlib.md5(x)

else:
    sha256 = hashlib.sha256
    md5sum = hashlib.md5
    imap = itertools.imap

if sys.version[0] == '2':
    def b64encode(x):
        return base64.b64encode(x)


    def b64decode(x):
        return base64.b64decode(x)

else:
    def b64encode(x):
        if hasattr(x, "encode"):
            x = x.encode('utf8')
        return base64.b64encode(x).decode('ascii')


    def b64decode(x):
        if hasattr(x, "encode"):
            x = x.encode('utf8')
        return base64.b64decode(x).decode('ascii')


def methodargs(m):
    if sys.version[0] == "2":
        return inspect.getargs(m.im_func.func_code).args
    elif sys.version[0] == "3":
        return inspect.getargs(m.__func__.__code__).args
    else:
        raise NotImplementedError
