from setuptools import setup

setup(
    name='wikidata',
    version='0.1',
    install_requires=['mediawikiapi==1.2', 'wikibase-rest-api-client==0.1.3'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Retrieves data from Wikidata API (a knowledge graph / knowledge base).',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
