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
import optparse
import os
import pwd
import re
import sys
import traceback

import Pyro4
from dfract import config
from dfract import docker_utils
from dfract.mixins import autostart
from dfract.mixins import callback_management
from dfract.mixins import datasets_commands
from dfract.mixins import datastreams_commands
from dfract.mixins import docker_isolation
from dfract.mixins import help
from dfract.mixins import ipc
from dfract.mixins import linked_data
from dfract.mixins import objects
from dfract.mixins import tagging
from dfract.persistency import PersistentDict
from dfract.specification import USER_RE

from . import utils


def validate_context(context):
    "Validate context"
    assert (re.match(USER_RE, context.get("user", "")))


ARG_TRANSFORM_MAP = {
    "uuid": lambda s, c, v: s._resolve_tag_to_uuid(c, v),
    "uuid_or_expr": lambda s, c, v: s._resolve_tag_to_uuid(c, v),
    "expr_or_udid": lambda s, c, v: s._resolve_tag_to_uuid(c, v)
}


def communication_safe(meth):
    arg_names = utils.methodargs(meth)
    assert (arg_names[0] == 'self')
    assert (arg_names[1] == 'context')
    arg_names = arg_names[2:]

    if sys.version[0] == '2':
        @functools.wraps(meth)
        def new_meth(context, *args, **kwargs):
            try:
                validate_context(context)
                targs = tuple((ARG_TRANSFORM_MAP.get(x[0], lambda s, c, v: v)(meth.im_self, context, x[1]) for x in
                               zip(arg_names, args[:len(arg_names)])))
                args = targs + args[len(arg_names):]
                return meth(context, *args, **kwargs)
            except Pyro4.errors.CommunicationError:
                return {"$error": "error communicating with dataset service"}
    else:
        @functools.wraps(meth)
        def new_meth(context, *args, **kwargs):
            try:
                validate_context(context)
                targs = tuple(ARG_TRANSFORM_MAP.get(x[0], lambda s, c, v: v)(meth.__self__, context, x[1]) for x in
                              zip(arg_names, args[:len(arg_names)]))
                args = targs + args[len(arg_names):]
                return meth(context, *args, **kwargs)
            except Exception as e:
                se = str(traceback.format_exc() + "\n")
                sys.stderr.write(se)
                return {"$error": str(e) + se}

    return new_meth


