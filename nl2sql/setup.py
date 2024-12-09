from setuptools import setup

setup(
    name='nl2sql',
    version='0.1',
    install_requires=['sqlparse~=0.5.1'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Produces an SQL query based on a natural language query statement ',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
