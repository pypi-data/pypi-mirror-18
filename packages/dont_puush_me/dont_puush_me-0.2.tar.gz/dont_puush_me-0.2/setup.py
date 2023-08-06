#!/usr/bin/env python3
import os.path

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dont_puush_me",
    version="0.2",
    description="A short script to upload screenshots to an SFTP server",
    long_description=long_description,
    url="https://pubgit.sotecware.net/jonas.wielicki/dont_puush_me",
    author="Jonas Wielicki",
    author_email="jonas@wielicki.name",
    license="GPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Communications :: Chat",
    ],
    packages=["dont_puush_me"],
    entry_points={
        "console_scripts": [
            "dont-puush-me=dont_puush_me:main"
        ]
    }
)
