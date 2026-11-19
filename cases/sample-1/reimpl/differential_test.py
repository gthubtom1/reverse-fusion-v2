# -*- coding: utf-8 -*-
"""Run sample 1 original and the independent validator on the same inputs.

Usage:
  python differential_test.py <original.exe> <out.json>

Outputs: one record per case with input, original stdout/stderr/exit code,
original decision, new decision, and whether they match.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validator import check  # noqa: E402

original, out_path = sys.argv[1], sys.argv[2]

CASES = [
    ("TC1", "mr1337"),
    ("TC2", "mr1338"),
    ("TC3", "MR1337"),
    ("TC4", "mr133"),
    ("TC5", "mr13377"),
]


def run_original(candidate: str):
    try:
        proc = subprocess.run(
            [original],
            input=(candidate + "\n").encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
        )
        stdout = proc.stdout.decode("utf-8", "replace")
        stderr = proc.stderr.decode("utf-8", "replace")
        code = proc.returncode
    except Exception as exc:  # noqa: BLE001
        stdout, stderr, code = "", "%s: %s" % (type(exc).__name__, exc), None
    if "ACCESS GRANTED" in stdout:
        decision = "accepted"
    elif "ACCESS DENIED" in stdout:
        decision = "denied"
    else:
        decision = "unknown"
    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": code,
        "decision": decision,
    }


records = []
for case_id, candidate in CASES:
    orig = run_original(candidate)
    new_decision = "accepted" if check(candidate) else "denied"
    records.append({
        "case": case_id,
        "input": candidate,
        "original": orig,
        "new": {
            "decision": new_decision,
            "expected_password": "mr1337",
        },
        "match": orig["decision"] == new_decision,
    })

result = {
    "sample": original,
    "cases": records,
    "all_match": all(r["match"] for r in records),
    "original_runnable": all(r["original"]["decision"] != "unknown" for r in records),
}
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(json.dumps({
    "all_match": result["all_match"],
    "original_runnable": result["original_runnable"],
    "decisions": [(r["case"], r["original"]["decision"], r["new"]["decision"]) for r in records],
}, ensure_ascii=False))
