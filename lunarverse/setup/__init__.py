from setuptools import setup, find_packages

AUTHOR = "Lunarbase (https://lunarbase.ai/)"
AUTHOR_EMAIL = "contact@lunarbase.ai"
LICENSE = "SPDX-License-Identifier: GPL-3.0-or-later"
TEST_REQUIREMENTS = [
    'pytest'
]
EXTRAS_REQUIRE = {
    'dev': [
        'pytest',
    ],
}


class ComponentSetupGenerator:
    def __init__(self, name, version, description):
        self.name = name
        self.version = version
        self.description = description

    def generate(self):
        return setup(
            name=self.name,
            version=self.version,
            packages=find_packages(),
            install_requires=self.load_requirements('requirements.txt'),
            tests_require=TEST_REQUIREMENTS,
            extras_require=EXTRAS_REQUIRE,
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            description=self.description,
            license=LICENSE
        )
