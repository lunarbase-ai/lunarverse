from setuptools import setup

setup(
    name='table2text',
    version='0.1',
    install_requires=['pandas~=1.5.3', 'spacy~=3.5.4'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Takes a CSV formatted table as input and converts it to a text by sentencifying each row.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
