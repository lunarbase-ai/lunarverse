from setuptools import setup

setup(
    name='sql_schema_extractor',
    version='0.1',
    install_requires=['psycopg2~=2.9.9'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Connects to a SQL database and retrieves its schema, i.e., data definition language.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
