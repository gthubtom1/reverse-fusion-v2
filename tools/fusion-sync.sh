#!/usr/bin/env bash
# fusion-sync.sh — 读唯一配置文件，生成三根细指针（v3.2 §11）。
# 用法：bash tools/fusion-sync.sh
# 只做四件事：生成 .mcp.json / 根 CLAUDE.md / AGENTS.md 顶部指针 / 全局技能 router 指针。
set -euo pipefail

HOME_CONF="${HOME_CONF:-$HOME/.fusion/fusion-home.yaml}"
if [[ ! -f "$HOME_CONF" ]]; then
  echo "FAIL 配置文件不存在: $HOME_CONF" >&2
  exit 1
fi

# 读 yaml 四值（简化解析：shared_folder/node_exe/ghidra_install_dir/java_home）
pick() { grep -E "^$1:" "$HOME_CONF" | head -1 | sed "s/^$1:[[:space:]]*//" | sed 's/[[:space:]]*$//'; }
SHARED=$(pick shared_folder)
NODE=$(pick node_exe)
GHIDRA=$(pick ghidra_install_dir)
JDK=$(pick java_home)
if [[ -z "$SHARED" || -z "$NODE" ]]; then
  echo "FAIL 配置文件缺 shared_folder 或 node_exe" >&2
  exit 1
fi

# 统一斜杠为 Windows 兼容（保持原始值；反斜杠路径原样用于 JSON，正斜杠用于文本指针）
SHARED_WS=$(printf '%s' "$SHARED" | sed 's|\\|/|g')
NODE_JSON=$(printf '%s' "$NODE" | sed 's|\\|\\\\|g')
GHIDRA_JSON=$(printf '%s' "$GHIDRA" | sed 's|\\|\\\\|g')
JDK_JSON=$(printf '%s' "$JDK" | sed 's|\\|\\\\|g')

# 1) .mcp.json（用 Python 生成，保证 JSON 反斜杠转义正确）
if [[ ! -f "$SHARED/.mcp.json.template" ]]; then
  echo "FAIL 缺少 .mcp.json.template" >&2; exit 1
fi
SHARED_S="$SHARED" NODE_S="$NODE" GHIDRA_S="$GHIDRA" JDK_S="$JDK" \
python - "$SHARED/.mcp.json.template" "$SHARED/.mcp.json" <<'PY'
import json, os, sys
tpl, out = sys.argv[1], sys.argv[2]
t = open(tpl, encoding="utf-8").read()
env = {
    "SHARED_FOLDER": os.environ["SHARED_S"],
    "NODE_EXE": os.environ["NODE_S"],
    "GHIDRA_DIR": os.environ["GHIDRA_S"],
    "JAVA_HOME": os.environ["JDK_S"],
}
data = json.loads(t)
def fill(o):
    if isinstance(o, dict):
        return {k: fill(v) for k, v in o.items()}
    if isinstance(o, list):
        return [fill(v) for v in o]
    if isinstance(o, str):
        for k, v in env.items():
            o = o.replace("<" + k + ">", v)
        return o
    return o
data = fill(data)
# SHARED_FOLDER 在 JSON 里统一用正斜杠（Windows/jq 都认），其余保留原样
json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK  .mcp.json 生成（python）")
PY

# 2) 根 CLAUDE.md（仅在缺失时写入；若已是占位符/指针版则保留，避免覆盖仓库模板）
if [[ ! -f "$SHARED/CLAUDE.md" ]] || ! grep -q "<SHARED_FOLDER>" "$SHARED/CLAUDE.md" 2>/dev/null; then
  cat > "$SHARED/CLAUDE.md" <<EOF
# reverse-fusion-v2（指针文件）
本项目位置：\`$SHARED\`（共享文件夹，三个上游、全部技能、全部案子都在里面）。
第一步，先读：\`$SHARED/FUSION-FINAL-v3.2.md\` 的“从磁盘恢复清单”那一节，再读 \`$SHARED/lifecycle/STATE.yaml\`，看 \`current_stage\` 和 \`next_step\`，从那里继续做。
总控是 \`$SHARED/core/skills/SKILL.md\`（reverse-skill-router）。分析引擎是 REA，只通过 MCP 调，不加载它的技能文件当总控。Seep 不在这里装（Track B，单独走）。
路径不要写死：共享文件夹位置只记在配置文件里（\`%USERPROFILE%\\.fusion\\fusion-home.yaml\` 的 \`shared_folder\` 这一行）。搬家只改那一行，再跑一次同步脚本。
EOF
  echo "OK  根 CLAUDE.md 生成（真实路径填充）"
else
  echo "OK  根 CLAUDE.md 保留（占位符版/已存在）"
fi

# 3) AGENTS.md 顶部指针（保留原 5 条同步约定）
if [[ -f "$SHARED/AGENTS.md" ]]; then
  head -3 "$SHARED/AGENTS.md" | grep -q "本项目位置" || {
    tmp=$(mktemp)
    cat > "$tmp" <<EOF
# reverse-fusion-v2（指针文件）
本项目位置：\`$SHARED\`。第一步读 \`$SHARED/FUSION-FINAL-v3.2.md\` 与 \`$SHARED/lifecycle/STATE.yaml\`；总控 \`$SHARED/core/skills/SKILL.md\`；配置文件 \`%USERPROFILE%/.fusion/fusion-home.yaml\`。
下面 5 条同步约定全文保留：
EOF
    cat "$SHARED/AGENTS.md" >> "$tmp"
    mv "$tmp" "$SHARED/AGENTS.md"
  }
  echo "OK  AGENTS.md 顶部指针已加（5 条约定保留）"
else
  echo "WARN AGENTS.md 不存在，跳过（记开放项）"
fi

# 4) 全局技能 router 指针（三个宿主；目录不存在也要尽力建）
for base in "$HOME/.claude" "$HOME/.codex" "$HOME/.pi"; do
  mkdir -p "$base/skills/reverse-skill-router"
  cat > "$base/skills/reverse-skill-router/SKILL.md" <<EOF
---
name: reverse-skill-router
description: Routes reverse engineering tasks to the right skill. Use when a task is about analyzing, rebuilding, bypassing or extracting an algorithm from a program and the correct entrypoint is unclear.
---
# reverse-skill-router（指针文件，不是总控本身）
这个文件只有指路，不写任何方法。真正的方法全在共享文件夹里，不要在这里加内容。
共享文件夹位置：\`$SHARED\`
第一步，先读这一个文件：\`$SHARED/core/skills/SKILL.md\`（唯一总控）。
第二步，按总控说的做。路由用 \`$SHARED/core/skills/scripts/master-route.ps1\`（Windows）或 \`master-route.sh\`，路由表只认 \`$SHARED/core/skills/config/routing.json\`。工具路径只认 \`$SHARED/core/skills/tool-index.md\`。
重建（R46）入口在 \`$SHARED/core/skills/reconstruction/SKILL.md\`，由总控打开，不要直接跳过去。
共享文件夹搬家后，这个文件不用手改：改配置文件里的一行，再跑一次同步脚本，它会自动重写。
EOF
  echo "OK  $base/skills/reverse-skill-router/SKILL.md 生成"
done

echo "同步完成。"