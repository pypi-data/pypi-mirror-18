#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from setuptools import setup, find_packages

from pygetwallpapers import PKG

NAME = PKG['NAME']
VERSION = PKG['VERSION']
AUTHOR = PKG['AUTHOR']
AUTHOR_EMAIL = PKG['AUTHOR_EMAIL']
LICENSE = PKG['LICENSE']
URL = PKG['GITHUB_URL']
DESCRIPTION = "Package for download wallpapers from websites. Read help: %s" % PKG[
    'GITHUB_URL']

try:
    README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['grab==0.6.30'],
    keywords=[PKG['BIN_NAME'], PKG['NAME'], 'python get image', 'python load image',
              'python get wallpapers', 'load wallpapers', 'wallpaper', 'get wallpapers', 'wallpapers download'],
    entry_points={
        "console_scripts":
            ["%s = %s:run" % (PKG['BIN_NAME'], PKG['NAME'])]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking'
    ]
)
