# -*- coding: utf-8 -*-

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pushscreeps/pushscreeps.py').read(),
    re.M
    ).group(1)

with open("README.rst", "rb") as f:
    long_description = f.read().decode("utf-8")


setup(
    name="pushscreeps",
    packages=["pushscreeps"],
    entry_points={
        "console_scripts": ['pushscreeps = pushscreeps.pushscreeps:main']
    },
    version=version,
    description="Python3 script for pushing code to screeps",
    long_description=long_description,
    author="Mathias Bøhn Grytemark",
    author_email="mathias@grytemark.no",
    url="https://github.com/mboehn/pushscreeps",
    install_requires=[
        "requests",
    ],
    )
