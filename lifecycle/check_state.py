# -*- coding: utf-8 -*-
"""check_state.py — v3.1 R7 防线：校验 STATE.yaml 与 git 仓库一致。

用法:
  python lifecycle/check_state.py [--fix-commit <sha>]

检查:
  1. STATE 存在且可解析
  2. last_commit 在 git log 中存在
  3. last_commit 等于当前 HEAD（或在远端 main 上）
对不上时:
  - 打印具体修法命令（不许猜）
  - --fix-commit <sha> 用真实 sha 更新 STATE 的 last_commit
"""
import os
import subprocess
import sys

# PyYAML 可能没装：用最小解析兜底
def _load_state(path):
    if not os.path.exists(path):
        return None
    try:
        import yaml
        return yaml.safe_load(open(path, encoding="utf-8"))
    except Exception:
        # 极简解析 last_commit/current_stage
        d = {}
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line.startswith("last_commit:") or line.startswith("current_stage:"):
                k, v = line.split(":", 1)
                d[k.strip()] = v.strip().strip('"').strip("'")
        return d or None


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True)


def main():
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    state_path = os.path.join(repo, "lifecycle", "STATE.yaml")
    state = _load_state(state_path)
    if state is None:
        print("FAIL  lifecycle/STATE.yaml 缺失或不可解析")
        print("修法: 创建 STATE.yaml（模板见 FUSION-FINAL-v3.1.md §8.2）")
        return 1

    lc = state.get("last_commit") or state.get("last_commit:", "").strip('"').strip("'")
    if not lc:
        print("FAIL  STATE 里没有 last_commit")
        return 1

    # last_commit 是否在 head.. 历史里
    r = git("rev-parse", "--verify", lc)
    if r.returncode != 0:
        print(f"FAIL  last_commit {lc} 不是有效 git 对象")
        print("修法: git log --oneline | head，找到真实 sha 后用:\n  python lifecycle/check_state.py --fix-commit <真实sha>")
        return 1

    head = git("rev-parse", "HEAD").stdout.strip()
    behind = git("rev-list", "--left-right", "--count", head + "..." + lc).stdout.strip()
    if head == lc:
        print("OK    STATE.last_commit == HEAD")
        return 0

    # 允许 last_commit 在远端 main 上（本地可落后一个提交）
    rmain = git("merge-base", "--is-ancestor", lc, "refs/remotes/origin/main")
    if rmain.returncode == 0:
        print(f"OK    last_commit 在远端 main 历史中（本地 HEAD 落后，next_step 会追上）")
        return 0

    print(f"FAIL  last_commit {lc} 与 HEAD {head} 不一致且在远端 main 找不到")
    print("修法: 用真实 sha 更新 STATE:\n  python lifecycle/check_state.py --fix-commit <真实sha>")
    return 1


if __name__ == "__main__":
    if "--fix-commit" in sys.argv:
        i = sys.argv.index("--fix-commit")
        sha = sys.argv[i + 1]
        subprocess.run(["git", "rev-parse", "--verify", sha], check=True)
        import re
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "STATE.yaml")
        s = open(p, encoding="utf-8").read()
        s = re.sub(r'last_commit: "\S+"', f'last_commit: "{sha}"', s)
        open(p, "w", encoding="utf-8").write(s)
        print(f"OK  STATE.last_commit 已更新为 {sha}")
    else:
        sys.exit(main())