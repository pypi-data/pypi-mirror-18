#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='exchange_rates',
    version='1.0.01',
    description='Retrives currency exchange rates from http://api.fixer.io/',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    url='http://exchange_rates.lukeshiner.com',
    keywords=['exchange rates', 'currency', 'api'],
    install_requires=['requests'],
    packages=find_packages(),
    )
