# -*- coding: utf-8 -*-
"""Candidate model for sample 2.

Hypothesis (from Ghidra main at 0x401640 + FUN_00401d80):
  table = KSA( KSA(name) || KSA(email) )   # RC4 key scheduling, 256-byte state
  serial is 16 bytes; for some i in {0,3,6,9,12,15}:
      serial[(i+3) % 17] == (table[i] * 4) & 0xff
  and (serial[(i+1)%17] + serial[i]) != serial[(i+2)%17] * 8

The check loop uses strlen+1 (17) as the modulus, so index 16 is the NUL terminator.
"""


def ksa(key: bytes) -> bytes:
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) & 0xFF
        s[i], s[j] = s[j], s[i]
    return bytes(s)


def table_for(name: str, email: str) -> bytes:
    key = ksa(name.encode()) + ksa(email.encode())
    return ksa(key)


def candidate_serial(name: str, email: str, i: int) -> str:
    table = table_for(name, email)
    s = bytearray(b"A" * 16)
    target = (table[i] * 4) & 0xFF
    if target == 0:
        return ""
    idx = (i + 3) % 17
    if idx >= 16:
        return ""
    s[idx] = target
    # make cond1 true for this i
    a, b, c = i % 17, (i + 1) % 17, (i + 2) % 17
    if a >= 16 or b >= 16 or c >= 16:
        return ""
    if (s[b] + s[a]) == s[c] * 8:
        s[c] = (s[c] + 1) & 0xFF or 1
    if 0 in s:
        s = bytearray(x or 1 for x in s)
    return s.decode("latin-1")
