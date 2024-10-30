from setuptools import setup

setup(
    name='paper_database_builder',
    version='0.1',
    install_requires=['git+https://github.com/SL2000s/lm_theory.git'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Builds a JSON with data of scientific papers.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
