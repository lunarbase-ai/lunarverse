from setuptools import setup

setup(
    name='cytoscape_visualizer',
    version='0.1',
    install_requires=[],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Receives a Cytoscape formatted JSON and creates a graph visualization.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
