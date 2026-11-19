# -*- coding: utf-8 -*-
"""unique-router check (R7 防线 6): only core/skills/config/routing.json is
the route table. Run from repo root."""
import glob
import os
import sys


def main():
    routing = os.path.join("core", "skills", "config", "routing.json")
    if not os.path.exists(routing):
        print("FAIL  core/skills/config/routing.json 缺失")
        return 1
    others = glob.glob(os.path.join("core", "**", "routing.json"), recursive=True)
    others = [p for p in others if p != routing]
    if others:
        print(f"FAIL  发现额外 routing.json: {others}")
        return 1
    print("OK    唯一路由表 core/skills/config/routing.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())