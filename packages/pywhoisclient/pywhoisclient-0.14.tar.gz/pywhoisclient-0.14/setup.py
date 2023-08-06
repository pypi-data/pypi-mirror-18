#!/usr/bin/python3

from setuptools import setup


setup(
    name = "pywhoisclient",
    version = "0.14",
    author = "Vitold Sedyshev",
    author_email = "vit1251@gmail.com",
    description = "An demonstration of how to make whois reqest",
    license = "MIT",
    keywords = "whois client",
    url = "https://github.com/vit1251/pywhoisclient",
    packages = ['pywhoisclient', 'tests'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
