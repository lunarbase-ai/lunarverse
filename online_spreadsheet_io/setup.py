from setuptools import setup

setup(
    name='online_spreadsheet_io',
    version='0.1',
    install_requires=['pyocclient==0.6', 'openpyxl>=3'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Save to a online spreadsheet then and forward the content',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
