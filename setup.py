# -*- coding:utf-8 -*-

import os
from setuptools import setup

from WebHello import __VERSION__
BASE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE, 'README.md')).read()

setup(
    name='WebHello',
    version=__VERSION__,
    classifiers=['License :: OSI Approved :: BSD License'],
    long_description=README,
    author="mapix",
    author_email="mapix.me@gmail.com",
    url='http://mapix.me/webhello/',
    license='BSD',
    packages=['WebHello'],
    include_package_data=True,
    zip_safe=True,
)
