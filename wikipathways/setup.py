from setuptools import setup

setup(
    name='wikipathways',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Fetch data from WikiPathways: an open science platform for biological pathways contributed, updated, and used by the research community.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
