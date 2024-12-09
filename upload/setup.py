from setuptools import setup

setup(
    name='upload',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Uploads local files to the server.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
