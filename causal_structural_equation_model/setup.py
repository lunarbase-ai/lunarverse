from setuptools import setup

setup(
    name='causal_structural_equation_model',
    version='0.1',
    install_requires=['graphviz>=0.17,<1.0.0', 'pygraphviz>=1.7,<2.0', 'langchain~=0.1.7', 'semopy>=2.3,<3.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Run SemoPy with an initial SEM so it can be refined and interpreted by an LLM.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
