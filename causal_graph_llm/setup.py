from setuptools import setup

setup(
    name='causal_graph_llm',
    version='0.1',
    install_requires=['graphviz>=0.17,<1.0.0', 'pygraphviz>=1.7,<2.0', 'langchain~=0.1.7', 'wikipedia~=1.4.0', 'langchain-community~=0.2.11', 'langchain_openai~=0.1.20'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Run Causal Graph Discovery thrugh a LLM with access to wikipedia (Agent)',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
