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
This is the distribution setup for WIDE IO DFRACT
"""

import os
import sys

from setuptools import setup
try:
    from pip.req import parse_requirements
    install_reqs = parse_requirements( "requirements.txt", session = False)
    reqs = [str(ir.req) for ir in install_reqs]
except:
    sys.stderr.warning("Could not load requirements - install pip")
    reqs = []

module = "dfract"


version = None

try:
    from dfract import __version__
    version = __version__
except:
  try:
    with open(os.path.join(os.path.dirname(__file__), module, 'VERSION'), 'r') as fd:
        version = fd.read()
  except:
    pass

if not version:
    version = "0.0.1"

setup(
    name=module,
    version=version,
    description='DFRACT  -',
    author='WIDE IO LTD',
    author_email='support@wide.io',
    url='https://gitlab.pet.wide.io/wide-io/dfract.git',
    license='BSD',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
    packages=[module, 
              module + '.datasets', 
              module + '.datastreams' 
    ],
    install_requires=reqs,
    include_package_data=True,
    package_dir={module: module},
    package_data={
        '': ['LICENSE'],
        module: ['VERSION']
    },
    entry_points={
        'console_scripts': [
            'dfract = dfract.client:main'
        ],
    },
    extras_require={
        ':python_version == "2.7"': [
            'functools32',
        ],
    }
)

