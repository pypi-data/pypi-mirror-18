#!/usr/bin/python
# -*- coding: utf-8

from os.path import dirname, basename, isfile
import glob

modules = glob.glob(dirname(__file__) + "/[!__]*.py")

__all__ = [basename(f)[:-3] for f in modules if isfile(f)]

DOMAIN_LIST = []

for name in __all__:
    _m = __import__(name, globals(), locals(), [], -1)
    DOMAIN_LIST.append(_m.__DOMAIN__)

del name
del _m


__name__ = "spiders"

__doc__ = """Package contains grab.Spiders modules for pygetwallpapers"""
