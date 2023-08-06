#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

version = "3.1.0"

packages = [
    "base58==0.2.2",
    "logbook==0.12.5",
    "ed25519",  # specifically unversioned
]

test_packages = [
    "pytest", "mypy-lang", "pytest-mypy"
]

setuptools.setup(
    name="credits.common",
    version=version,
    author="Credits Developers",
    author_email="admin@credits.vision",
    description="Credits blockchain framework common client library",
    install_requires=packages,
    namespace_packages=['credits'],
    packages=setuptools.find_packages(),
    url="https://github.com/CryptoCredits/credits-common",
    download_url="https://github.com/CryptoCredits/credits-common/tarball/%s" % version,
    extras_require={
        'test': test_packages,
    },
)
