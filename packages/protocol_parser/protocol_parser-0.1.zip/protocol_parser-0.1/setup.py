#!/usr/bin/env python

#Copyright (c) [2016-] [Matan Perelman]
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

def get_tests():
    import pytest
    import unittest
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setup(name="protocol_parser",
    version="0.1",
    description="package for parsing data easily",
    long_description=readme(),
    url="https://github.com/matan1008/protocol_parser",
    download_url="https://github.com/matan1008/protocol_parser/tarball/0.1",
    author="Matan Perelman",
    author_email="matan1008@gmail.com",
    license="MIT",
    packages=["protocol_parser", "protocol_parser.parsing_elements", "protocol_parser.parsing_matches"],
    test_suite="setup.get_tests",
    tests_require=['pytest'],
    zip_safe=False)