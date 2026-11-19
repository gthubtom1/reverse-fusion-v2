# -*- coding: utf-8 -*-
"""submodule hard gate (R7 防线 5): verify pinned submodule HEADs.

Run from repo root (e.g. `python lifecycle/defenses/submodule_gate.py`).
Uses relative paths so git receives ASCII-safe paths when the repo lives
under a non-ASCII directory.
"""
import os
import subprocess
import sys

PIN = {
    "engine/rea": "4491c84c82140a43fa12390b727840a433875ba8",
    "upstream/reverse-skill": "ce675096e6a2cd4789a76f9bd618feddc2b6f333",
}


def main():
    ok = True
    for path, pinned in PIN.items():
        r = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", cwd=os.getcwd())
        if r.returncode != 0:
            print(f"FAIL  {path}: 子模块未初始化（{r.stderr.strip()}）")
            ok = False
            continue
        h = r.stdout.strip()
        if h != pinned:
            print(f"FAIL  {path}: HEAD={h} 应为 {pinned}")
            ok = False
        else:
            print(f"OK    {path} @ {h[:12]}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())