#!/usr/bin/env python

import sys, os
import setuptools


version = '0.1.0'


def long_description():
    """
    - pypi likes rst, Github prefers markdown
    - if README.rst exists use that
    - if README.md exists convert that to rst
    - pandoc README.md -o README.rst
    """
    return ''


def gather_requirements():
    """
    - define your requirements in requirements.txt
    - allow pinned requirements in requirements.txt but ignore the pin in setup.py
    - allow >= in requirements.txt and carry that through
    - ignore blank lines and comments in requirements.txt
    """
    requirements = []
    for r in open('requirements.txt').readlines():
        if not r.strip().startswith('#') and r.strip():
            if '==' in r:
                r = r.split('==')[0]
            requirements.append(r)
    return requirements


if sys.argv[-1] == 'publish':
    os.system('python setup.py register')
    os.system('python setup.py sdist upload')
    # os.system('python setup.py bdist_wheel upload --universal')
    sys.exit()


setuptools.setup(
    name='ssl_expiry',
    version=version,
    author='Brenton Cleeland',
    author_email='brenton@brntn.me',
    packages=setuptools.find_packages(),
    url='https://github.com/sesh/ssl_expiry',
    description='Quickly check when your SSL certificate expires from the command line',
    long_description=long_description(),
    entry_points={
        'console_scripts': [
            'ssl_expiry=ssl_expiry.ssl_expiry:ssl_expiry',
        ]
    },
    install_requires=gather_requirements(),
    license='MIT License',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ]
)
