#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import os, sys

from setuptools import setup, find_packages

if __name__ == "__main__":

    _setup = {}
    with open('src/_twisted_platform_support/_setup.py') as f:
        exec(f.read(), _setup)


    setup(
        name='twisted_platform_support',
        author='Twisted Matrix Laboratories',
        maintainer='Amber Brown',
        maintainer_email='hawkowl@twistedmatrix.com',
        url="https://github.com/twisted/twisted_platform_support",
        classifiers = [
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
        ],
        use_incremental=True,
        setup_requires=['incremental'],
        install_requires=[
        ],
        package_dir={"": "src"},
        packages=find_packages('src'),
        license="MIT",
        zip_safe=False,
        include_package_data=True,
        description='Platform support packages for Twisted.',
        long_description=open('README.rst').read(),
        **_setup["getSetupArgs"]()
    )
