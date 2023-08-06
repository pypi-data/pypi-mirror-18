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
import base64
import json
import logging
import os
import re
import select
import ssl
import sys
import traceback

import Pyro4
import jinja2
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.web
from dfract import config
from dfract.cache_utils import lru_cache
from tornado import gen

from .utils import b64decode

_nameserver = None
with_cache = True


def get_nameserver(hmac=None):
    global _nameserver
    if config.get("pyro-ns"):
        _nameserver = Pyro4.Proxy("PYRO:Pyro.NameServer@%s" % (config.get("pyro-ns"),))
        return _nameserver
    if not _nameserver:
        _nameserver = Pyro4.locateNS(hmac_key=hmac)
    try:
        _nameserver.ping()
        return _nameserver
    except Pyro4.errors.ConnectionClosedError:
        _nameserver = None
        print("Connection with nameserver lost, reconnecting...")
        return get_nameserver(hmac)


def basic_auth(auth_func=lambda *args, **kwargs: True, after_login_func=lambda *args, **kwargs: None,
               realm='Restricted'):
    def basic_auth_decorator(handler_class):
        def wrap_execute(handler_execute):
            def require_basic_auth(handler, kwargs):
                handler.user = None

                def create_auth_header():
                    handler.set_status(401)
                    handler.set_header('WWW-Authenticate', 'Basic realm=%s' % realm)
                    handler._transforms = []
                    handler.finish()

                auth_header = handler.request.headers.get('Authorization')

                if auth_header is None or not auth_header.startswith('Basic '):
                    create_auth_header()
                else:
                    auth_decoded = base64.decodestring(auth_header[6:])
                    user, pwd = auth_decoded.split(':', 2)

                    if auth_func(user, pwd):
                        after_login_func(handler, kwargs, user, pwd)
                        handler.user = user
                    else:
                        create_auth_header()

            def _execute(self, transforms, *args, **kwargs):
                require_basic_auth(self, kwargs)
                return handler_execute(self, transforms, *args, **kwargs)

            return _execute

        handler_class._execute = wrap_execute(handler_class._execute)
        return handler_class

    return basic_auth_decorator


SITE_URL = "https://dfract.io/"


