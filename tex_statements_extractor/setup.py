from setuptools import setup

setup(
    name='tex_statements_extractor',
    version='0.1',
    install_requires=['git+https://github.com/SL2000s/lm_theory.git'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Extracts definitions, axioms, lemmas, theorems, and corollaries stated in Latex codes.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
