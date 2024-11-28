from setuptools import setup

setup(
    name='property_getter',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Extracts the mapped value of an inputted key/field/attribute in an inputted object/datastructure. It can be the value of a field/attribute in an object, or the mapped value of a key in a dictionary.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