## extra auth
class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(
                redirect_uri=SITE_URL + '/auth/google',
                code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
        else:
            yield self.authorize_redirect(
                redirect_uri=SITE_URL + '.com/auth/google',
                client_id=self.settings['googleconte_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


def check_credentials(user, pwd):
    return user == 'foo'


environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
environment.filters['enumerate'] = enumerate
environment.filters['len'] = len

REWRITES = {
    #    ("GET", "/"): (homeController),
    ("GET", "/dyn/datasets/([^/]+)/$"): lambda m: ("http.DataHub", "datasets_dyn_list", [m[0]]),
    ("GET", "/dyn/datasets/([^/]+)/([^/]+)/$"): lambda m: (
    "http.DataHub", "datasets_dyn_get", [m[0], m[1], "base64"], "image/png"),
    ("GET", "/dyn/datastreams/([^/]+)/$"): lambda m: ("http.DataHub", "datastreams_dyn_list", [m[0]]),
    ("GET", "/dyn/datastreams/([^/]+)/([^/]+)/$"): lambda m: (
    "http.DataHub", "datastreams_dyn_get", [m[0], m[1], "base64"], "image/png"),
    ("GET", "/datasets/([^/]+)/$"): lambda m: ("http.DS-" + m[0] + "),keys"),
    ("GET", "/datasets/$"): ("http.DataHub", "datasets_list"),
    ("POST", "/datasets/$"): ("http.DataHub", "datasets_create"),
    ("DELETE", "/datasets/$"): ("http.DataHub", "datasets_delete"),
    ("PUT", "/datasets/$"): ("http.DataHub", "datasets_alias"),

    ("GET", "/datastreams/$"): ("http.DataHub", "datastreams_list"),
    ("POST", "/datastreams/$"): ("http.DataHub", "datastreams_create"),
    ("DELETE", "/datastreams/$"): ("http.DataHub", "datastreams_delete"),
    ("PUT", "/datastreams/$"): ("http.DataHub", "datastreams_alias"),
}


def route_rewriter(method, path):
    for r in REWRITES.items():
        if r[0][0] == method:
            matches = re.match(r[0][1], path)
            if matches:
                if callable(r[1]):
                    return r[1](matches.groups())
                else:
                    return r[1][:]

    return method, path


def singlyfy_parameters(parameters):
    """
    Makes a cgi-parsed parameter dictionary into a dict where the values that
    are just a list of a single value, are converted to just that single value.
    """
    for key, value in parameters.items():
        if isinstance(value, (list, tuple)) and len(value) == 1:
            parameters[key] = value[0]
    return parameters


class homeController(tornado.web.RequestHandler):
    """
    Return the homepage and a list of link to datasets.
    FIXME:
        - datasets should be implemented with pager in AJAX later.
        - auth may be required to see some datasets - we need to make this obvious to the user.
    """

    def get(self):
        context = {'user': 'anonymous'}
        dfract = {}
        datasets = get_proxy.with_cache(with_cache)(resolve_object("http.DataHub"))._object_list(context)
        self.write(environment.get_template("dfract-home.html").render({'config': config,
                                                                        'dfract': dfract,
                                                                        'datasets': datasets,
                                                                        'context': context}).encode('utf8'))
        self.finish()


class adminConfigController(tornado.web.RequestHandler):
    def get(self):
        dconfig = dict([(k, config.get(k)) for k in config.keys() if k[0] != '_'])
        dfract = {}
        context = {}
        self.write(environment.get_template("dfract-adminconfig.html").render({'config': dconfig,
                                                                               'dfract': dfract,
                                                                               'context': context}).encode(
            'utf8'))
        self.finish()


@lru_cache
def get_proxy(uri):
    logging.info("Creating proxy for " + str(uri))
    return Pyro4.Proxy(uri)


@lru_cache
def resolve_object(object_name):
    uri = nameserver.lookup(object_name)
    return uri


@basic_auth(check_credentials)
class proxyController(tornado.web.RequestHandler):
    def prepare(self):
        if getattr(self, "user", None) is None:
            self.user = "anonymous"

        context = {
            "paginate": True,
            "user": "web-auth:" + self.user + "@" + config.get("machine-id")
        }

        args = [context]
        kwargs = {k: ''.join(v) for k, v in self.request.arguments.iteritems()}
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

        mimetype = "application/json"

        rrw = route_rewriter(self.request.method, self.request.uri[3:])
        obj, meth = rrw[0], rrw[1]
        if (len(rrw) >= 3):
            args += rrw[2]
        if (len(rrw) >= 4):
            mimetype = rrw[3]

        logging.debug(self.request.uri)
        logging.debug("%r %r %r %r" % (obj, meth, args, kwargs))

        uri = resolve_object.with_cache(with_cache)(obj)
        proxy = get_proxy.with_cache(with_cache)(uri)

        # get proxy object and method
        logging.debug(proxy)

        res = getattr(proxy, meth)(*args, **kwargs)
        if mimetype == "application/json":
            res = json.dumps(res)
        else:
            if isinstance(res, dict):
                # probably an error
                mimetype == "application/json"
                res = json.dumps(res)
            else:
                res = b64decode(res)
            # pass

        self.set_header('Content-Type', mimetype)

        self.finish(res)
        #self.finish("OK")

        try:
            pass
        except:
            self.write_error("error")

    def get(self):
        pass


@basic_auth(check_credentials)
class webProxyController(tornado.web.RequestHandler):
    def prepare(self):
        if getattr(self, "user", None) is None:
            self.user = "anonymous"

        context = {
            "paginate": True,
            "user": "web-auth:" + self.user + "@" + config.get("machine-id")
        }

        args = [context]
        kwargs = {k: ''.join(v) for k, v in self.request.arguments.iteritems()}
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

        rrw = route_rewriter(self.request.method, self.request.uri[4:])
        obj, meth = rrw[0], rrw[1]
        if (len(rrw) >= 3):
            args += rrw[2]
        if (len(rrw) >= 4):
            mimetype = rrw[3]

        uri = resolve_object.with_cache(with_cache)(obj)
        proxy = get_proxy.with_cache(with_cache)(uri)
        logging.debug(proxy)

        res = getattr(proxy, meth)(*args, **kwargs)

        self.write(environment.get_template("dfract-" + meth.replace('_', '-') + ".html").render({'config': config,
                                                                                                  'res': res,
                                                                                                  'request': self.request,
                                                                                                  'context': context}).encode(
            'utf8'))

        self.finish("")

    def get(self):
        pass


@gen.coroutine
def handlePyroEvents():
    while True:
        try:
            s, _, _ = select.select(pyro_daemon.sockets, [], [], 0.01)
        except select.error:
            s = False
        if s:
            try:
                self.pyro_daemon.events(s)
            except:
                traceback.print_exc()
                sys.exit(-1)
            w = False
        else:
            # no more events, stop the loop, we'll get called again soon anyway
            break

        # Allow other processing to happen
        yield gen.sleep(0.001)


application = tornado.web.Application([
    (r'/', homeController),
    (r'/config/', adminConfigController),
    (r'/v0/(.+)', proxyController),
    (r'/web/(.+)', webProxyController)
])

if __name__ == '__main__':
    ns = None
    global nameserver
    from optparse import OptionParser

    Pyro4.config.SERIALIZER = "serpent"  # we only talk json through the http proxy
    Pyro4.config.COMMTIMEOUT = 120  # limit wait to 2minutes
    Pyro4.config.LOGWIRE = False

    Pyro4.config.SERIALIZERS_ACCEPTED = ["json", "serpent"]

    parser = OptionParser()
    parser.add_option("-H", "--host", default="0.0.0.0", help="Bind IP")
    parser.add_option("-p", "--port", default=1443, help="Port to listen on")
    options, args = parser.parse_args(sys.argv[1:])

    port = 1443
    # pyro_app.hmac_key = "" # (options.pyrokey or "").encode("utf-8")
    # pyro_app.gateway_key = ""# (options.gatewaykey or "").encode("utf-8")
    # pyro_app.ns_regex = options.expose
    # pyro_app.comm_timeout = Pyro4.config.COMMTIMEOUT = options.timeout
    # if pyro_app.ns_regex:
    #    print("Exposing objects with names matching: ", pyro_app.ns_regex)
    # else:
    #    print("Warning: exposing all objects (no expose regex set)")

    logging.debug("Searching nameserver")
    try:
        ns = get_nameserver()  # (hmac=pyro_app.hmac_key)
        logging.info("Found name server at: %s ", ns._pyroUri)
    except Pyro4.errors.PyroError as e:
        logging.warning("Not yet connected to a name server." + repr(e))

    nameserver = ns

    if not os.path.exists("test/test.key"):
        os.system(
            "openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout test/test.key -out test/test.crt   -subj \"/C=UK/ST=London/L=London/O=WIDE IO/OU=Test/CN=WIDE IO TEST/emailAddress=test@wide.io\"")


    ssl_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_ctx.load_cert_chain("test/test.crt", "test/test.key")
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_OPTIONAL

    http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_ctx)

    http_server.listen(port)

    logging.info("Test server by running curl -X ...\n")
    io_loop = tornado.ioloop.IOLoop.instance()
    # io_loop.add_callback(handlePyroEvents)
    io_loop.start()
