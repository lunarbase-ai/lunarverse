from setuptools import setup

setup(
    name='bar_chart',
    version='0.1',
    install_requires=['matplotlib~=3.8.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Plots a bar chart given a dictionary with numerical values. The output can be linked to a report component.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
