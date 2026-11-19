# -*- coding: utf-8 -*-
"""Open a sample in REA and run a list of tool calls in one session.

Usage:
  python rea_query.py <node.exe> <rea.mjs> <sample> <out.json> tool1 '{"json":1}' tool2 '{}' ...

Each response is written to out.json with the tool name, arguments and raw result.
"""
import hashlib
import json
import os
import queue
import subprocess
import sys
import threading
import time

node, script, sample, out_path = sys.argv[1:5]
pairs = sys.argv[5:]
assert len(pairs) % 2 == 0, "tool/args pairs expected"

env = dict(os.environ)
env["PATH"] = os.path.dirname(os.path.abspath(node)) + ";" + env.get("PATH", "")
env.setdefault("HUSKY", "0")

proc = subprocess.Popen(
    [node, script, "mcp"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    env=env, cwd=os.getcwd(),
)
lines = queue.Queue()
stderr_chunks = []


def pump_out():
    for raw in iter(proc.stdout.readline, b""):
        lines.put(raw.decode("utf-8", "replace").rstrip("\r\n"))


def pump_err():
    for raw in iter(proc.stderr.readline, b""):
        stderr_chunks.append(raw.decode("utf-8", "replace").rstrip("\r\n"))


threading.Thread(target=pump_out, daemon=True).start()
threading.Thread(target=pump_err, daemon=True).start()

_id = 0


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


def read_until(msg_id, timeout=900):
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


def call(name, args, timeout=900):
    mid = send("tools/call", {"name": name, "arguments": args})
    t0 = time.time()
    resp = read_until(mid, timeout)
    text = None
    if resp and "result" in resp:
        for item in resp["result"].get("content", []):
            if item.get("type") == "text":
                text = item.get("text")
    return {
        "tool": name,
        "arguments": args,
        "elapsed_seconds": round(time.time() - t0, 3),
        "response": resp,
        "text": text,
    }


init_id = send("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "fusion-rea-query", "version": "1.0"},
})
init = read_until(init_id, 180)
send("notifications/initialized", {}, notify=True)

results = []
if init is not None:
    results.append(call("open_binary", {"path": sample}))
    for i in range(0, len(pairs), 2):
        results.append(call(pairs[i], json.loads(pairs[i + 1])))

out = {
    "sample": sample,
    "sample_sha256": hashlib.sha256(open(sample, "rb").read()).hexdigest(),
    "initialize": init,
    "results": results,
    "stderr_tail": stderr_chunks[-30:],
}
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

try:
    proc.stdin.close()
except Exception:
    pass
try:
    proc.wait(timeout=10)
except Exception:
    proc.kill()

print(json.dumps({
    "calls": [{"tool": r["tool"], "ok": bool(r["response"] and "error" not in r["response"]),
              "seconds": r["elapsed_seconds"]} for r in results]
}, ensure_ascii=False))
