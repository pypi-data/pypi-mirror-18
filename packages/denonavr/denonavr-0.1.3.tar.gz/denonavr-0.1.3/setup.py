#!/usr/bin/env python
# encoding: utf-8
"""Setup script."""
from setuptools import setup

setup(name='denonavr',
      version='0.1.3',
      description='Automation Library for Denon AVR receivers',
      long_description='Automation Library for Denon AVR receivers',
      url='https://github.com/scarface-4711/denonavr',
      author='Oliver Goetz',
      author_email='scarface@mywoh.de',
      license='MIT',
      packages=['denonavr'],
      install_requires=['requests'],
      platforms=['any'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries",
          "Topic :: Home Automation",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: PyPy"
          ])
