from setuptools import setup, find_packages

setup(
    name="text_input",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "lunarcore @ git+https://github.com/lunarbase-ai/lunar.git@feature/cancel-button#subdirectory=lunarcore"
    ],
    tests_require=[
        'pytest',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A package that defines the TextInput component",
)