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
# -*- coding: utf-8 -*-


"""
autoimp -- Import all modules, load them lazily at first use.

Public domain, Connelly Barnes 2006.  Works with Python 2.1 - 2.5.

I got sick of writing "import X" in Python.  To solve this problem,
one can now write

  >>> from autoimp import *
  >>> os.stat('.')                     # Module loaded at first use.
  >>> Image.open('test.bmp')           # Module loaded at first use.
  >>> pylab.plot([1,2],[3,4])          # Module loaded at first use.
  >>> scipy.linalg.eig([[1,2],[3,4]])  # Module loaded at first use.
  >>> os.stat('..')                    # Module has already been
  >>> ...                              # imported -- subsequent uses
  >>>                                  # of os are fast.

The command "from autoimp import *" imports all modules found in
sys.path lazily.  This is done by placing lazy-import proxy objects
in the namespace of module autoimp.  The modules are actually loaded
when they are first used.  For ultimate laziness, place the command
"from autoimp import *" in your PYTHONSTARTUP file.  Now your
interactive session has all modules available by default.

One can also use "from autoimp import *" in Python source files.  This
works correctly with documentation utilities such as pydoc and epydoc
(one should define __all__ to keep auto-imported modules from leaking
into the documentation).  One cannot currently use autoimp with py2exe
or pyinstaller, because the installers cannot determine which modules
are imported.

Auto-importing works on all of the packages which I tested (CGKit,
Numpy, Scipy, OpenGL, PIL, Pygame, ODE).  The wrapping class itself
works by sharing its __dict__ special attribute with the module; thus
there is little impact on the speed of the user's code (I benchmarked
the time to call (lambda: math.cos(1.0)); the function ran 1.022
million times per sec without autoimp, and 1.048 million times per sec
with autoimp on my Pentium 3 3.0 GHz Windows machine).

Note that the default behavior of "autoimp" is somewhat invasive: it
wraps all modules AND all sub-modules in the wrapper class
_LazyModule.  The benefit of this approach is that sub-modules are
lazily imported as well:

 >>> from autoimp import *
 >>> scipy.linalg
 >>> # Success

Finally, note that modules with leading underscores are not imported
(with the exception of __builtin__, __main__, and __future__), nor are
modules which have the same name as a builtin, such as "repr".  Also
reload() and help() are defined and exported by this module, so that
the these commands "do the right thing" when used with proxy import
objects.  The modified reload calls the __reload__() special method
on its argument (if available) and likewise for the help() function.

Send bugs, patches, suggestions to: connellybarnes at domain yahoo.com.

"""

__version__ = '1.0.2'
__all__ = ['reload']         # Lazily imported modules will go here

#TODO: .PY .pY .Py, various capitalizations of Python modules/packages.
#TODO: Test a whole lot on examples of lots of libraries.  Also test with
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

#from distutils.sysconfig import get_config_var as _get_config_var

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


class _RecursiveLazyModule(object):
    """
    Proxy class, imports modules and sub-modules automatically.
    """

    def __init__(self, modname, searchpath=None, lib=None):
        self.__dict__['__name__'] = modname
        self.__set_lib(lib)
        if (searchpath is not None):
            self.__dict__['__searchpath__'] = searchpath[:]
        else:
            self.__dict__['__searchpath__'] = None

    def __set_lib(self, lib):
        # Set the self.__lib attribute to lib.
        if lib is not None:
            # Share __dict__ with the imported object.
            self.__dict__ = lib.__dict__
            self.__dict__['_autoimp_lib'] = lib
        else:
            self.__dict__['_autoimp_lib'] = None

    def __load_lib(self):
        # Load library if not yet loaded.
        if self.__dict__.get('__searchpath__'):
            sav = _sys.path
            _sys.path = self.__dict__['__searchpath__']
            self.__set_lib(__import__(self.__name__))
            self.__dict__['__searchpath__'] = _sys.path
            _sys.path = sav
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
        if self.__dict__['_autoimp_lib'] is None:
            self.__load_lib()

        lib = self.__dict__['_autoimp_lib']

        # Look up key, is it now found?
        if hasattr(lib, key) and (not isinstance(getattr(lib, key), type(_os))):
            return getattr(lib, key)
        else:
            # Try importing a sub-module, wrapping it in a lazy import proxy.
            try:
                if '__searchpath__' not in self.__dict__:
                    self.__searchpath__ = None
                if self.__searchpath__:
                    sav = _sys.path
                    _sys.path = self.__dict__['__searchpath__']
                subname = '%s.%s' % (self.__name__, key)
                # print( "============================vvvv========================")
                #print
                #print(subname)
                #print
                consider = _sys.path
                fromlist = self.__name__.split(".")
                # print (fromlist)
                #print("============================^^^^========================")
                __import__(subname, fromlist=fromlist)
                if self.__searchpath__:
                    _sys.path = sav
                sublib = getattr(lib, key)
            except ImportError as e:
                print ("Exception " + repr(e))
                #print "lazy module content =",dir(self)
                raise AttributeError("'lazymodule' object '%s' has no attribute %r " % (self.__name__, key))
            self.__dict__[key] = _RecursiveLazyModule(subname, searchpath=self.__searchpath__, lib=sublib)
            #print key,self.__dict__[key]
            return self.__dict__[key]

    def __setattr__(self, key, value):
        # Import the module if user tries to set an attribute.
        if key == '__dict__':
            return super(_RecursiveLazyModule, self).__setattr__(key, value)
        if self.__dict__.get('_autoimp_lib') is None:
            self.__load_lib()
        self.__dict__[key] = value

    def __call__(self, *args, **kwargs):
        if self.__dict__['_autoimp_lib'] is None:
            self.__load_lib()
        lib = self.__dict__['_autoimp_lib']
        #print self.__dict__['__name__']
        return getattr(lib, "__call__")(*args, **kwargs)
        #raise TypeError("'lazymodule' object is not callable")


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
    return d.keys()


def _import_all():
    """
    Lazy import all modules found by _all_modules().
    """
    for mod in _all_modules():
        # Do not replace existing builtins, such as repr().
        if (not hasattr(_builtin, mod) and (not mod.startswith('_') or
                                            mod in _BUILTIN_SPECIAL_MODULES)):
            d = globals()
            d[mod] = _RecursiveLazyModule(mod)
            __all__.append(mod)


def import_all_as_context(context, temppath=None):
    """
    Lazy import all modules found by _all_modules().
    """
    if temppath:
        temppath = temppath[:]
        temppath.reverse()
        pathsav = _sys.path[:]
        #_sys.path=[]
        for t in temppath:
            if (t):
                if (t[-1] == "."):
                    t = t[:-1]
                m = __import__(t, fromlist=t.split('.')[-1])
                mp = m.__path__
                del m
                for p in mp:
                    _sys.path.insert(0, p)
                    #print p
    contextall = context["__all__"]
    #print  _all_modules()

    for mod in _all_modules():
        # Do not replace existing builtins, such as repr().
        if (not hasattr(_builtin, mod) and (not mod.startswith('_') or
                                            mod in _BUILTIN_SPECIAL_MODULES)):
            d = context
            d[mod] = _RecursiveLazyModule(mod, _sys.path)
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

_import_all()

