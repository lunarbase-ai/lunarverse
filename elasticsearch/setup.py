from setuptools import setup

setup(
    name='elasticsearch',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Search data in a given Elasticsearch instance.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
