# -*- coding: utf-8 -*-
"""Independent repro of netwin-1 license check (mode 3 algorithm extraction).

Original: self-built .NET console app (cases/netwin-1/target/Program.cs),
compiled to build.exe. Algorithm: serial 12 chars, chars at 3 and 7 must be
'-'; sum over non-dash chars of (char ^ i*7); pass iff (sum % 256) == 0x2F.
Repro is written from static reading; does not execute the exe.
"""
import subprocess
import sys

EXE = r"D:\Project\最终版聚合\cases\netwin-1\target\build\out\build.exe"


def validate(s):
    if len(s) != 12 or s[3] != '-' or s[7] != '-':
        return False
    sm = 0
    for i in range(12):
        if i in (3, 7):
            continue
        sm += ord(s[i]) ^ (i * 7)
    return (sm % 256) == 0x2F


def original(s):
    r = subprocess.run([EXE, s], capture_output=True, text=True, timeout=15)
    return r.stdout.strip() == "VALID"


CASES = [
    ("TC1 good", "AAA-AAA-AAA|"),
    ("TC2 good", "BBB-BBB-BBB|"),
    ("TC3 bad len", "abc"),
    ("TC4 bad dash", "ABCD-EFG-HIJK"),
    ("TC5 bad sum", "AAA-AAA-AAAZ"),
]


def run():
    rows = []
    ok = True
    for name, s in CASES:
        o = original(s)
        n = validate(s)
        m = o == n
        if not m:
            ok = False
        rows.append({"case": name, "input": s, "original": o, "repro": n, "match": m})
    return ok, rows


if __name__ == "__main__":
    ok, rows = run()
    for r in rows:
        print(f"{r['case']:12} {r['input']!r:22} orig={r['original']!s:5} repro={r['repro']!s:5} {'OK' if r['match'] else 'FAIL'}")
    print("ALL_MATCH", ok)
    sys.exit(0 if ok else 1)