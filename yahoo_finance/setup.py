from setuptools import setup

setup(
    name='yahoo_finance',
    version='0.1',
    install_requires=['yfinance~=0.2.37'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description="Connects to Yahoo's public API (using Python package yfinance) and retrieves financial data about companies and their stocks.",
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
