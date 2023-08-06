#!/usr/bin/env python
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

import functools
import logging
import os
import sys

import Pyro4
from dfract import config
from dfract import docker_utils
from dfract import utils


def dataset_client(url):
    return Pyro4.proxy(url)


class DFractClient():
    def __init__(self, host=None):
        self.context = {}
        try:
            user = os.getlogin()
        except:
            user = str(os.getuid())

        self.context["user"] = "unix:" + user + "@" + config.get("machine-id")

        default_host = host
        if default_host is None:
            logging.debug("Automatically trying to infer location of dfract-hub")
            if config.get("use-docker"):
                try:
                    if not docker_utils._is_running("dfract-hub"):
                        raise ValueError
                    default_host = docker_utils._dock_get_ip("dfract-hub")
                    logging.debug("Found running container serving dfract server")
                except:
                    default_host = "localhost"
            else:
                default_host = "localhost"

        uri = "PYRO:datahub@%s:%s" % (default_host, config.get("pyro-hub-port"))

        logging.debug("Connecting to datahub %s" % (uri,))
        self.dh = Pyro4.Proxy(uri)
        # logging.debug("Pinging %s" % (uri,))
        # self.dh.ping()
        # logging.debug("Successful")

    def __getattr__(self, item):
        x = getattr(self.dh, item)
        x = functools.partial(x, self.context)
        return x


def main():
    Pyro4.config.HOST = config.get("hostname", os.uname()[1])
    logging.info("Pyro host set to " + Pyro4.config.HOST)

    args = sys.argv[3:]
    options = {}

    if False:
        parser = OptionParser()
        for ci in getattr(f, "cli_options", []):
            parser.add_option(ci[0], ci[1], **ci[2])
        # allow to manually specify user
        (options, args) = parser.parse_args(sys.argv[3:])

    cmd = ((sys.argv[1] + "_" + sys.argv[2]) if len(sys.argv) > 2 else (sys.argv[1] if len(sys.argv) > 1 else "help"))

    dc = DFractClient()

    try:
        f = getattr(dc, cmd)
    except AttributeError:
        logging.warning("Could not find command %s" % (cmd,))
        f = getattr(dc, "help")
    except Pyro4.errors.CommunicationError:
        if config.get("autostart"):
            logging.warning("Autostart is on - Attempting to start the server.")
            os.system("python -m dfract.server server start")
            try:
                dc = DFractClient()
                try:
                    f = getattr(dc, cmd)
                except AttributeError:
                    logging.warning("Could not find command %s" % (cmd,))
                    f = getattr(dc, "help")
            except Pyro4.errors.CommunicationError:
                logging.warning(
                    "Could not communicate with server process. An autostart has been attempted it but I can't communicate with it.")
                sys.exit(-1)
        else:
            logging.warning("Could not communicate with server process. Is it running ?")
            sys.exit(-1)

    res = f(*args, **options)
    try:
        if (type(res) in [list, dict]) or (res.encode('ascii') == res):
            utils.pretty_print(res)
            return
    except:
        pass
    if hasattr(res, "encode"):
        res = res.encode('utf8')
    sys.stdout.write(res)


if __name__ == "__main__":
    main()
