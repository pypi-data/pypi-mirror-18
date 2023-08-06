#!/usr/bin/python
import setuptools
from distutils.core import setup

setup(
  name = "snorkel_ie",
  packages = ["snorkel_ie"],
  description = "a lightweight framework for developing structured information extraction applications",
  license = 'Apache',
  version = "v0.4alpha", 
  author = "Alex Ratner",
  author_email = "ajratner@stanford.edu",
  url = "https://github.com/HazyResearch/snorkel",
  download_url = "https://github.com/HazyResearch/snorkel/tarball/v0.4.alpha", 
  keywords = "information extraction",
  classifiers = ['Development Status :: 3 - Alpha', 
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 2.7'],
  install_requires = ['jupyter', 'nltk', 'lxml', 'requests', 'numpy>=1.11', 'scipy>=0.17', 'bs4', 'matplotlib', 'theano>=0.8.2', 'sqlalchemy>=1.0.14', 'ipywidgets', 'pandas', 'sklearn'],
  )


