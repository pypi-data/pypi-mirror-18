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


"""
autoimp2 -- Import all modules, load them lazily at first use.

Public domain, Connelly Barnes 2006.  Works with Python 2.1 - 2.6.


Specific version of autoimp for PyCVF.

For reference about autoimp check normal "autoimp.py"

"""

__version__ = '1.0.4pycvf'
__all__ = ['reload']  # Lazily imported modules will go here

# TODO: .PY .pY .Py, various capitalizations of Python modules/packages.
# TODO: Test a whole lot on examples of lots of libraries.  Also test with
#      the Python lib unit tests.

# Use leading underscores on values used internally by this module so
# we don't get name conflicts with imported modules (which go in our
# globals() namespace).

import sys

if sys.version[0] == "2":
    import __builtin__ as _builtin
else:
    import builtins as _builtin

import imp as _imp
import os as _os
import sys as _sys
import copy as _copy
import logging

logger = logging.getLogger(__name__)
logger.setLevel("WARNING")

# Modules with names of the form __name__ which are part of Python's lib.
_BUILTIN_SPECIAL_MODULES = '__builtin__ __main__ __future__'.split()

# Modules compiled or dynamically linked with Python binary (using
# _sys.builtin_module_names alone won't work, as 'math' may not be in
# here if math is dynamically linked, and searching sys.path also
# won't work, as this will find 'mathmodule' on Linux but not 'math').
_BUILTIN_COMPILED_MODULES = list(_sys.builtin_module_names) + """
  al array audioop binascii bsddb bz2 cd cmath cPickle crypt cStringIO
  datetime dbm dl errno fcntl fl fm fpectl functional gc gdbm gl grp
  imageop itertools linuxaudiodev math md5 mmap mpz nis operator
  ossaudiodev parser posix pcre pure pwd pyexpat readline regex
  resource rgbimg rotor select sgi sha256 sha512 sha shm signal socket
  spwd strop struct sunaudiodev sv symtable syslog termios thread time
  timing unicodedata xreadlines zipimport zlib
  """.split()

# Extensions known to be Python modules.
_PYTHON_EXTS = ['.py', '.pyc', '.pyo', '.pyw', '.pyd',
                '.dll', '.so', '.ppc.slb', '.carbon.slb', '.macho.slb']

_INIT_PY_NAMES = ['__init__.py', '__init__.pyc', '__init__.pyo']


