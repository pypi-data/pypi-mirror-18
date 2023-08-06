#!/usr/bin/env python

import os
from setuptools import setup, find_packages


PACKAGE = 'nejgit'

setup(
    name=PACKAGE,
    description="A collection of nejucomo's git helper tools.",
    version='0.1',
    author='Nathan Wilcox',
    author_email='nejucomo@gmail.com',
    license='GPLv3',
    url='https://github.com/nejucomo/nejgit',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'git-{} = {}.scripts.{}:main'.format(
                n.replace('_', '-'),
                PACKAGE,
                n
            )
            for n
            in [
                os.path.splitext(f)[0]
                for f
                in os.listdir('{}/scripts'.format(PACKAGE))
                if f != '__init__.py' and f.endswith('.py')
            ]
        ],
    }
    )
