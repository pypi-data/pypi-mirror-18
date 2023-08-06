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
try:
    import docker
except:
    docker = None
import functools
import os
import re

__dock_shared_client = None

if docker is not None:
    def _dock_shared_client():
        global __dock_shared_client
        if __dock_shared_client is None:
            __dock_shared_client = docker.Client(os.environ.get("DOCKER_HOST"))
        return __dock_shared_client


    def cfilters0(name, dc):
        if dc is None:
            dc = _dock_shared_client()
        return dc.containers(all=True, filters={"name": name})[0]


    def cfilters1(name, dc):
        if dc is None:
            dc = _dock_shared_client()
        rl = [c for c in dc.containers(all=True) if name in [n.strip("/") for n in c["Names"]]]
        if not rl:
            return None
        return rl[0]


    def _dock_get_ip(name, dc=None):
        try:
            return cfilters1(name, dc)["NetworkSettings"]["Networks"].values()[0]["IPAddress"]
        except:
            raise ValueError


    def _is_running(name, dc=None):
        try:
            return cfilters1(name, dc)["Status"].lower().startswith("up ")
        except:
            raise ValueError


    def _dock_get_by_name(name, dc=None):
        if dc is None:
            dc = _dock_shared_client()
        return cfilters1(name, dc)


    def _dock_get_by_matching(name, dc=None):
        if dc is None:
            dc = _dock_shared_client()
        return filter(lambda x: functools.reduce(lambda b, y: b or re.match(name, y), x["Names"], False),
                      dc.containers(all=True))
