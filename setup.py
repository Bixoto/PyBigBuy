#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'Lugh <jbc@mozaart.com>'
__version__ = '3.7.0'

packages = [
    'bigbuy',
]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='pybigbuy',
    version=__version__,
    install_requires=['requests>=2.1.0', 'requests_oauthlib>=0.4.0', 'ujson>=1.35'],
    author='Lugh',
    author_email='jbc@mozaart.com',
    license=open('LICENSE').read(),
    url='TODO',
    keywords='bigbuy search api dropshipping stream',
    description='Actively maintained, pure Python wrapper for the \
    BigBuy API.',
    long_description=open('README.rst').read() + '\n\n' +
        open('HISTORY.rst').read(),
    include_package_data=True,
    packages=packages,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
