#!/usr/bin/env python

from setuptools import setup

setup(name='csplitb',
  version='1.0',
  description='Split binary files on content boundaries',
  author='Michael White',
  author_email='csplitb@mypalmike.com',
  url='https://github.com/mypalmike/csplitb',
  py_modules=['csplitb'],
  scripts=['scripts/csplitb'],
  include_package_data=True,
)
