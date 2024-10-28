from setuptools import setup, find_packages
import logging
import os

from setuptools import find_packages, setup

logging.basicConfig()

ROOT = os.path.abspath(os.path.dirname(__file__))
def load_requirements() -> list:
    """Load requirements from file, parse them as a Python list!"""
    with open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8") as f:
        all_reqs = f.read().split("\n")
    install_requires = [x.strip() for x in all_reqs if "git+" not in x]

    return install_requires

setup(
    name="text_input",
    version="0.1",
    packages=find_packages(),
    install_requires=load_requirements(),
    author="Your Name",
    author_email="your.email@example.com",
    description="A package that defines the TextInput component",
)