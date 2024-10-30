from setuptools import find_packages, setup
import os
import re

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
    def __init__(self):
        pass

    def generate_arguments(self, name, version, description, package_dir):
        return {
            "name": name,
            "version": version,
            # "packages":find_packages(where="src"),
            # "package_dir":{"": "src"},
            "install_requires": self._load_requirements(os.path.join(package_dir, REQUIREMENTS_FILE_PATH)),
            "tests_require": TEST_REQUIREMENTS,
            "extras_require": EXTRAS_REQUIREMENTS,
            "author": AUTHOR,
            "author_email": AUTHOR_EMAIL,
            "description": description,
            "license": LICENSE,
        }

    def generate_setup_file(self, name, version, description, package_dir):
        arguments = self.generate_arguments(name, version, description, package_dir)
        with open(os.path.join(package_dir, 'setup.py'), 'w') as file:
            file.write(f"from setuptools import setup\n")
            file.write("\n")
            file.write(f"setup(\n")
            for key, value in arguments.items():
                file.write(f"    {key}={repr(value)},\n")
            file.write(f")\n")

    def _load_requirements(self, requirements_path=REQUIREMENTS_FILE_PATH):
        if os.path.isfile(requirements_path):
            with open(requirements_path, 'r') as file:
                lines = file.read().splitlines()
                return [line for line in lines if line and not line.startswith('#')]
        else:
            return []
        

def get_all_dirs(path='.'):
    dirs = [
        d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.') and d != 'LICENSES' and d != 'utils'
    ]
    return dirs

dirs = get_all_dirs()
components = []

for component_dir in dirs:
    init_file_path = os.path.join(component_dir, '__init__.py')
    if os.path.isfile(init_file_path):
        with open(init_file_path, 'r') as file:
            content = file.read()
            match = re.search(r'component_description\s*=\s*["\']{3}(.*?)["\']{3}|component_description\s*=\s*["\'](.*?)["\']', content, re.DOTALL)
            if match:
                description = match.group(1) if match.group(1) else match.group(2)
                first_line = description.strip().split('\n')[0]
                component_info = {
                    'name': component_dir,
                    'description': first_line,
                    'version': '0.1'
                }
                components.append(component_info)

generator = ComponentSetupGenerator()
for component in components:
    generator.generate_setup_file(
        component['name'], 
        component['version'], 
        component['description'], 
        os.path.join(component['name'])
    )
    print(f"Generated setup.py for {component['name']}")