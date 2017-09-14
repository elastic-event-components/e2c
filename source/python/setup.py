#!/usr/bin/env python

from setuptools import find_packages, setup

version = 0.1

install_requires = []
with open('scripts/require.txt') as f:
    install_requires = f.readlines()

setup(
    name='e2c',
    packages=find_packages(),
    license='Apache 2.0',
    platforms="any",
    version=version,
    author='Stefan Bergmann',
    author_email='stefan.bergmann.cx@gmail.com',
    description='Elastic Event Components',
    long_description=open("README.md").read(),
    install_requires=install_requires,
    entry_points={},
    classifiers=[],
)
