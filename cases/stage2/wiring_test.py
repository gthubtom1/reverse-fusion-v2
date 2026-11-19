# -*- coding: utf-8 -*-
"""Stage 2 wiring test: router-side task -> REA MCP -> evidence stored in cases/.

Sequence (matches FUSION-FINAL-v2.1 §7 stage 2 item 3):
  1. open_binary on the sample
  2. binary_overview
  3. get_evidence_bundle (summary) to obtain Evidence IDs
  4. get_evidence_bundle (complete) stored as the case evidence package

Usage:
  python wiring_test.py <node.exe> <rea.mjs> <sample> <case_dir>
"""
import json
import os
import queue
import subprocess
import sys
import threading
import time

node, script, sample, case_dir = sys.argv[1:5]
evidence_dir = os.path.join(case_dir, "evidence")
os.makedirs(evidence_dir, exist_ok=True)

env = dict(os.environ)
env["PATH"] = os.path.dirname(os.path.abspath(node)) + ";" + env.get("PATH", "")
env.setdefault("HUSKY", "0")

proc = subprocess.Popen(
    [node, script, "mcp"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    env=env, cwd=os.getcwd(),
)
lines = queue.Queue()


def pump_out():
    for raw in iter(proc.stdout.readline, b""):
        lines.put(raw.decode("utf-8", "replace").rstrip("\r\n"))


stderr_chunks = []


def pump_err():
    for raw in iter(proc.stderr.readline, b""):
        stderr_chunks.append(raw.decode("utf-8", "replace").rstrip("\r\n"))


threading.Thread(target=pump_out, daemon=True).start()
threading.Thread(target=pump_err, daemon=True).start()

_id = 0
transcript = []


def send(method, params=None, notify=False):
    global _id
    msg = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        msg["params"] = params
    if not notify:
        _id += 1
        msg["id"] = _id
    proc.stdin.write((json.dumps(msg, ensure_ascii=False) + "\n").encode("utf-8"))
    proc.stdin.flush()
    return _id


def read_until(msg_id, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            line = lines.get(timeout=1)
        except queue.Empty:
            if proc.poll() is not None:
                return None
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if msg.get("id") == msg_id:
            return msg
    return None


def call_tool(name, args):
    mid = send("tools/call", {"name": name, "arguments": args})
    t0 = time.time()
    resp = read_until(mid, 900)
    entry = {
        "tool": name,
        "arguments": args,
        "elapsed_seconds": round(time.time() - t0, 3),
        "ok": resp is not None and "error" not in (resp or {}),
        "response": resp,
    }
    transcript.append(entry)
    return entry


init_id = send("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "fusion-wiring-test", "version": "1.0"},
})
init = read_until(init_id, 180)
send("notifications/initialized", {}, notify=True)

results = {}
if init is not None:
    results["open_binary"] = call_tool("open_binary", {"path": sample})
    results["binary_overview"] = call_tool("binary_overview", {})
    results["evidence_summary"] = call_tool(
        "get_evidence_bundle", {"detail": "summary"})
    results["evidence_complete"] = call_tool(
        "get_evidence_bundle", {"detail": "complete"})

out = {
    "sample": sample,
    "sample_sha256": __import__("hashlib").sha256(
        open(sample, "rb").read()).hexdigest(),
    "case_dir": os.path.abspath(case_dir),
    "initialize": init,
    "results": results,
    "stderr_tail": stderr_chunks[-30:],
    "transcript": transcript,
}
with open(os.path.join(evidence_dir, "wiring-transcript.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# store the complete Evidence bundle separately when REA returned one
bundle_text = None
complete = results.get("evidence_complete") or {}
res = (complete.get("response") or {}).get("result", {})
for item in res.get("content", []):
    if item.get("type") == "text":
        bundle_text = item.get("text")
if bundle_text:
    with open(os.path.join(evidence_dir, "E-REA-COMPLETE.json"), "w", encoding="utf-8") as f:
        f.write(bundle_text)

try:
    proc.stdin.close()
except Exception:
    pass
try:
    proc.wait(timeout=10)
except Exception:
    proc.kill()

summary = {
    "init_ok": init is not None,
    "tools": {k: bool(v.get("ok")) for k, v in results.items()},
    "bundle_saved": bool(bundle_text),
}
print(json.dumps(summary, ensure_ascii=False))
