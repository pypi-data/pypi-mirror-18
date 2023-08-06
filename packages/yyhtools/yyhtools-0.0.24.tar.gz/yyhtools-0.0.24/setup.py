#!/usr/bin/env python

import os
from setuptools import setup, find_packages

CURDIR = os.path.abspath(os.path.dirname(__file__))

with open("%s/version.txt" % CURDIR) as fp:
    version = fp.read().strip().rstrip()

setup(
    name = 'yyhtools',
    version = version,
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    install_requires = [],
    packages = ['yyhtools'],
    include_package_data=True,
    author = 'yyh',
    author_email = '736184425@qq.com',


    platforms = 'any',
)
