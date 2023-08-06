# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytools-args',

    version='0.1.0',

    description='A small helper module for detecting, evaluating and processing arguments.',
    long_description=long_description,

    url='https://github.com/pytools/pytools-args',

    author='Richard King',
    author_email='richrdkng@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

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

    keywords='arguments argument args pytools development',

    packages=find_packages(exclude=('docs', 'tests')),

    install_requires=[],
)