class _RecursiveLazyModule:
    """
    Proxy class, imports modules and sub-modules automatically.


    Search path will look among the followin directories.
    On the opposite rev search path will try to add some path

    """

    def __init__(self, modname, searchpath=None, revsearchpath=None, lib=None, sname=None):
        # print modname
        logger.debug("_RecursiveLazyModule %s sp=%r rsp=%r" % (modname, searchpath, revsearchpath))
        self.__dict__['__name__'] = modname
        self.__dict__['__sname__'] = sname
        self.__dict__['_autoimp_lib'] = None
        if (searchpath is not None):
            self.__dict__['__searchpath__'] = _copy.copy(searchpath)
        else:
            self.__dict__['__searchpath__'] = None

        if (revsearchpath is not None):
            self.__dict__['__revsearchpath__'] = _copy.copy(revsearchpath)
        else:
            self.__dict__['__revsearchpath__'] = ['']

        self.__set_lib(lib)

    def __set_lib(self, lib):
        # Set the self.__lib attribute to lib.
        n = self.__dict__['__name__']
        sp = self.__dict__.get('__searchpath__')
        rsp = self.__dict__.get('__revsearchpath__')

        def moduleaslazy(mname):
            if (isinstance(_os, (type(mname[1])))):
                return (mname[0], _RecursiveLazyModule(n + "." + mname[0],
                                                       searchpath=sp,
                                                       revsearchpath=rsp,
                                                       lib=None))
            else:
                return mname

        if lib is not None:
            # Share __dict__ with the imported object.
            self.__dict__ = lib.__dict__
            self.__dict__['__searchpath__'] = sp
            self.__dict__['__revsearchpath__'] = rsp
            self.__dict__['_autoimp_lib'] = lib
            self.__dict__ = dict(list(map(moduleaslazy, list(lib.__dict__.items()))))
            self.__dict__['__searchpath__'] = sp
            self.__dict__['__revsearchpath__'] = rsp
            self.__dict__['_autoimp_lib'] = lib
            # print map(lambda x:(x[0],type(x[1])),lib.__dict__.items())
            # p0=_os.path.dirname(self.__dict__['_autoimp_lib'].__file__)
            for xname in [('%s.%s' % (n, r)) for r in
                          [x[:-1] for x in [x for x in self.__dict__['__revsearchpath__'] if x != "."]]]:
                # print xname
                try:
                    if (xname[-1] != "."):
                        xfromlist = xname.split(".")[:-1]
                        xsublib = __import__(xname, fromlist=xfromlist)
                        for x in dir(xsublib):
                            if (not x in self.__dict__):
                                self.__dict__[x] = getattr(xsublib, x)
                except (ImportError, NameError) as e:
                    continue
        else:
            self.__dict__['_autoimp_lib'] = None

    def __load_lib(self):
        ## Try to load the module according to its name
        ## The complicated issue is to guess all the combinatorics of the paths
        ## The name will so it has to be correct
        if self.__dict__.get('__searchpath__'):
            sp = self.__dict__.get('__searchpath__')
            rsp = self.__dict__.get('__revsearchpath__', [''])
            for p in [''] + sp:
                for rp in rsp:
                    try:
                        logger.debug("trying to load %r" % (p + rp + self.__dict__["__name__"],))
                        ns = self.__dict__["__name__"]
                        self.__set_lib(__import__(p + rp + self.__dict__["__name__"],
                                                  fromlist=((p + rp + self.__dict__["__name__"]).split(".")[:-1])))
                        self.__dict__["__name__"] = ns
                        logger.debug("done loading %r" % (p + self.__dict__["__name__"],))
                        return
                    except ImportError as e:
                        logger.debug("error in import : %r" % (e,))
                        pass
            raise Exception(self.__dict__["__name__"] + " : Not found in sp :" + str(sp))
        else:
            self.__set_lib(__import__(self.__name__))

    def __reload__(self):
        if self.__dict__['_autoimp_lib'] is None:
            # If mod has not yet been imported, then only load mod once.
            self.__load_lib()
            return self
        else:
            _reload(self.__dict__['_autoimp_lib'])
            self.__set_lib(self.__dict__['_autoimp_lib'])
            return self

    def __help__(self):
        self.__load_lib()
        return _help(self.__dict__['_autoimp_lib'])

    def __getattr__(self, key):
        # Do the import.
        errors = []
        if self.__dict__.get('_autoimp_lib') is None:
            self.__load_lib()

        lib = self.__dict__['_autoimp_lib']

        # Look up key, is it now found?
        if hasattr(lib, key) and (not isinstance(getattr(lib, key), type(_os))):
            return getattr(lib, key)
        else:
            # print "NHK",lib,key
            # Try importing a sub-module, wrapping it in a lazy import proxy
            if '__searchpath__' not in self.__dict__ or self.__searchpath__ is None:
                self.__searchpath__ = ['']
            for p in self.__searchpath__:
                for rp in self.__dict__['__revsearchpath__']:
                    subname = '%s%s.%s%s' % (p, self.__dict__["__name__"], rp, key)
                    print ("*" + subname)
                    try:
                        fromlist = subname.split(".")[:-1]
                        sublib = __import__(subname, fromlist=fromlist)
                    except ImportError as e:
                        continue
                    # print "subname/sublib/key/base", subname, sublib, key, self.__name__
                    self.__dict__[key] = _RecursiveLazyModule(subname, searchpath=self.__searchpath__,
                                                              revsearchpath=self.__dict__[
                                                                  '__revsearchpath__'])  # , lib=sublib)

                    for xname in [('%s.%s' % (subname, r)) for r in
                                  [x[:-1] for x in [x for x in self.__dict__['__revsearchpath__'] if x != "."]]]:
                        try:
                            if (xname[-1] != "."):
                                xfromlist = xname.split(".")[:-1]
                                # print "MN=", xname
                                xsublib = __import__(xname, fromlist=xfromlist)
                                for x in dir(xsublib):
                                    if (not x in self.__dict__):
                                        self.__dict__[x] = getattr(xsublib, x)
                        except ImportError as e:
                            errors.append(e)
                            continue
                    # print key,self.__dict__[key],"loading ok"
                    return self.__dict__[key]
            # print "Exception ",e
            # print "lazy module content =",dir(self)
            raise AttributeError("'lazymodule' object '%s'/%r has no attribute %r/ SP=%r, import errors=%r" % (
                self.__name__, lib, key, self.__searchpath__, [x for x in errors if x != key]))

    def __setattr__(self, key, value):
        # Import the module if user tries to set an attribute.
        if key == "__dict__":
            return super(_RecursiveLazyModule, self).__setattr__(key, value)
        if self.__dict__.get('_autoimp_lib') is None:
            self.__load_lib()
        self.__dict__[key] = value

    def __call__(self, *args, **kwargs):
        if self.__dict__['_autoimp_lib'] is None:
            self.__load_lib()
        lib = self.__dict__['_autoimp_lib']
        # print self.__dict__['__name__']
        return getattr(lib, "__call__")(*args, **kwargs)
        # raise TypeError("'lazymodule' object is not callable")


