#!/usr/bin/env python

try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup


setup(name='newsFeedClassifierCS331',
      version='2.0.1',
      license='LUMS',
      description='news feed classifier using naive bayes algorithm',
      long_description=open('README.md').read(),
      author='CS331 Group: Dot Slash',
      author_email='artificialintelligence@pern.edu.pk',
      reference= 'https://github.com/muatik/naive-bayes-classifier',
      packages=['newsFeedClassifierCS331'],
      platforms='any')
