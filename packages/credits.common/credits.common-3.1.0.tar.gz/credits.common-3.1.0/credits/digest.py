#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from operator import itemgetter

NONE = b"\x00"
BOOL = b"\x01"
INT = b"\x02"
UTF8 = b"\x03"
BYTES = b"\x04"
LIST = b"\x05"
MAP = b"\x06"


@functools.singledispatch
def digest(obj):
    raise TypeError("Unknown type: %s." % (type(obj, )))


@digest.register(bytes)  # noqa
def _(obj: bytes):
    return BYTES + len(obj).to_bytes(4, "big") + obj


@digest.register(str)  # noqa
def _(obj: str):
    return UTF8 + len(obj).to_bytes(4, "big") + obj.encode("utf8")


@digest.register(int)  # noqa
def _(obj: int):
    return INT + obj.to_bytes(4, "big")


@digest.register(dict)  # noqa
def _(obj: dict):
    pairs = (digest(k) + digest(v) for (k, v) in sorted(obj.items(), key=itemgetter(0)))
    return MAP + len(obj).to_bytes(4, "big") + b"".join(pairs)


@digest.register(tuple)  # noqa
@digest.register(list)  # noqa
def _(container: list):
    return LIST + len(container).to_bytes(4, "big") + b"".join(digest(value) for value in container)


@digest.register(type(None))  # noqa
def _(value: type(None)):
    return NONE
