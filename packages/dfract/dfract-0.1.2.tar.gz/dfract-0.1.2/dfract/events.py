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
import datetime
import json
from six import string_types

from dfract import serialization
from dfract.jobqueue import request_get
from dfract.utils import _gen_uuid


class EventHandler(object):
    """
    This is a persistent event handler.

    As event passing generally involves contacting remote object, calling
    event will be done in an asynchronous way with a job queues.

    NOTE: Only remote objects can be called as we expect objects to have endpoint in the datahub.
    Obviously this allow simple serialisations.
    Here the event handler assumes that it operates at level 4 by doing
    http requests to the right elements.
    
    NOTE: This imply we will notify all the datasets/streams that need to be notified
    but that it may be take time to propagate.
    """

    def __init__(self, events=["add", "remove", "update"]):
        self._events = events
        for event in self._events:
            setattr(self, "_on_" + event, [])
            self._inject_eh_for_event(event)

    def _inject_eh_for_event(self, event):
        def add_on_event(url_or_func, data=None, uuid=None):
            if uuid is None:
                uuid = _gen_uuid()
            eh_list = getattr(self, "_on_" + event)
            created = last_ping = datetime.datetime.now()
            last_triggered = None
            eh_list.append([uuid, url_or_func, data, created, last_ping, last_triggered])
            return uuid

        def ping_on_event(uuid):
            """
            Use to record last ping from callback client.

            :param uuid:
            :return:
            """
            eh_list = getattr(self, "_on_" + event)
            last_ping = datetime.datetime.now()
            for i in range(len(eh_list)):
                if eh_list[i][0] == uuid:
                    eh_list[i][4] = last_ping

        def del_on_event(uuid):
            """
            Remove one of the record from the client.

            :param uuid:
            :return:
            """
            eh_list = getattr(self, "_on_" + event)
            for i in range(len(self._on_add)):
                if eh_list[i][0] == uuid:
                    del eh_list[i]
                    break


        def on_event(msg):
            """
            Call on update handlers
            """
            eh_list = getattr(self, "_on_" + event)
            for i in range(len(eh_list)):
                data = eh_list[i][2]
                if not callable(eh_list[i][1]):
                    request_get.delay(eh_list[i][1], msg)
                    eh_list[i][5] = datetime.datetime.now()
                else:
                    if data is None:
                        data = {}
                    eh_list[i][1](msg, **data)

        setattr(self, "add_on_" + event, add_on_event)
        setattr(self, "ping_on_" + event, ping_on_event)
        setattr(self, "del_on_" + event, del_on_event)
        setattr(self, "on_" + event, on_event)

    def dumps(self):
        # FIXME: Change to internal serialization
        to_serialize = {}
        for event in self._events:
            to_serialize["on_" + event] = getattr(self, "_on_" + event, [])

        return json.dumps(
            serialization.smj_dumpx(to_serialize)
        )

    def loads(self, config):
        if isinstance(config, string_types):
            config = serialization.smj_loadx(json.loads(config))
        for event in self._events:
            setattr(self, "_on_" + event, config["on_" + event])
