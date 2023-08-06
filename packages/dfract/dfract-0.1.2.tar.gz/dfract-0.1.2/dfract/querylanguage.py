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
import dateutil.parser

import logging
import re
from functools import reduce


def xhasattr(object, path):
    try:
        xgetattr(object, path)
    except AttributeError:
        return False
    return True


def xgetattr(object, path):
    r = reduce(
        lambda x, y: (
            x.__getitem__(y) if (
                hasattr(
                    x, "__getitem__")) else getattr(
                x, y)), path.split("."), object)
    if (callable(r)):
        r = r()
    return r


def parse_date(d):
    if isinstance(d, datetime.datetime):
        return d
    return dateutil.parser.parse(d)


operators = {
    '$and': lambda object, arg: reduce(lambda x, y: x and match_object(object, y), arg, True),
    '$or': lambda object, arg: reduce(lambda x, y: x or match_object(object, y), arg, False),
    '$nor': lambda object, arg: reduce(lambda x, y: not (x or match_object(object, y)), arg, False),
    '$lt': lambda object, arg: (object < arg),
    '$lte': lambda object, arg: (object <= arg),
    '$gt': lambda object, arg: (object > arg),
    '$gte': lambda object, arg: (object >= arg),
    '$ne': lambda object, arg: (object != arg),
    '$neq': lambda object, arg: (object != arg),
    '$in': lambda object, arg: (object in arg),
    '$all': lambda object, arg: (reduce(lambda b, k: b or (k in object), arg, False)),
    '$regex': lambda object, arg: re.match(arg, object),
    '$mod': lambda object, arg: (object % arg[1] == arg[2]),
    '$nin': lambda object, arg: not (object in arg),
    '$not': lambda object, arg: not match_object(object, arg),
    '$len': lambda object, arg: match_object(len(object), arg),
    '$exists': lambda object, arg: xhasattr(object, arg),
    '$lt_date': lambda object, arg: (parse_date(object) < parse_date(arg)),
    '$lte_date': lambda object, arg: (parse_date(object) <= parse_date(arg)),
    '$gt_date': lambda object, arg: (parse_date(object) > parse_date(arg)),
    '$gte_date': lambda object, arg: (parse_date(object) >= parse_date(arg)),
    '$geo_ball': lambda object, arg: (sum([(o[0] - o[1]) ** 2 for o in zip(object, arg[0])]) ** .5 <= arg[1]),

}


def match_object(object, rule):
    for i in rule.items():
        if (i[0][0] == '$'):
            v = operators[i[0]](object, i[1])
            if not v:
                return False
        else:
            try:
                v = xgetattr(object, i[0])
            except AttributeError:
                logging.warning(str(i[0]) + " not found")
                return False
            except KeyError:
                logging.warning(str(i[0]) + " not found")
                return False
            except Exception as e:
                # print object, i[0]
                raise e
            if (isinstance(v, dict)):
                if not match_object(v, i[1]):
                    return False
            else:
                if (isinstance(i[1], dict)):
                    if not match_object(v, i[1]):
                        return False
                else:
                    if (v != i[1]):
                        return False
    return True
