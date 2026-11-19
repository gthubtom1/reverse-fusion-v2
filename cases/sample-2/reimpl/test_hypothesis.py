# -*- coding: utf-8 -*-
"""Run candidate serials (RC4-KSA hypothesis) against the original in QEMU."""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from serial_model import candidate_serial  # noqa: E402

sample = sys.argv[1]
name, email = "alice", "bob@example.com"
runner = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "stage3", "qemu_run.py")

results = []
for i in (0, 3, 6, 9, 12, 15):
    serial = candidate_serial(name, email, i)
    if not serial:
        results.append((i, "skip", None))
        continue
    infile = os.path.join(r"D:\tmp", "hyp-%d.in" % i)
    with open(infile, "wb") as f:
        f.write(name.encode() + b"\n" + email.encode() + b"\n" +
                serial.encode("latin-1") + b"\n")
    log = os.path.join(r"D:\tmp", "hyp-%d.log" % i)
    subprocess.run([sys.executable, "-I", runner, sample, infile, log],
                   stdout=subprocess.DEVNULL, timeout=180)
    body = open(log + ".body.txt", encoding="utf-8", errors="replace").read()
    rc = re.search(r"SAMPLE-RC=(-?\d+)", body)
    decision = "denied" if "ROBBER" in body else ("accepted" if rc and rc.group(1) == "0" else "unknown")
    results.append((i, decision, serial.encode("latin-1").hex()))

for r in results:
    print(r)
