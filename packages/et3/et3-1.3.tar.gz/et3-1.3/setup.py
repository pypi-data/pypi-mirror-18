#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup

#http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool
def parse_requirements():
    with open('requirements.txt') as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

VERSION = '1.3'
BASE_URL = 'https://bitbucket.org/lskibinski/et3'

setup(**{
    'name': 'et3',
    'version': VERSION,
    'description': 'Simple library for Extracting and Transforming data, third incarnation.',
    'url': BASE_URL,
    'download_url': BASE_URL + '/get/' + VERSION + '.tar.gz',
    'license': 'GPLv3',
    'author': 'Luke Skibinski',
    'author_email': 'lsh@ccxx.cx',
    'test_suite': 'et3.tests',
    'packages': ['et3'],
    'install_requires': parse_requirements(),
    'platforms': ['any']
})
