#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
import sys

def get_install_requires():
    install_requires = []
    with open('requirements.txt') as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            install_requires.append(line.strip())

    return install_requires


install_requires = get_install_requires()


setup(
    name='hubby',
    version='0.1.0',
    author='Tarjei Husøy',
    author_email='git@thusoy.com',
    url='https://github.com/thusoy/hubby',
    description="Hub alternatives",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'git-assignees = hubby:list_assignees'
        ]
    },
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        # 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
)
