# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytools-command',

    version='0.9.0',

    description='A collection of functions to run and evaluate external commands from Python.',
    long_description=long_description,

    url='https://github.com/pytools/pytools-command',

    author='Richard King',
    author_email='richrdkng@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='command exec observe pytools development',

    packages=find_packages(exclude=('docs', 'tests')),

    install_requires=[],
)
