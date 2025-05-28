# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

from setuptools import setup, find_packages

setup(
    name="url2llm",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "lunarcore",
        "crawl4ai",
    ],
    python_requires=">=3.8",
    author="Lunarbase",
    author_email="contact@lunarbase.ai",
    description="Component for extracting information from web pages using LLM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lunarbase/url2llm",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 