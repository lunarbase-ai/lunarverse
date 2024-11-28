from setuptools import setup

setup(
    name='pdf_extractor',
    version='0.1',
    install_requires=['git+https://github.com/dscarvalho/pdf_extract.git@v0.1.3'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Extracts title, sections, references, tables and text from PDF files.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
