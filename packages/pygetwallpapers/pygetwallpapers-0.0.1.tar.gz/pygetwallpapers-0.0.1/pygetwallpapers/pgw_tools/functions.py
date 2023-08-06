#!/usr/bin/python
# -*- coding: utf-8

import sys
import os
import pprint
import re


def ru(self, s="", e='utf-8'):
    try:
        s = s.encode(e)
    except:
        return s
    return s


def exit(self, code=0):
    sys.exit(code)


def chunks(array=[], chunk_size=5):
    for i in xrange(0, len(array), chunk_size):
        yield array[i:i + chunk_size]


def print_(s="",  mode=True):
    if mode == True:
        pprint.pprint(s)
    else:
        try:
            print(s)
        except:
            print s


def mkdirp(*args):
    directory = os.path.join(*args)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    return directory
