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

from dfract.client import DFractClient

class DFractObject(object):
    """
    Set an id to every isolated object used in dfract.

    The isolated objects are assumed to run in separate containers.
    They are connected to the main hub via an ORB or a similar technology.
    """


    def __init__(self):
        self.__id = os.environ.get("DFRACT_INSTANCE_UUID")
        self._dfract__client = None
        # self.dfract_remote.internal_set_object_state(self.__id, 'INIT')

    @property
    def dfract_remote(self):
        """
        Provide access to the (master) server via its standard API
        :return:
        """
        if self._dfract__client is None:
            self._dfract__client = DFractClient()
        return self._dfract__client

    def dfract_set_uuid_master_and_slave(self, uuid, master, slave):
        self._dfract_uuid = uuid
        self._dfract_master = master
        self._dfract_slave = slave

    @property
    def dfract_master(self):
        """
        Connects to the master server
        :return:
        """
        return self._dfract_master

    @property
    def dfract_slave(self):
        """
        Connect to the slave server that runs local object in isolated context.
        :return:
        """
        return self._dfract_slave

    @property
    def dfract_uuid(self):
        return self._dfract_uuid

    def register_adjunct_objects(self):
        pass
