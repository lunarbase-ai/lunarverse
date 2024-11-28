from setuptools import setup

setup(
    name='causal_graph_viewer',
    version='0.1',
    install_requires=['pandas>=2.2.0', 'matplotlib>=3.1.1'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Displays JSON serializable graph (node-link format)',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
