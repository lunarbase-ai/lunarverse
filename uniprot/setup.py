from setuptools import setup

setup(
    name='uniprot',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Fetch data from UniProt: a database of high-quality, comprehensive and freely accessible resource of protein sequence and functional information. ',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
