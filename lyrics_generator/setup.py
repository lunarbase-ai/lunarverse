from setuptools import setup

setup(
    name='lyrics_generator',
    version='0.1',
    install_requires=['langchain~=0.1.7'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description="Generates song lyrics from an inputted theme using Azure OpenAI's API (an LLM).",
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
