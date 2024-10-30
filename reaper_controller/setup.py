from setuptools import setup

setup(
    name='reaper_controller',
    version='0.1',
    install_requires=['langchain~=0.1.7', 'python-reapy~=0.10.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Controlls Reaper (a digital audio workstation (DAW)) by natural language. Opens a Reaper project, edits it, and creates a new audio file.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
