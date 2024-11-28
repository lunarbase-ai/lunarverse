from setuptools import setup

setup(
    name='llamaindex_query',
    version='0.1',
    install_requires=['llama_index~=0.10.58', 'llama-index-embeddings-azure-openai~=0.1.11', 'llama-index-llms-azure-openai~=0.1.10', 'llama-index-retrievers-bm25~=0.2.2'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Querying from LlamaIndex index.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
