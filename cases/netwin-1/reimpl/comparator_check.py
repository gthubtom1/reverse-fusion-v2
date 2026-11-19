# -*- coding: utf-8 -*-
"""Comparator self-check for netwin-1 (TC5 防背答案)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from licensecheck import validate

def validate_tampered(s):
    """改 0x2F -> 0x2E：独一常量，其余同 licensecheck.validate"""
    if len(s) != 12 or s[3] != '-' or s[7] != '-':
        return False
    sm = 0
    for i in range(12):
        if i in (3, 7):
            continue
        sm += ord(s[i]) ^ (i * 7)
    return (sm % 256) == 0x2E


rows = []
for s in ["AAA-AAA-AAA|", "AAA-AAA-AAAZ", "abc"]:
    n = validate(s)
    t = validate_tampered(s)
    # 防背答案：凡 normal 通过(candidate)，tampered 必须改为 False；
    # normal 不通过的无效输入，tampered 保持 False 属正确语义。
    changed = (n is True and t is False) or (n is False and t is False)
    rows.append({"input": s, "normal": n, "tampered": t, "changed": changed,
                 "note": "valid candidate must flip to False" if n else "invalid stays False"})
ok = all(r["changed"] for r in rows)
print({"ok": ok, "rows": rows})