from setuptools import setup

setup(
    name='report',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Creates an editable report from the input it gets.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
