from setuptools import setup

setup(
    name='progeny',
    version='0.1',
    install_requires=['decoupler', 'pandas', 'anndata'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='PROGENy is the definitive resource for pathways and target genes, with weights for each interaction. It requires two CSV files as input. decoupler https://decoupler-py.readthedocs.io/en/latest/notebooks/progeny.html | paper: Schubert, M., Klinger, B., Klünemann, M. et al. Perturbation-response genes reveal signaling footprints in cancer gene expression. Nat Commun 9, 20 (2018). https://doi.org/10.1038/s41467-017-02391-6 (https://www.nature.com/articles/s41467-017-02391-6)',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
