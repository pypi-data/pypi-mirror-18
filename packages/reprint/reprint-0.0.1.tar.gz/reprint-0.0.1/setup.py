# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md") as file:
    long_desc = file.read()


setup(
    name="reprint",
    version="0.0.1",
    packages=find_packages(),

    author="Yinzo",
    author_email="oop995+pypi@gmail.com",
    description="A simple module for Python3 to print and refresh multi line output contents in terminal",
    long_description=long_desc,
    license="Apache-2.0",
    keywords="multi line print value binding refresh",
    url="https://github.com/Yinzo/reprint",
)