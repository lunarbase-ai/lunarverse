from setuptools import setup

setup(
    name='audio2base64',
    version='0.1',
    install_requires=['mimetypes'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Converts an audio file (.mp3 or .wav) to a base64 string.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
