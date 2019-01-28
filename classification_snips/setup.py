"""
Hello World app for running Python apps on Bluemix
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import os

here = path.abspath(path.dirname(__file__))

print('Hello ')

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='IWIBot-snips-flask',
    version='1.0.0',
    description='IWIBot Snips on Bluemix',
    long_description=long_description,
    url='https://github.com/HSKA-IWI-VSYS/IWIbot',
    license='Apache-2.0'
)


