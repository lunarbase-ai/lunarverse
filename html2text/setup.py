from setuptools import setup

setup(
    name='html2text',
    version='0.1',
    install_requires=['beautifulsoup4~=4.12.3'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Converts HTMLs to texts.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
