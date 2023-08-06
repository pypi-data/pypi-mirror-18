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
import logging
import os
import re

import Pyro4

##
## WE USE THE MACHINE ID TO IDENTIFY THIS NODE IN VARIOUS SITUATION (CREATION OF DATASETS / MIRRORING)
##

MACHINE_ID = "01d01d01d01d01d01d01d01d01d"

if os.path.exists("/etc/machine-id"):
    MACHINE_ID = open("/etc/machine-id").read().strip()
else:
    logging.warning(
        "Could not find machine id ! Your machine id may collide with other machines when publishing datasets and datastreams.\n")

# SPLIT THE ID IN A SECRET AND PUBLIC PART TO PROTECT PASSWORDS
MACHINE_SALT = MACHINE_ID[1::2]
MACHINE_ID = MACHINE_ID[::2]

##
## DEFAULT CONFIG FOR DFRACT
##

DEFAULT_HMACKEY = "0123456789abcdef" + MACHINE_SALT  # < CHANGE ME

DEFAULT = {
    "log-level": "DEBUG",
    "config-file": "~/.config/dfract.json",
    "persistent-storage": "mongodb://dfract-mongo:27017/",
    "pyro-ns": "dfract-pyro-ns:22222",
    "pyro-gw": "localhost:9999",
    "pyro-hub-port": 57260,
    "pyro-hmackey": DEFAULT_HMACKEY,
    "docker-image": "dfract-hub:ready-latest",
    "publish-to": None,  # automatically publish new public datasets and datastreams to this address
    "public-ip": None,  # to publish datasets - we may need a public IP associated with this server
    "machine-id": MACHINE_ID,
    "use-docker": True,  # use docker to run datasets
    "mode": "docker",  # use docker to run datasets
    "resolve-docker-names": True,
# should we manually try to resolve name container ip via docker (set True if you are usigng host network)
    "host-static-folder": os.path.expanduser("~/static"),
    "docker-extra-args": "",
    "docker-network": None,
    "docker-devices": ["/dev/video0", "/dev/video1", "/dev/video2", "/dev/video3", "/dev/video4", "/dev/video5",
                       "/dev/video6",
                       "/dev/usb"
                       ],  # devices that datasets / datastreams may eventually access on the node
    "autostart": True,
# if auto start is true then if the client fails to connect it will attempt to start a server (if the dfract server is assumed local)
    "datastream-mode": "thread"
}

DOCKER_HOST_NETWORK = {
    "Bridge": "",
    "HairpinMode": False,
    "LinkLocalIPv6Address": "",
    "LinkLocalIPv6PrefixLen": 0,
    "Ports": {},
    #            "SandboxKey": "/var/run/docker/netns/default",
    "SecondaryIPAddresses": None,
    "SecondaryIPv6Addresses": None,
    "EndpointID": "",
    "Gateway": "",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "IPAddress": "",
    "IPPrefixLen": 0,
    "IPv6Gateway": "",
    "MacAddress": "",
    "Networks": {
        "host": {
            "IPAMConfig": None,
            "Links": None,
            "Aliases": None,
            #                   "NetworkID": "8ab09755afae2a37fa3e1d9c6d600905000b23b5b8144a075beb19a7916dedf0",
            #                   "EndpointID": "61e44e45bf043a90342950429466be7b887a5ad9f225ff8617d56347885b6063",
            "Gateway": "",
            "IPAddress": "",
            "IPPrefixLen": 0,
            "IPv6Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "MacAddress": ""
        }
    }
}

CONFIG = {
}


def get(key, default=None):
    return CONFIG.get(key,
                      os.environ.get("DFRACT_" + key.upper().replace('-', '_'),
                                          (default if default is not None else DEFAULT.get(key))))


def keys():
    return sorted(list(set(CONFIG.keys()).union(set(DEFAULT.keys()))))


##
## UPDATE CONFIG WITH CONFIG-FILE DATA
##

_cf = get("config-file")
if os.path.exists(_cf):
    CONFIG = json.loads(open(_cf).read())

##
## CONFIG FOR PYRO4
##

Pyro4.config.COMPRESSION = False

Pyro4.config.HOST = "0.0.0.0"
Pyro4.config.NS_HOST = get("pyro-ns").split(":")[0]
Pyro4.config.NS_PORT = int(get("pyro-ns").split(":")[1])
Pyro4.config.SERIALIZER = "serpent"
Pyro4.config.SERIALIZERS_ACCEPTED = ["json", "serpent"]

Pyro4.config.COMMTIMEOUT = 4
Pyro4.config.SERVERTYPE = "multiplex"

logging.getLogger().setLevel(get("log-level"))
from dfract import log

log.enable_pretty_logging(stream = get("log-file"))

if get("resolve-docker-names") and get("pyro-ns"):
    from . import docker_utils

    try:
        CONFIG["pyro-ns"] = docker_utils._dock_get_ip(get("pyro-ns").split(":")[0]) + ":" + get("pyro-ns").split(":")[1]
    except Exception as e:
        logging.debug(repr(e))

if get("resolve-docker-names"):
    from . import docker_utils

    try:
        persistent_storage_host = re.match('mongodb://([^:]*):([0-9]+)/', get("persistent-storage"))
        if persistent_storage_host is not None:
            logging.debug("mongo storage:" + get("persistent-storage"))
            persistent_storage_host = persistent_storage_host.groups()[0]
            CONFIG["persistent-storage"] = get("persistent-storage").replace(persistent_storage_host,
                                                                             docker_utils._dock_get_ip(
                                                                                 persistent_storage_host))
        logging.debug("mongo storage:" + get("persistent-storage", ""))
    except Exception as e:
        logging.debug(repr(e))

for e in keys():
    if get("show-config"):
        logging.debug("config: %s : %r" % (e, get(e)))
