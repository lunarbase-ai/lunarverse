from setuptools import setup, find_packages

setup(
    name='azure_openai_llm',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=['langchain~=0.1.7'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description="Connects to Azure OpenAI's API (an LLM), runs an inputted natural language prompt (str), and output the result as text (str).",
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
