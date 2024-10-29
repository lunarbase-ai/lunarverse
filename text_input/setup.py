from setuptools import setup, find_packages

def load_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        return [line for line in lines if line and not line.startswith('#')]

setup(
    name="text_input",
    version="0.1",
    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    tests_require=[
        'pytest',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    author="Lunarbase (https://lunarbase.ai/)",
    author_email="contact@lunarbase.ai",
    description="A package that defines the TextInput component",
    license="SPDX-License-Identifier: GPL-3.0-or-later"
)