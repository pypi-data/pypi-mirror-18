#!/usr/bin/env python

from setuptools import setup
with open('README.md') as README:
    long_description = README.read()

setup(
    name='mfnbc',
    version='1.01',
    license='The MIT License (MIT)',
    author="Shawn",
    author_email='shawnzam@gmail.com',
    url='https://github.com/shawnzam/mfnbc',
    packages=['mfnbc'],
    install_requires=['nltk>=3.2'],
    keywords=['bayes'],
    zip_safe=False,
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ]
)
