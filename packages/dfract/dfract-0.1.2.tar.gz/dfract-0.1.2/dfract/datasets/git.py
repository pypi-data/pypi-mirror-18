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
import os
import subprocess
import sys

import yaml
from dfract import config
from dfract.cache_utils import lru_cache
from dfract.dataset import Dataset
from dfract.utils import sha256


def do_git_clone(self, url, repo_path, branch=None):
    dirname = os.path.dirname(repo_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    p = subprocess.Popen("git clone %s %s" % (url, repo_path))
    p.communicate()
    if branch is not None:
        p = subprocess.Popen("git checkout %s" % (branch,), cwd=repo_path)
        p.communicate()
    assert (p.returncode == 0)


def do_git_pull(self, repo_path, branch=None):
    p = subprocess.Popen("git pull", cwd=repo_path)
    p.communicate()
    if branch is not None:
        p = subprocess.Popen("git checkout %s" % (branch,), cwd=repo_path)
        p.communicate()
    assert (p.returncode == 0)


def do_git_log(self, repo_path, branch):
    p = subprocess.Popen("git pull", cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    content, errs = p.communicate()
    assert (p.returncode == 0)
    content = content.split("\n")


class GitWrappedDataset(Dataset):
    """
    Wrapper providing automated mechanism to link dfract dataset versions with the code repository versions.
    """

    def __init__(self, dataset):
        self._dataset = dataset

    def __getattr__(self, item):
        return getattr(self._dataset, item)


def autowrapped(wrapper, ctor):
    def new_ctor(*args, **kwargs):
        i = ctor(*args, **kwargs)
        return wrapper(i)

    return new_ctor


@lru_cache
def GitDataset(self, url, update=False, module=None, classname=None, branch=None, with_requirements=True,
               autowrap=True):
    ### download if not downloaded
    urlhash = sha256(url + ("#" + branch if branch is not None else '')).hexdigest()

    self.dataset_path = os.path.join(config.get("dataset_path"), urlhash + "-code")

    if not os.path.exists(self.dataset_path):
        do_git_clone(url, self.dataset_path, branch)
    else:
        if update:
            do_git_pull(self.dataset_path, branch)

    sys.path = sys.path + [self.dataset_path]

    git_config = {
        "module": url.split("/")[-1].split(".")[0],
        "classname": None
    }

    if os.path.exists(os.path.join(self.dataset_path, ".dfract.yml")):
        git_config = yaml.loads(config.read())

    if autowrap:
        xwrap = functools.partial(autowrapped, GitWrappedDataset)
    else:
        xwrap = lambda x: x

    m = __import__(module)
    if classname is None:
        return xwrap(getattr(m, classname))
    else:
        return xwrap(m.__call__)


__call__ = GitDataset
