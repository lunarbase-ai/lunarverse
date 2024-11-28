from setuptools import setup

setup(
    name='nci_thesaurus',
    version='0.1',
    install_requires=['owlready2>=0.46'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Retrieve biomedical information from the NCI Thesaurus, via SPARQL query',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
