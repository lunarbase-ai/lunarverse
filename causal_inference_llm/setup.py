from setuptools import setup

setup(
    name='causal_inference_llm',
    version='0.1',
    install_requires=['dowhy~=0.11.1', 'causalpy~=0.3.1', 'econml~=0.14.1', 'graphviz~=0.17', 'pygraphviz~=1.7', 'langchain~=0.1.7', 'langchain-community~=0.2.11', 'langchain-openai~=0.1.20'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Run Causal Inference with the help of a LLM to run different methods (DoWhy and CausalPy)',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
