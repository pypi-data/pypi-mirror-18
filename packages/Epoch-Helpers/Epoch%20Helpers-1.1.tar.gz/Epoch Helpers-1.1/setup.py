#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='Epoch Helpers',
      version='1.1',
      description='Helpers for comparing dates with January 1st, 1970',
      author='Christopher Harris',
      author_email='cbrentharris@gmail.com',
      url='https://github.com/cbrentharris/epoch-helpers.git',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'epoch_helpers = epoch_helpers:main'
          ]
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      )
