#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright (c) 2016 Sergey S. aka j7sx

from setuptools import setup, find_packages

setup(
    name     = 'gXor',
    version  = '0.1',
    packages = find_packages(),
    requires = ['python (>= 3.0)'],
    description  = 'XOR(gamma-sequence) symmetric enc/dec method',
    long_description = open('README.rst').read(), 
    author       = 'Sergey S. aka j7sx',
    author_email = 'joker66s@mail.ru',
    url          = 'https://github.com/j7sx/gXor',
    download_url = 'https://github.com/j7sx/gXor/tarball/master',
    license      = 'BSD',
    keywords     = ['xor', 'gamma', 'gamma-sequence'],
    classifiers  = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)