@Pyro4.expose
class DataHubServer(
    ipc.Mixin,
    docker_isolation.Mixin,
    help.Mixin,
    objects.Mixin,
    datasets_commands.Mixin,
    datastreams_commands.Mixin,
    callback_management.Mixin,
    tagging.Mixin,
    autostart.Mixin,
    linked_data.Mixin,
):
    """
    A DFRACT DataHub Server representing one server node in the distributed dataset network.

    This node is currently implemented using Pyro.
    A dfract datahub is normally in charge of managing objects running on a local cluster.

    The role of the server is also to act as a registry of dataset/datastreams and to memorise/persist how user are
    connected to datasets via eventhandlers. So that event happening to datasets/datastreams can be pushed toward their
    right destination.

    The notifications pushed by the hub are sent by the server as fire-and-forget. There is no warranty that any
    notification-handler will be called. It is simply a best effort strategy.

    At current stage:
    Although access to the server is password protected this server is only meant to be accessible in fully trusted
    environment and to be only directly accessible by administrators.
    """

    def __init__(self, daemon=None):
        if daemon is None:
            daemon = Pyro4.Daemon(port=config.get("pyro-hub-port"))
        self._pyro_ns = None
        self._dfract_client = None
        self.daemon = daemon
        self._running = True

        ## all the following collection are indexed by uuid
        ## user / versioned ids (as we must
        ## allow two concurrent versions of a dataset / datastreams to be ran at the same time
        ## most of the time the exact version cannot be clarified from the expression
        ## and the final versionned id will be supplied by the dataset it self. As we may not want
        ## to block for that long before to use the dataset we also suggest to give a uuid to the dataset.
        ##
        ## This lead to the facct that dataset shouldsearchable by
        ##  uuid                    uuid
        ##  udid = expressionhash?  unique dataset id
        ##  ucid = contenthash ?    unique content id
        ## and obviously filtered by owner

        ##
        ## Actual list of the objects that we should be able to serve
        ##
        # self.instances = PersistentDict("instances")        # meta updating the dataset meta

        ##
        ## Metadata
        self._pending_meta = {}  # meta suggested but not yet acceoted by owner/reviewer

        self._updated_meta = PersistentDict("datasets_meta")  # meta updating the dataset meta

        ##
        ## Indexed by tag
        self._tags = PersistentDict("_tags")  # used to provide alias to local and remote dataset.
        self._rev_tags = PersistentDict("_revtags")  # used to provide alias to local and remote dataset.

        ## Unversioned static id to UUID
        ## Link to UDID to UUID
        self._objects_udid = PersistentDict("objects_udid")

        ## Link to semantic link uri to UUID
        self._rel_uri = PersistentDict("datasets_rel_uri")

        self._objects = {}  # actual proxy object to the collection

        for x in dir(self):
            if x[0] != '_':
                v = getattr(self, x)
                if callable(v) and hasattr(v, "__name__") and (
                        v.__doc__ is None or not v.__doc__.startswith("INTERNAL")):
                    setattr(self, x, communication_safe(v))

        # Sync current_URIs with running objects
        if docker_utils.docker and self._use_docker():
            self.docker = docker_utils._dock_shared_client()
            # look for existing / persistent  datasets datastreams
            self._find_running_datasets()

    def _use_docker(self):
        return str(config.get("use-docker")).upper() in ["TRUE" or "1"]

    @Pyro4.expose
    def ping(self):
        """INTERNAL"""
        return "pong"


    ##
    ## DATASETS/DATASTREAMS
    ##

    def __find_master_datahub(self):
        """
        Connects to default target host and returns a proxy to it.
        """
        if self._dfract_client is None:
            # NOTE: import done here to avoid eventual circular import between server and client
            from dfract.client import DFractClient
            self._dfract_client = DFractClient()
        return self._dfract_client()

    def _datasets_direct_invoke_uuid(self, context, uuid):
        """
        Returns a the object for a dataset matching a uuid.

        (implies that the conversions expression to uuid has already been done..)
        """
        logging.debug("_datasets_docker_invoke %r %r" % (context, uuid))

        if not self._slave_is_running(context, uuid):
            self._slave_start(context, uuid)
            self._datasets_wait_for_slave_start(context, uuid)

        if not self._objects.get(uuid):
            logging.debug("object %s link to URI: %s" % (uuid, self.ipc_get_service_address(uuid)))
            self._objects[uuid] = Pyro4.Proxy(self.ipc_get_service_address(uuid))

        return self._objects[uuid]

    def datasets_clean_unused(self, context):
        # FIXME: THIS IS UNFINISHED
        for r in self._docker_containers():
            # if "dfract.x" in  r["Labels"] :
            r.detach()

    ## ================================================================================
    ## TAG MANAGEMENT
    ## ================================================================================
    def _solve_dataset_reference(self, key):
        if key.startswith("udid:"):
            key = self._objects_udid[key[5:]]
        if key.startswith("uuid:"):
            key = key[5:]
        if re.match("([0-9a-f]{24,32})", key):
            return key
        raise ValueError

    ## ================================================================================
    ## BASE SECURITY MODEL
    ## ================================================================================
    def _accesscontrol_approve(self, context, key, mode="r"):
        """
        Indicate whether the logged user can access or not the specific datasets.
        """
        # todo : self use metadata
        # todo: change rest of the code so that can access work with all types of objects
        if mode == "r":
            return (self._updated_meta[key]["owner"] == context["user"]) or self._datasets_meta[key]["public"]
        elif mode == "w":
            return (self._updated_meta[key]["owner"] == context["user"])
        else:
            return False

    ## ================================================================================
    ## MANAGEMENT OF THE SERVICE
    ## ================================================================================

    # def map_service(self, context, expr):
    #     """
    #     Creates a new dataset by applying a transform and eventually store/cache it for reuse.
    #     """
    #     assert (False)

    def _get_pyro_ns(self):
        if self._pyro_ns is None:
            if config.get("pyro-ns"):
                self._pyro_ns = Pyro4.Proxy("PYRO:%s@%s" % (Pyro4.constants.NAMESERVER_NAME, config.get("pyro-ns"),))
            if self._pyro_ns is None:
                self._pyro_ns = Pyro4.locateNS()
        return self._pyro_ns

    def server_run(self, context, _register_hub=True):
        """
        Starts the dfract server process.
        """
        logging.info("DFRACT daemon starting")

        if _register_hub:
            uri = self.daemon.register(self, "datahub")
            self._get_pyro_ns().register("http.DataHub", uri)
            logging.info("http.Datahub registered in NS to " + str(uri))

        retry = 10
        while retry > 0:
            try:
                self.daemon.requestLoop(loopCondition=lambda: self._running)
            except Exception as e:
                retry -= 1
                traceback.print_exc(e)


if __name__ == "__main__":
    """
    DFRACT server can be used from the command line.

    CLI interface at this stage is minimal but is meant to mimic the object
    interface. A CLI client will also be provided to allow to run command an
    existing server.
    """
    Pyro4.config.HOST = config.get("hostname", os.uname()[1])
    logging.info("Pyro host set to " + Pyro4.config.HOST)
    dh = DataHubServer()

    cmd = ((sys.argv[1] + "_" + sys.argv[2]) if len(sys.argv) > 2
           else (sys.argv[1] if len(sys.argv) > 1 else "server_run"))

    try:
        f = getattr(dh, cmd)
    except AttributeError:
        logging.warning("Could not find command %s" % (cmd,))
        f = getattr(dh, "help")

    args = sys.argv[3:]
    options = {}

    query_context = {}
    user = pwd.getpwuid(os.geteuid()).pw_name
    query_context["user"] = "unix:" + user + "@" + config.get("machine-id")

    if False:
        parser = optparse.OptionParser()
        # parser.add_option("-v", "--file", dest="filename",
        #                  help="write report to FILE", metavar="FILE")

        for ci in getattr(f, "cli_options", []):
            parser.add_option(ci[0], ci[1], **ci[2])
        # allow to manually specify user
        (options, args) = parser.parse_args(argv[3:])

    # print cmd, f, args
    res = f(query_context, *args, **options)
    if res:
        if res.encode('ascii') == res:
            utils.pretty_print(res)
        else:
            print(res)
