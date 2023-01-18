#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pywr-wq',
    version='0.1',
    description='model for expploring integrating water quality into Pywr',
    packages=find_packages(),
   
    entry_points='''
    [console_scripts]
    pywr-wq=pywr_wq.cli:start_cli
    ''',
)
