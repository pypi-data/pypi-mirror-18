# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="django_booley",
    version="0.1.1",
    author="Alberto Casero",
    author_email="kas.appeal@gmail.com",
    packages=["django_booley"],
    url="https://github.com/kasappeal/django_booley",
    license="MIT",
    description="Booley integration for Django with BooleyField for models.",
    install_requires=["booley", "Django"],
)
