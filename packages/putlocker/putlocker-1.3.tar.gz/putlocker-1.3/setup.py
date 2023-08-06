#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import (setup, find_packages)
from putlocker import (__version__, __author__, __author_email__)

setup(
    name="putlocker",
    packages=find_packages(),
    version=__version__,
    platforms=["Linux"],
    url="https://github.com/agusmakmun/putlocker/",
    download_url="https://github.com/agusmakmun/putlocker/tarball/v{}".format(__version__),
    description="Grabber app to get meta-data or download the movie from Putlocker. Website Putlocker: http://putlockers.ch",
    long_description=open("README.rst").read(),
    license="MIT",
    author=__author__,
    author_email=__author_email__,
    keywords=["putlocker", "putlocker downloader", "putlocker grabber"],
    entry_points={
        "console_scripts": ["putlocker=putlocker.putlocker:main", ],
    },
    install_requires=["cfscrape>=1.6.8"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet",
        "Topic :: Utilities"
    ]
)
