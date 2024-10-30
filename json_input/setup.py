from setuptools import setup

setup(
    name='json_input',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Allows the input of a JSON text (potentially with template variables) that can then be used in other downstream components. It can also be used as an output if useful.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
