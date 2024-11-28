from setuptools import setup

setup(
    name='react_agent',
    version='0.1',
    install_requires=['arxiv==2.1.0', 'mediawikiapi==1.2', 'wikibase-rest-api-client==0.1.3', 'wikipedia==1.4.0', 'wolframalpha==5.0.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Implements ReACT logic.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
