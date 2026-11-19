# -*- coding: utf-8 -*-
"""Run sample 2 in QEMU for each case and record the original result.

Usage: python run_cases.py <sample> <cases.json> <out.json>

cases.json: [{"case": "TC1", "name": "...", "email": "...", "serial": "..."}, ...]
Classification:
  - exit code 0 and no "ROBBER" marker -> "accepted"
  - "ROBBER" marker or exit code != 0 -> "denied"
  - otherwise -> "unknown"
"""
import json
import os
import re
import subprocess
import sys
import tempfile

RUNNER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "stage3", "qemu_run.py")

sample, cases_path, out_path = sys.argv[1:4]
cases = json.load(open(cases_path, encoding="utf-8"))

records = []
for c in cases:
    payload = "%s\n%s\n%s\n" % (c["name"], c["email"], c["serial"])
    fd, infile = tempfile.mkstemp(prefix="s2in-", dir=r"D:\tmp", text=True)
    with os.fdopen(fd, "w", newline="\n") as f:
        f.write(payload)
    log = os.path.join(r"D:\tmp", "s2-%s.log" % c["case"])
    proc = subprocess.run(
        [sys.executable, "-I", RUNNER, sample, infile, log],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    body = ""
    body_path = log + ".body.txt"
    if os.path.exists(body_path):
        body = open(body_path, encoding="utf-8", errors="replace").read()
    rc_match = re.search(r"SAMPLE-RC=(-?\d+)", body)
    rc = int(rc_match.group(1)) if rc_match else None
    if "ROBBER" in body:
        decision = "denied"
    elif rc == 0:
        decision = "accepted"
    else:
        decision = "unknown"
    records.append({
        "case": c["case"],
        "name": c["name"],
        "email": c["email"],
        "serial": c["serial"],
        "exit_code": rc,
        "decision": decision,
        "stdout_body": body,
        "log": log,
    })

with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"sample": sample, "cases": records}, f, ensure_ascii=False, indent=2)

print(json.dumps([(r["case"], r["decision"], r["exit_code"]) for r in records],
                 ensure_ascii=False))
