from setuptools import setup, find_packages

setup(
    name = "fundamentals vs market price",
    version = "1.0",
    description = "work in progress",
    packages = find_packages(),
    install_requires = ['pandas', 'openpyxl', 'investpy']
)