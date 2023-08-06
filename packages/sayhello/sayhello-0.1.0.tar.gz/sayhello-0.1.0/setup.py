#!/usr/bin/env python
#encoding=utf-8

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    readme = f.read()

setup(
    name = 'sayhello',
    version = '0.1.0',
    author = 'catplanet',
    description = 'say text on the command-line',
    long_description = readme,
    author_email='catplanet@qq.com',
    url='https://github.com/catplant/say-hello',
    packages=find_packages(exclude=['test*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    #install_requires = ['doctop', 'requests'],
    license = 'MIT',
    keywords='say command text',
    entry_points={
        'console_scripts': ['say=say:run']
    }
)
