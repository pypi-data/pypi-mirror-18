# -*- coding: utf-8 -*-

from setuptools import setup
import sys
import os
import re

if sys.version_info < (2, 7):
    install_requires = ['lxml', 'argparse', 'cssselect']
else:
    install_requires = ['lxml', 'cssselect']

ROOT = os.path.dirname(__file__)
README = open(os.path.join(ROOT, 'README.rst')).read()
INIT_PY = open(os.path.join(ROOT, 'mtglib', '__init__.py')).read()

setup(
    name = 'mtglib',
    version = 0.1,
    author = 'Cameron Higby-Naquin',
    author_email = 'cameron.higbynaquin@gmail.com',
    maintainer = 'James Fette',
    maintainer_email = 'jfette@gmail.com',
    description = 'Magic the Gathering Python library',
    license = 'MIT',
    url = 'https://github.com/chigby/mtg',
    keywords = ['mtg', 'magic', 'gatherer'],
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Utilities',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
                   'Topic :: Games/Entertainment'],
    long_description = '''\
  Console-based access to the Gatherer Magic Card Database
  --------------------------------------------------------
  Search for Magic cards from the command line.  Limit your results by
  card name, color, type, rules text, converted mana cost, power,
  toughness, or expansion set.  Rulings and flavor text also available.
  Clean interface and output.
  '''
)
