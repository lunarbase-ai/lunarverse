from setuptools import setup

setup(
    name='spleeter_deezer',
    version='0.1',
    install_requires=['ffmpeg', 'libsndfile', 'spleeter', 'numpy<2.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Deezer Spleeter',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
