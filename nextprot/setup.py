from setuptools import setup

setup(
    name='nextprot',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Fetch data from neXtProt: an on-line knowledge platform on human proteins, such as their function, subcellular location, expression, interactions and role in diseases. ',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
