from setuptools import setup

setup(
    name='pubmed_searcher',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Search article information from Pubmed by keywords',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
