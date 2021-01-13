#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="stispectrograph",
    version="0.2",
    author="Antoni Kowalik",
    author_email="antonikowalik23@gmail.com",
    description="A replacement for \"ST-i Spectroscopy Program\" by SBIG.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=["bin/fits_to_csv.py"],
    license="LICENSE.txt",
    install_requires=["astropy"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    keywords="astronomy, spectrograph, sti, sbig",
    python_requires=">=3.8",
)
