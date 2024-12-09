from setuptools import setup

setup(
    name='csv_extractor',
    version='0.1',
    install_requires=['pandas>=2.2.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Reads a CSV file with a header.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
