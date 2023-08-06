#!/usr/bin/env python

import codecs
import os
import re

from setuptools import find_packages, setup


########################################

ROOT_PKG = 'ct_core_db'
NAME = 'ct-core-db'
DESCRIPTION = 'Catalant Core DB Framework'
KEYWORDS = 'flask sqlalchemy db database validation'
URL = 'https://github.com/Catalant/ct-core-db'
AUTHOR = 'Catalant Technologies'
AUTHOR_EMAIL = 'engineering@gocatalant.com'
LICENSE = 'MIT'
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2 :: Only',
    'Programming Language :: SQL',
    'Framework :: Flask',
    'Topic :: Software Development :: Libraries :: Python Modules']

########################################


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
META_PATH = os.path.join(ROOT_PKG, '__init__.py')


def _read(*path_parts):
    with codecs.open(os.path.join(ROOT_PATH, *path_parts), 'rb', encoding='utf-8') as f:
        return f.read()


META_FILE = _read(META_PATH)


def _extract_meta(meta):
    meta_match = re.search(r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


VERSION = _extract_meta('version')


install_requires = [
    l for l in _read('requirements.txt').split('\n')
    if l and not l.startswith('#')]

tests_requires = [
    l for l in _read('requirements-test.txt').split('\n')
    if l and not l.startswith('#')]


setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=_read('README.rst'),
    keywords=KEYWORDS.split(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_requires,
    zip_safe=False)
