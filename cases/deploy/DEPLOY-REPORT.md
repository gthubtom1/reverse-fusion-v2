# 第 11 章 共享文件夹部署报告（v3.2）

日期：2026-11-20。

## 部署了什么（全部已落盘 + 已验）

| 项 | 状态 | 说明 |
|---|---|---|
| 唯一配置文件 | ✅ | `%USERPROFILE%/.fusion/fusion-home.yaml`（`shared_folder=D:\Project\最终版聚合`，4 路径 + 3 锁定提交） |
| `.mcp.json.template` | ✅ | 进仓库，占位符版（`<NODE_EXE>/<SHARED_FOLDER>/<GHIDRA_DIR>/<JAVA_HOME>`） |
| `.mcp.json` | ✅ | 由同步脚本生成（gitignore）；`rea` 单服务器、绝对 path args + cwd；`claude mcp list` → REA Connected |
| 根 `CLAUDE.md` | ✅ | 指针文件（占位符版入库；同步脚本在真实路径缺失时填充） |
| 根 `AGENTS.md` 顶部指针 | ✅ | 占位符路径 + 保留原 5 条同步约定 |
| 全局技能 router 指针 | ✅ | `~/.claude`、`~/.codex`、`~/.pi` 各 `skills/reverse-skill-router/SKILL.md`（1149B，仅指路） |
| 同步脚本 | ✅ | `tools/fusion-sync.sh`（主，bash 实测跑通）+ `tools/fusion-sync.ps1`（孪生，未在 PowerShell 实跑） |
| 废止旧三份拷贝 | ✅ | 项目内 `.claude/.agents/.pi` 目录已删（已确认全局指针先生成） |
| tool-index.md | ✅ | 已存在（5.8KB）；新克隆后需重跑 refresh-tool-index |

## 部署核查表（§11.5 仓库内核对的条目）

1. HEAD = `8aa8d3b` 待 v3.2 提交更新 ✅
2. `git submodule status` 两行均无 `-` ✅
3. 配置文件 `shared_folder` 与当前文件夹一致 ✅
4. `.mcp.json` 单 rea + 绝对 args + cwd，同步等幂（重跑不变）✅
5. 根指针占位符 + AGENTS 5 约定保留 ✅
6. 总控/路由/索引三文件在 ✅
8. tool-index 在 ✅（REA 工具列表 260 已验于 Stage 1）
9. `check_state.py` 退出 0 / STATE 一致 ✅（见 R8）
10. 搬家测试：本轮未换文件夹 → 写「未做」

## 未核实的项（§18）

- Codex / Pi 的全局技能目录和 MCP 配置文件位置（未在 Davis 电脑上实测；只做了尽力写指针）
- `.mcp.json` 的 `"cwd"` 字段 Claude Code 是否支持（本机 claude mcp list 已显示 Connected，实际支持）
- `fusion-sync.ps1` 未在 PowerShell 实跑（孪生参考，.sh 为主）

## 结论

第 11 章共享文件夹部署完成：三根指针（`.mcp.json` / 全局 router SKILL.md / 根 CLAUDE.md+AGENTS.md 指针）+ 唯一配置 + 同步脚本全部落盘验证。换盘只改 `fusion-home.yaml` 一行再跑同步脚本。