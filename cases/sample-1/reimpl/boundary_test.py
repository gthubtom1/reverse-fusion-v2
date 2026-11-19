# -*- coding: utf-8 -*-
"""Boundary/error probes for sample 1 (L5 surface), original vs reimplementation."""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validator import check  # noqa: E402

original, out_path = sys.argv[1], sys.argv[2]

CASES = [
    ("B1", ""),                      # empty input / EOF
    ("B2", "m"),                     # length 1
    ("B3", "mr1337 "),               # trailing space (cin >> strips whitespace)
    ("B4", "mr1337x"),               # length 7 with valid prefix
    ("B5", "x" * 64),                # long input
    ("B6", "mr1337\r"),              # CR before newline
]


def run(candidate):
    try:
        proc = subprocess.run(
            [original], input=(candidate + "\n").encode(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
        out = proc.stdout.decode("utf-8", "replace")
        code = proc.returncode
    except Exception as exc:  # noqa: BLE001
        out, code = "%s: %s" % (type(exc).__name__, exc), None
    if "ACCESS GRANTED" in out:
        decision = "accepted"
    elif "ACCESS DENIED" in out:
        decision = "denied"
    else:
        decision = "unknown"
    return out, decision, code


records = []
for case_id, candidate in CASES:
    out, decision, code = run(candidate)
    new = "accepted" if check(candidate) else "denied"
    records.append({
        "case": case_id,
        "input_repr": repr(candidate),
        "original_decision": decision,
        "original_exit_code": code,
        "original_stdout_tail": out[-200:],
        "new_decision": new,
        "match": decision == new,
    })

res = {"cases": records, "all_match": all(r["match"] for r in records)}
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print(json.dumps({"all_match": res["all_match"],
                  "rows": [(r["case"], r["original_decision"], r["new_decision"]) for r in records]},
                 ensure_ascii=False))
