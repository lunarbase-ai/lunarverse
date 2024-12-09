from setuptools import setup

setup(
    name='r_coder',
    version='0.1',
    install_requires=['rpy2~=3.5.15'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Performs customized R code execution. Outputs the value that the R variable `result` is set to during the execution of the R code.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
