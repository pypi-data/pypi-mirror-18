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
"""
This file contain different implementation allowing to get access to a dfract dataset or datastream.

"""
from .builder import generic_builder
from .client import DFractClient


def l2_invoke(expr):
    """
    Use Python API to instantiate object within current process.

    :return: a Dataset L2 object
    """
    return generic_builder(expr)


def l3_invoke(expr):
    """
    Use datahub server to instantiate and manipulate process.

    :return: A proxy object to a DatasetL3 acquired via the the server
    """
    dc = DFractClient()
    ds = dc.dataset_invoke(expr)
    return ds


def l4_invoke(expr):
    """
    Use datahub http server to instantiate and manipulate process.

    :return: A proxy object to a DatasetL4 object acquired via the the http server
    """
    raise Exception


    # Not
    # dc = DFractAPIClient()
    # dataset = dc.dataset_invoke(expr)



if __name__ == "__main__":
    ## TODO: TEST - SUBJECT TO CORRECT CREDENTIAlS AND LEVEL-LIMITATIONS - ALL INVOKE SHOULD ALLOW ACCESS TO DATASET OBJECT IN THE SAME WAY
    pass
