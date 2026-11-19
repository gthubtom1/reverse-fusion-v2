# -*- coding: utf-8 -*-
"""Compare emulated hash tables with tables dumped from the running original.

Usage: python verify_table.py <elf> <table.bin> <name> <email>
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMU = os.path.join(HERE, "emulate_hash.py")


def H(elf, data):
    out = subprocess.run([sys.executable, "-I", EMU, elf, data.hex()],
                         capture_output=True, text=True, check=True)
    return bytes.fromhex(out.stdout.strip().splitlines()[-1])


elf, table_path, name, email = sys.argv[1:5]
emulated = H(elf, H(elf, name.encode()) + H(elf, email.encode()))
dumped = open(table_path, "rb").read()
print("emulated", emulated[:16].hex())
print("dumped  ", dumped[:16].hex())
print("match", emulated == dumped)
sys.exit(0 if emulated == dumped else 1)
