#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from typing import Type
from typing import TypeVar

import ed25519
import logbook

from credits.interface import Marshallable

SigningKeyImpl = TypeVar("SigningKeyImpl", bound="SigningKey")
VerifyingKeyImpl = TypeVar("VerifyingKeyImpl", bound="VerifyingKey")


class SigningKey(Marshallable):
    fqdn = "NOTSET"

    def __init__(self):
        self.logger = logbook.Logger(__name__)

    @classmethod
    def new(cls: Type[SigningKeyImpl]) -> SigningKeyImpl:
        raise NotImplementedError()

    @classmethod
    def from_string(cls: Type[SigningKeyImpl], sk_s: str) -> SigningKeyImpl:
        raise NotImplementedError()

    def to_string(self) -> str:
        raise NotImplementedError()

    def get_verifying_key(self) -> VerifyingKeyImpl:
        raise NotImplementedError()

    def sign(self, data: bytes) -> bytes:
        raise NotImplementedError()

    def __str__(self):
        return self.to_string()


class VerifyingKey(Marshallable):
    fqdn = "NOTSET"

    def __init__(self):
        self.logger = logbook.Logger(__name__)

    @classmethod
    def from_string(cls: Type[VerifyingKeyImpl], sk_s: str) -> VerifyingKeyImpl:
        raise NotImplementedError()

    def to_string(self) -> str:
        raise NotImplementedError()

    def verify(self, data: bytes, signature: bytes) -> bool:
        raise NotImplementedError()

    def __str__(self):
        return self.to_string()


class ED25519VerifyingKey(VerifyingKey):
    fqdn = "works.credits.core.ED25519VerifyingKey"

    def __init__(self, vk):
        super(ED25519VerifyingKey, self).__init__()
        self.vk = vk

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls.from_string(payload["vks"])

    def marshall(self):
        return {
            "fqdn": self.fqdn,
            "vks": self.to_string(),
        }

    @classmethod
    def from_string(cls, vks: str) -> "ED25519VerifyingKey":
        """
        Take the output from ED25519VerifyingKey.to_string and convert it back into a VerifyingKey.
        """
        vk = ed25519.VerifyingKey(bytes.fromhex(vks))
        return cls(vk)

    def to_string(self) -> str:
        """
        Generate a string representation of this verifying key, useful for generating addresses using an AddressProvider
        """
        # It gives back the hex. As bytes? Decode it here to get a str of the hex.
        return self.vk.to_ascii(encoding="hex").decode()

    def verify(self, msg: bytes, signature: bytes) -> bool:
        """
        Verify data with a provided signature.
        """
        try:
            # This library does arguments round the other way.
            self.vk.verify(signature, msg)
            return True

        except ed25519.BadSignatureError:
            return False


class ED25519SigningKey(SigningKey):
    fqdn = "works.credits.core.ED25519SigningKey"

    def __init__(self, sk):
        super(ED25519SigningKey, self).__init__()
        self.sk = sk

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls.from_string(payload["sks"])

    def marshall(self):
        return {
            "fqdn": self.fqdn,
            "sks": self.to_string(),
        }

    @classmethod
    def new(cls) -> "ED25519SigningKey":
        """
        Generate a new ED25519SigningKey.
        """
        sk, _ = ed25519.create_keypair()
        return cls(sk)

    @classmethod
    def from_string(cls, sks):
        """
        Take the output from ED25519SigningKey.to_string and convert it back into a SigningKey.
        """
        sk = ed25519.SigningKey(codecs.decode(sks, "hex"))
        return cls(sk)

    def to_string(self):
        return self.sk.to_ascii(encoding="hex").decode()

    def get_verifying_key(self):
        """
        Generate the complementary ED25519VerifyingKey from this ED25519SigningKey.
        """
        return ED25519VerifyingKey(self.sk.get_verifying_key())

    def sign(self, data: bytes) -> bytes:
        return self.sk.sign(data)
