from setuptools import setup

setup(
    name='sleep',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Sleep (delay execution) for the given number of seconds.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
