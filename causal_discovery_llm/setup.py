from setuptools import setup

setup(
    name='causal_discovery_llm',
    version='0.1',
    install_requires=['econml>=0.14.1,<1.0.0', 'graphviz>=0.17,<1.0.0', 'pygraphviz>=1.7,<2.0', 'langchain~=0.1.7', 'langchain-community~=0.2.11', 'statsmodels~=0.14.0', 'scipy~=1.14.0', 'causal-learn~=0.1.3', 'torchvision~=0.19.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Run Causal Discovery algorithms with the help of a LLM to run different methods',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
