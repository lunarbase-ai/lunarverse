from setuptools import setup

setup(
    name='pic2text',
    version='0.1',
    install_requires=['pix2text==1.1.0.2'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Extracts text and math formulas from a picture. The math formulas are outputted in LaTeX style (eg.: `$$f(x)=3 \\cdot x^2$$`).',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
