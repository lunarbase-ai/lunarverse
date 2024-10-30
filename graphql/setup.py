from setuptools import setup

setup(
    name='graphql',
    version='0.1',
    install_requires=['requests~=2.31.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Fetches data from a GraphQL endpoint',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
