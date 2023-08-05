#!/usr/bin/env python
# crate_anon/anonymise/hash.py

"""
Config class for CRATE anonymiser.

Author: Rudolf Cardinal
Created at: 22 Nov 2015
Last update: 22 Nov 2015

Copyright/licensing:

    Copyright (C) 2015-2016 Rudolf Cardinal (rudolf@pobox.com).
    Department of Psychiatry, University of Cambridge.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

import hashlib
import hmac
import sys
from typing import Any, Callable

import mmh3


# https://docs.python.org/3/library/platform.html#platform.architecture
IS_64_BIT = sys.maxsize > 2**32


# =============================================================================
# Base classes
# =============================================================================

class GenericHasher(object):
    def hash(self, raw: Any) -> str:
        """The public interface to a hasher."""
        raise NotImplementedError()


# =============================================================================
# Simple salted hashers.
# Note that these are vulnerable to attack: if an attacker knows a
# (message, digest) pair, it may be able to calculate another.
# See https://benlog.com/2008/06/19/dont-hash-secrets/ and
# http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.134.8430
# +++ You should use HMAC instead if the thing you are hashing is secret. +++
# =============================================================================

class GenericSaltedHasher(GenericHasher):
    def __init__(self, hashfunc: Callable[[bytes], Any], salt: str) -> None:
        self.hashfunc = hashfunc
        self.salt_bytes = salt.encode('utf-8')

    def hash(self, raw: Any) -> str:
        raw_bytes = str(raw).encode('utf-8')
        return self.hashfunc(self.salt_bytes + raw_bytes).hexdigest()


class MD5Hasher(GenericSaltedHasher):
    """MD5 is cryptographically FLAWED; avoid."""
    def __init__(self, salt: str) -> None:
        super().__init__(hashlib.md5, salt)


class SHA256Hasher(GenericSaltedHasher):
    def __init__(self, salt: str) -> None:
        super().__init__(hashlib.sha256, salt)


class SHA512Hasher(GenericSaltedHasher):
    def __init__(self, salt: str) -> None:
        super().__init__(hashlib.sha512, salt)


# =============================================================================
# HMAC hashers. Better, if what you are hashing is secret.
# =============================================================================

class GenericHmacHasher(GenericHasher):
    def __init__(self, digestmod: Any, key: str) -> None:
        self.key_bytes = str(key).encode('utf-8')
        self.digestmod = digestmod

    def hash(self, raw: Any) -> str:
        raw_bytes = str(raw).encode('utf-8')
        hmac_obj = hmac.new(key=self.key_bytes, msg=raw_bytes,
                            digestmod=self.digestmod)
        return hmac_obj.hexdigest()


class HmacMD5Hasher(GenericHmacHasher):
    def __init__(self, key: str) -> None:
        super().__init__(hashlib.md5, key)


class HmacSHA256Hasher(GenericHmacHasher):
    def __init__(self, key: str) -> None:
        super().__init__(hashlib.sha256, key)


class HmacSHA512Hasher(GenericHmacHasher):
    def __init__(self, key: str) -> None:
        super().__init__(hashlib.sha512, key)


# =============================================================================
# Hashing in a NON-CRYPTOGRAPHIC, PREDICTABLE, and fast way
# =============================================================================

def hash64(x: Any) -> int:
    return mmh3.hash64(x, seed=0, x64arch=IS_64_BIT)[0]
    # The first number is the low-order half of the 128-bit hash; see the
    # slower pure Python version at
    # https://github.com/wc-duck/pymmh3/blob/master/pymmh3.py
