from setuptools import setup

setup(
    name='elasticsearchdb',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Stores data in a given Elasticsearch instance for future search.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
