from setuptools import setup

setup(
    name='container',
    version='0.1',
    install_requires=['docker~=7.1.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Runs a service in a Docker container based on the provided image. If necessary it downloads the image beforehand.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
