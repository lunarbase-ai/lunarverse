from setuptools import setup

setup(
    name='gemini_llm',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description="Connects to Gemini's API, runs natural language prompts and outputs the result as text",
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
