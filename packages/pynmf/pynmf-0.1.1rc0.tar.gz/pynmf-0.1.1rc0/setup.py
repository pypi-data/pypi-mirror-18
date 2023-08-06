#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

long_description = "Non-negative matrix factorization algorithms for spike/mask inference on 2-photon recordings."


setup(
    name='pynmf',
    version='0.1.1rc0',
    description="non-negative matrix factorization algorithms for 2-photon processing",
    long_description=long_description,
    author='Daniel Sourdry, Fabian Sinz, Edgar Y. Walker',
    author_email='',
    license="MIT",
    url='https://github.com/cajal/pynmf',
    keywords='neuroscientific data processing',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['numpy','matplotlib','tifffile'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
