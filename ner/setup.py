from setuptools import setup

setup(
    name='ner',
    version='0.1',
    install_requires=['spacy~=3.5.4'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Performs Named Entity Recognition (NER).',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
