#!/usr/bin/env python

from setuptools import setup
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = ''


setup(
    name='mfnbc',
    version='1.03',
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
