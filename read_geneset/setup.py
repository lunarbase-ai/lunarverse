from setuptools import setup

setup(
    name='read_geneset',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Reads a CSV file with genes and outputs a list of the gene names.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
