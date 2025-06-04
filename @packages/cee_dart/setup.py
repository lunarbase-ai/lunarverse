from setuptools import setup, find_packages

setup(
    name="cee_dart",
    version="0.1.0",
    install_requires=[
        "numpy",
        "pandas",
        "networkx",
        "openai",
        "requests",
        "pingouin",
        "seaborn",
        "matplotlib",
        "pydantic",
        "rich",
        "pydot",
        "pydotplus",
        "gprofiler-official",
        "pandera",
        "python-dotenv",
    ],
    author="CEE DART Team",
    description="A package for biological pathway analysis and evidence integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 