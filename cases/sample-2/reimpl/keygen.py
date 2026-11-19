# -*- coding: utf-8 -*-
"""Keygen for sample 2.

Table generation reproduces FUN_00401d80 by emulating the original machine
code with Unicorn (verified byte-identical to the runtime table dumped via
gdb, see evidence/E-004-table-dump.txt). The serial check is reimplemented in
Python below.

Usage: python keygen.py <elf> <name> <email>
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMU = os.path.join(HERE, "emulate_hash.py")
IDX = (0, 3, 6, 9, 12, 15)


def H(elf, data: bytes) -> bytes:
    out = subprocess.run(
        [sys.executable, "-I", EMU, elf, data.hex()],
        capture_output=True, text=True, check=True)
    return bytes.fromhex(out.stdout.strip().splitlines()[-1])


def table_for(elf, name: str, email: str) -> bytes:
    return H(elf, H(elf, name.encode()) + H(elf, email.encode()))


def signed(b: int) -> int:
    return b - 256 if b >= 128 else b


def check(serial: bytes, table: bytes) -> bool:
    if len(serial) != 16:
        return False
    n = len(serial) + 1
    for i in IDX:
        a, b, c, p = i % n, (i + 1) % n, (i + 2) % n, (i + 3) % n
        get = lambda k: serial[k] if k < 16 else 0  # noqa: E731
        if get(b) + get(a) == get(c) * 8:
            continue
        if get(p) == (signed(table[i]) * 4) & 0xFF and signed(table[i]) * 4 == signed(get(p)):
            return True
    return False


def make_serial(table: bytes) -> bytes:
    for i in IDX:
        v = (signed(table[i]) * 4) & 0xFF
        if v == 0 or v in (0x0A, 0x0D) or signed(table[i]) * 4 != signed(v):
            continue
        s = bytearray(b"ABCDEFGHIJKLMNOP")
        s[(i + 3) % 17] = v
        a, b, c = i % 17, (i + 1) % 17, (i + 2) % 17
        get = lambda k: s[k] if k < 16 else 0  # noqa: E731
        if get(b) + get(a) == get(c) * 8 and c < 16:
            s[c] = (s[c] + 1) & 0xFF or 1
        if check(bytes(s), table):
            return bytes(s)
    raise SystemExit("no reachable table index for this input")


if __name__ == "__main__":
    elf, name, email = sys.argv[1], sys.argv[2], sys.argv[3]
    table = table_for(elf, name, email)
    serial = make_serial(table)
    print(serial.hex())
