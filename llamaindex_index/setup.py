from setuptools import setup

setup(
    name='llamaindex_index',
    version='0.1',
    install_requires=['llama_index~=0.10.58', 'llama-index-embeddings-azure-openai~=0.1.11', 'llama-index-llms-azure-openai~=0.1.10'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Index documents from a json dict with Azure OpenAI models within LlamaIndex.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
