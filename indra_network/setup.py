from setuptools import setup

setup(
    name='indra_network',
    version='0.1',
    install_requires=['indra', 'pybel', 'https://files.pythonhosted.org/packages/8f/d3/d994f9347b42407adc04e58fdeb5e52013df14bcc4a678c5211ffd526ebd/pandas-1.2.5-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.whl', 'boto3==1.33.2', 'botocore==1.33.2', 's3transfer==0.8.1', 'beautifulsoup4', 'requests', 'networkx', 'tqdm'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Retrieve literature related to a set of genes',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
