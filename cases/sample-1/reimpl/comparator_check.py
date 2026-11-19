# -*- coding: utf-8 -*-
"""Comparator self-check: run the same 5 cases through the original and a
deliberately broken variant. The comparator must report at least one mismatch.

Usage: python comparator_check.py <original.exe> <out.json>
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tampered_validator  # noqa: E402

original, out_path = sys.argv[1], sys.argv[2]
CASES = ["mr1337", "mr1338", "MR1337", "mr133", "mr13377"]


def original_decision(candidate):
    proc = subprocess.run(
        [original], input=(candidate + "\n").encode(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
    out = proc.stdout.decode("utf-8", "replace")
    if "ACCESS GRANTED" in out:
        return "accepted"
    if "ACCESS DENIED" in out:
        return "denied"
    return "unknown"


records = []
for candidate in CASES:
    orig = original_decision(candidate)
    bad = "accepted" if tampered_validator.check(candidate) else "denied"
    records.append({"input": candidate, "original": orig, "tampered": bad,
                    "match": orig == bad})

detected = any(not r["match"] for r in records)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"records": records, "detected_difference": detected}, f,
              ensure_ascii=False, indent=2)
print(json.dumps({"detected_difference": detected,
                  "mismatches": [r["input"] for r in records if not r["match"]]},
                 ensure_ascii=False))
