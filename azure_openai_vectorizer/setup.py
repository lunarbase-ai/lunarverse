from setuptools import setup

setup(
    name='azure_openai_vectorizer',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Encodes inputted texts as numerical vectors (embeddings) using Azure OpenAI models.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
