from setuptools import find_packages, setup

AUTHOR = "Lunarbase (https://lunarbase.ai/)"
AUTHOR_EMAIL = "contact@lunarbase.ai"
LICENSE = "SPDX-License-Identifier: GPL-3.0-or-later"
TEST_REQUIREMENTS = [
    'pytest'
]
EXTRAS_REQUIREMENTS = {
    'dev': [
        'pytest',
    ],
}

REQUIREMENTS_FILE_PATH = 'requirements.txt'

class ComponentSetupGenerator:
    def __init__(self, name, version, description):
        self.name = name
        self.version = version
        self.description = description

    def generate(self):
        return {
            "name": self.name,
            "version": self.version,
            "packages":find_packages(where="src"),
            "package_dir":{"": "src"},
            "install_requires": self._load_requirements(),
            "tests_require": TEST_REQUIREMENTS,
            "extras_require": EXTRAS_REQUIREMENTS,
            "author": AUTHOR,
            "author_email": AUTHOR_EMAIL,
            "description": self.description,
            "license": LICENSE,
        }

    def _load_requirements(self):
        with open(REQUIREMENTS_FILE_PATH, 'r') as file:
            lines = file.read().splitlines()
            return [line for line in lines if line and not line.startswith('#')]

setup_generator = ComponentSetupGenerator(
    name="bar_chart",
    version="0.1",
    description="Plots a bar chart given a dictionary with numerical values"
)

setup(**setup_generator.generate())
from setuptools import setup

setup(
    name='bar_chart',
    version='0.1',
    install_requires=['matplotlib~=3.8.0'],
    tests_require=['pytest'],
    extras_require={'dev': ['pytest']},
    author='Lunarbase (https://lunarbase.ai/)',
    author_email='contact@lunarbase.ai',
    description='Plots a bar chart given a dictionary with numerical values. The output can be linked to a report component.',
    license='SPDX-License-Identifier: GPL-3.0-or-later',
)
