from setuptools import setup

setup(
    name='python_coder',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Performs customized Python code execution. Outputs the value that the Python variable `result` is set to during the execution of the Python code.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
