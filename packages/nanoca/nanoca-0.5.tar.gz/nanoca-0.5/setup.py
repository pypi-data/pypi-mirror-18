# -*- coding: utf8 -*-

from setuptools import setup, find_packages

setup(
    name        = 'nanoca',
    packages    = find_packages(),
    scripts     = ['nanoca'],
    version     = '0.5',
    description = 'small library and cli tool for managing a certificate authority',
    author      = 'Moritz Möller',
    author_email= 'mm@mxs.de',
    url         = 'https://github.com/mo22/nanoca'
)
