#!/usr/bin/env python

from setuptools import setup, find_packages


PACKAGE = 'virtualenv_here'

setup(
    name=PACKAGE,
    description="Manage a virtualenv for a project based on the its path.",
    version='0.1',
    author='Nathan Wilcox',
    author_email='nejucomo@gmail.com',
    license='MIT',
    url='https://github.com/nejucomo/{}'.format(PACKAGE),

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            '{} = {}.main:main'.format(
                PACKAGE.replace('_', '-'),
                PACKAGE,
            )
        ],
    }
)
