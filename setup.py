#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='RedBaron',
      version='1.0',
      description='red-baron',
      author='Akifumi Imanishi',
      author_email='akifumi.imanishi@gmail.com',
      url='https://github.com/asi1024/red-baron',
      packages=find_packages(exclude=('example')),
      scripts=['red-baron'])
