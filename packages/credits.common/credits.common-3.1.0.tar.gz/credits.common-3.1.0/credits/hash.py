#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from credits.interface import HashProvider


class SHA256HashProvider(HashProvider):
    fqdn = "works.credits.core.SHA256HashProvider"

    def hash(self, i: bytes) -> bytes:
        """
        Return the SHA256 hash of the input i.

        :type i: bytes
        :rtype: bytes
        """
        return hashlib.sha256(i).digest()

    def marshall(self) -> dict:
        return {
            "fqdn": self.fqdn,
        }

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls()


class SHA512HashProvider(HashProvider):
    fqdn = "works.credits.core.SHA512HashProvider"

    def hash(self, i: bytes) -> bytes:
        """
        Return the SHA512 hash of the input i.

        :type i: bytes
        :rtype: str
        """
        return hashlib.sha512(i).digest()

    def marshall(self) -> dict:
        return {
            "fqdn": self.fqdn,
        }

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls()