def _add_module_if_pymodule(L, path, modname, ext, zipnames=None):
    """
    Add module name to list L if it is a Python module.
    """
    mods = [modname]

    # For 'Xmodule.ext', trim off 'module' and import remaining name.
    if modname.lower().endswith('module'):
        mods.append(modname[:len(modname) - len('module')])

    for mod in mods:
        # Check if the file is clearly a Python source file.
        if ext in _PYTHON_EXTS:
            L.append(mod)
        else:
            if zipnames is None:
                modfull = _os.path.join(path, modname + ext)
                if _os.path.isdir(modfull):
                    for init_py in _INIT_PY_NAMES:
                        if _os.path.exists(_os.path.join(modfull, init_py)):
                            L.append(mod)
                            break
            else:
                for init_py in _INIT_PY_NAMES:
                    if (modname + '/' + init_py in zipnames or
                                        modname + '\\' + init_py in zipnames):
                        L.append(mod)
                        break


def _list_modules_in_path(path):
    """
    Return list of all modules in filesystem path.
    """
    ans = []
    for filename in _os.listdir(path):
        (pre, ext) = _os.path.splitext(filename)
        _add_module_if_pymodule(ans, path, pre, ext)
    return ans


def _list_modules_in_zip(zipname):
    """
    Return list of all modules in zip file with filename zipname.
    """
    import zipfile
    z = zipfile.ZipFile(zipname, 'r')
    zipnames = {}
    for filename in z.namelist():
        zipnames[filename] = None
    ans = []
    for filename in zipnames:
        filename = filename.rstrip('/').rstrip('\\')
        if '/' not in filename and '\\' not in filename:
            (pre, ext) = _os.path.splitext(filename)
            _add_module_if_pymodule(ans, zipname, pre, ext, zipnames)
    return ans


def _all_modules():
    """
    Return list of all module names to import, from sys.path.
    """
    ans = []
    for path in _sys.path:
        if path == '':
            path = _os.curdir
        if _os.path.isdir(path):
            ans.extend(_list_modules_in_path(path))
        elif (_os.path.splitext(path)[1].lower() == '.zip'
              and _os.path.exists(path)):
            ans.extend(_list_modules_in_zip(path))
        else:
            pass

    # Other modules compiled into the Python binary (for Python <= 2.5).
    extras = _sys.builtin_module_names
    tried = {}
    for x in ans:
        tried[x] = None
    for x in _BUILTIN_COMPILED_MODULES:
        if x not in tried:
            tried[x] = None
            try:
                _imp.find_module(x)
                ans.append(x)
            except ImportError:
                pass

    # Remove duplicates.
    d = {}
    for x in ans:
        d[x] = None
    return list(d.keys())


def _import_all():
    """
    Lazy import all modules found by _all_modules().
    """
    for mod in _all_modules():
        # Do not replace existing builtins, such as repr().
        # print mod
        if (not hasattr(_builtin, mod) and (not mod.startswith('_') or
                                                    mod in _BUILTIN_SPECIAL_MODULES)):
            d = globals()
            d[mod] = _RecursiveLazyModule(mod)
            __all__.append(mod)


def import_all_as_context(context, temppath=None, revsearchpath=None):
    """
    Lazy import all modules found by _all_modules().
    """

    if temppath:
        temppath = _copy.copy(temppath)
        temppath.reverse()
        pathsav = _copy.copy(_sys.path)
        # _sys.path=[]
        for t in temppath:
            if (t):
                if (t[-1] == "."):
                    t = t[:-1]
                try:
                    m = __import__(t, fromlist=t.split('.')[-1])
                    mp = m.__path__
                    del m
                    for p in mp:
                        _sys.path.insert(0, p)
                        # print p
                except:
                    pass
        temppath.reverse()
    contextall = _copy.copy(list(context["__all__"]))
    # print  _all_modules()

    for mod in _all_modules():
        # Do not replace existing builtins, such as repr().
        if (not hasattr(_builtin, mod) and (not mod.startswith('_') or
                                                    mod in _BUILTIN_SPECIAL_MODULES)):
            d = context
            # sys.stdout.flush()
            d[mod] = _RecursiveLazyModule(mod, temppath, revsearchpath)  # _sys.path)
            # print mod,d[mod]
            contextall.append(mod)
    if temppath:
        _sys.path = pathsav


def _export_builtins():
    """
    Export all lazily imported modules to the __builtin__ namespace.
    """
    for k in __all__:
        setattr(_builtin, k, globals()[k])


_reload = _imp.reload


def reload(x):
    """
    Replacement for builtin reload() by autoimp.py.

    Reloads the module argument, and returns the reloaded module.  The
    module need not have been already imported.  If the argument has the
    special method __reload__(), then that method is called and its
    return value is returned by reload().
    """
    if hasattr(x, '__reload__'):
        return x.__reload__()
    else:
        return _reload(x)


if _sys.version_info[:2] >= (2, 2):
    _help = help
    __all__.append('help')


    def help(x):
        """
        Get help on the given object.
        """
        if hasattr(x, '__help__'):
            return x.__help__()
        else:
            return _help(x)
