#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='sophiabus230',
      version='0.1',
      description='Module to get the timetable of the Sophia Antipolis bus line 230',
      url='http://github.com/paraita/sophiabus230',
      author='Paraita Wohler',
      author_email='paraita.wohler@gmail.com',
      license='MIT',
      packages=['sophiabus230'],
      install_requires=[
          'beautifulsoup4',
          'python-dateutil'
      ],
      test_suite='nose.collector',
      tests_require=[
          'mock',
          'nose',
          'coverage',
          'coveralls'
      ],
      zip_safe=False)
