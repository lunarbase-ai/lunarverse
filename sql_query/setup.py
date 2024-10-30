from setuptools import setup

setup(
    name='sql_query',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Connects to a SQL database and returns the result of a query',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
