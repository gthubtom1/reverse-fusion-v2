# -*- coding: utf-8 -*-
"""Deliberately wrong variant: uses XOR key 0x54 instead of 0x55.

Used only to prove the comparator notices a difference (R46 L90).
"""

KEY = 0x54
EXPECTED_XORED = [0x38, 0x27, 0x64, 0x66, 0x66, 0x62]


def check(password: str) -> bool:
    if len(password) != 6:
        return False
    return all(ord(ch) == (b ^ KEY) for ch, b in zip(password, EXPECTED_XORED))
