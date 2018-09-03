#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='red-baron',
      version='1.0',
      description='red-baron',
      install_requires=['requests', 'termcolor'],
      author='Akifumi Imanishi',
      author_email='akifumi.imanishi@gmail.com',
      url='https://github.com/asi1024/red-baron',
      packages=find_packages(exclude=('example',)),
      scripts=['red-baron'])
