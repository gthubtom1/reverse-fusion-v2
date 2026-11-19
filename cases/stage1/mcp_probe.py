# -*- coding: utf-8 -*-
"""Minimal MCP stdio probe: initialize + tools/list, save raw evidence.

Usage:
  python mcp_probe.py <node.exe> <server-script> <out.json> [args...]
"""
import json
import os
import queue
import subprocess
import sys
import threading
import time

node, script, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
extra = sys.argv[4:]

env = dict(os.environ)
node_dir = os.path.dirname(os.path.abspath(node))
env["PATH"] = node_dir + ";" + env.get("PATH", "")
env.setdefault("HUSKY", "0")

proc = subprocess.Popen(
    [node, script, *extra],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env,
    cwd=os.getcwd(),
)

lines = queue.Queue()
stderr_chunks = []


def pump(stream, q, tag):
    for raw in iter(stream.readline, b""):
        text = raw.decode("utf-8", "replace").rstrip("\r\n")
        if tag == "out":
            q.put(text)
        else:
            stderr_chunks.append(text)


threading.Thread(target=pump, args=(proc.stdout, lines, "out"), daemon=True).start()
threading.Thread(target=pump, args=(proc.stderr, queue.Queue(), "err"), daemon=True).start()


def send(obj):
    proc.stdin.write((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))
    proc.stdin.flush()


def read_until(msg_id, timeout=120):
    deadline = time.time() + timeout
    seen = []
    while time.time() < deadline:
        try:
            line = lines.get(timeout=1)
        except queue.Empty:
            if proc.poll() is not None:
                break
            continue
        seen.append(line)
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if msg.get("id") == msg_id:
            return msg, seen
    return None, seen


started = time.time()
send({
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "fusion-probe", "version": "1.0"},
    },
})
init_msg, init_raw = read_until(1, 180)

tools_msg, tools_raw = None, []
if init_msg is not None:
    send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    tools_msg, tools_raw = read_until(2, 180)

tools = []
if tools_msg and isinstance(tools_msg.get("result"), dict):
    tools = tools_msg["result"].get("tools", [])

result = {
    "command": [node, script, *extra],
    "cwd": os.getcwd(),
    "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "elapsed_seconds": round(time.time() - started, 3),
    "initialize_ok": init_msg is not None,
    "server_info": (init_msg or {}).get("result", {}).get("serverInfo"),
    "protocol_version": (init_msg or {}).get("result", {}).get("protocolVersion"),
    "tools_list_ok": tools_msg is not None,
    "tool_count": len(tools),
    "tool_names": sorted(t.get("name", "") for t in tools),
    "raw_initialize": init_raw,
    "raw_tools": tools_raw,
    "stderr_tail": stderr_chunks[-40:],
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

try:
    proc.stdin.close()
except Exception:
    pass
try:
    proc.wait(timeout=10)
except Exception:
    proc.kill()

print(json.dumps({
    "initialize_ok": result["initialize_ok"],
    "server_info": result["server_info"],
    "tools_list_ok": result["tools_list_ok"],
    "tool_count": result["tool_count"],
}, ensure_ascii=False))
