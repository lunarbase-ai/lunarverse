from setuptools import setup

setup(
    name='openai_vectorizer',
    version='0.1',
    install_requires=['langchain~=0.1.7'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Use OpenAI models to encode texts. The output is the embeddings',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
