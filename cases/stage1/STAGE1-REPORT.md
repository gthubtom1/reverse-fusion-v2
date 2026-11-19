# 第 1 阶段报告：签出、安装、工具列表

日期：2026-11-20（北京时间）。范围：REA 与 reverse-skill 两个项目。Seep 未签出、未安装，记为「以后再说」。

**结论：两个项目都已装上并通过本机验证；REA MCP 的 `tools/list` 返回 260 个工具。安装回执 `installed=true`，见 [INSTALL-RECEIPT.json](INSTALL-RECEIPT.json)。** 未通过项和限制在每节末尾单列，不混算。

## 1. 本地签出

详细命令和输出见 [LOCAL-CHECKOUT.md](LOCAL-CHECKOUT.md)。摘要：

| 项目 | 本地 HEAD | 锁定提交 | 判定 |
|---|---|---|---|
| REA | `4491c84c82140a43fa12390b727840a433875ba8` | `4491c84c82140a43fa12390b727840a433875ba8` | 一致 |
| reverse-skill | `ce675096e6a2cd4789a76f9bd618feddc2b6f333` | `ce675096e6a2cd4789a76f9bd618feddc2b6f333` | 一致 |

`git submodule status` 两条记录的提交号与上表相同；签出位置为 `engine/rea`、`upstream/reverse-skill`。

## 2. REA 安装

### 2.1 环境问题与处理

1. REA `package.json` 要求 Node `^22.23.4 || ^24.22.1 || >=26.12.1`，`.npmrc` 设 `engine-strict=true`。本机默认 Node `v24.20.0`，`npm ci` 返回 `EBADENGINE`。
2. 下载官方 `v24.22.1` 到 `D:/Tools/node-24.22.1/node-v24.22.1-win-x64` 后，`npm ci` 仍在本机 npm 生命周期脚本处失败：`esbuild` 的 `node install.js` 由 npm 拉起的 `cmd.exe` 执行，该子进程的 `PATH` 为空，报 `'node' 不是内部或外部命令`。`scripts-prepend-node-path=true` 同样失败。这是本机执行环境的 `cmd.exe` 环境变量问题，不是 REA 仓库的问题（用 `cmd /c "set PATH=... && node -v"` 可复现并证实）。
3. 改用 `npm ci --ignore-scripts` 完成依赖安装（`added 735 packages`），再单独执行 `npm run compile`（`clean-build-output → tsc -p tsconfig.build.json → record-catalog-digests → record-mcp-catalog → record-cli-commands → bundle-runtime`），`COMPILE_EXIT=0`，`dist/` 生成 3,483 个文件。

### 2.2 本机验证

| 检查 | 命令 | 结果 |
|---|---|---|
| 版本 | `node.exe scripts/rea.mjs --version` | `6.9.0` |
| MCP 握手 + 工具列表 | `python cases/stage1/mcp_probe.py <node> engine/rea/scripts/rea.mjs cases/stage1/tools-list-rea.json mcp` | `initialize_ok=true`，`serverInfo={"name":"rea","version":"6.9.0"}`，`tools_list_ok=true`，`tool_count=260` |
| Claude Code 注册 | `claude mcp add -s local rea -- <node.exe> <rea.mjs> mcp`；`claude mcp list` | `rea: ... - ✔ Connected` |
| 关键工具名 | 从 `tools-list-rea.json` 的 `tool_names` 中查找 | `compare_functions`、`compare_artifacts`、`export_evidence_bundle`、`compare_managed_members` 四项都存在 |

这四项在 v2.1 §5.2 里是「固定版本文档已核」；本次本机 `tools/list` 把它们升级为「本机工具列表已核」。完整 260 项见 [tools-list-rea.json](tools-list-rea.json)。

### 2.3 doctor 结果（未全部通过，照实记）

`node.exe scripts/rea.mjs doctor` 首行 `healthy: false`。健康项：`node`、`host`、`ghidra`、`ghidra-platform`、`ghidra-architecture`、`ghidra-installation`、`ghidra-headless`、`ghidra-native_decompiler`。不健康项：

| 检查 | 状态 |
|---|---|
| `hopper` | `missing_analysis_engine` |
| `ida-registration` | `missing_analysis_engine` |
| `jadx` | `missing_dependency` |
| `ghidra-java` | `runtime_failure` |
| `ghidra-version` | `config_drift` |

完整输出见 [rea-doctor.txt](rea-doctor.txt)。`doctor` 的 `healthy: false` 不等于 MCP 没装上：服务已完成握手并列出 260 个工具。但 `ghidra-java` 失败可能影响后续原生分析，第 3 阶段遇到时按实际结果记录。

## 3. reverse-skill 安装

按 v2.1 §4.1 保留 15 个模块（总控 `SKILL.md` + 14 个目录），从锁定提交复制到 `core/`：

- 保留的 14 个目录：`reverse-engineering`、`reconstruction`、`js-reverse`、`apk-reverse`、`dotnet-reverse`、`binary-diff`、`protocol-reverse`、`ghidra-reverse`、`ida-reverse`、`radare2`、`binary-ninja-reverse`、`mobile-reverse`、`case-review`、`docs-generator`。
- 删除：`core/skills/reverse-engineering/dsl-vm-reverse`（v2.1 §4.3 第 6 条）。
- 支撑文件另放 `core/support/`（`config`、`ops`、`scripts`、`references`、`INDEX.md`、`routing.md`、`routing_zh.md`、`MASTER-ROUTING.md`），因为总控的 hot path 直接引用 `config/routing.json` 与 `ops/`。`core/skills/` 下的模块数是 14，加根 `SKILL.md` 共 15，符合 v2.1 §4.1。
- `core/` 共 208 个文件、约 2.2 MB。

三处数字已按 v2.1 §4.5 修正（只改 `core/` 副本，未改上游子模块）：

| 文件:行 | 原值 | 新值 |
|---|---|---|
| `core/README_zh.md:236` | `175 条` | `192 条` |
| `core/support/routing_zh.md:261` | `63 工具` | `78 工具` |
| `core/docs/RELEASE-CHECKLIST.md:16` | `当前 25 项` | `当前 26 项` |

安装到三个位置：`.claude/skills/`、`.agents/skills/`、`.pi/skills/`，每个位置含 `reverse-skill-router/SKILL.md`（总控 + 14 模块 + 支撑文件）和 `reconstruction/SKILL.md`（R46 独立入口）。命令：

```bash
for base in .claude .agents .pi; do
  mkdir -p "$base/skills/reverse-skill-router" "$base/skills/reconstruction"
  cp -r core/. "$base/skills/reverse-skill-router/"
  cp -r core/skills/reconstruction/. "$base/skills/reconstruction/"
done
```

工具检查：`python -I core/skills/reconstruction/scripts/check_handoff.py --help` 正常输出用法（`project_root`、`manifest`、`--format {json,markdown}`），退出码 0。实际案子校验留到第 2 阶段。

## 4. 安装回执

[INSTALL-RECEIPT.json](INSTALL-RECEIPT.json)：`installed: true`，`scope: ["rea","reverse-skill"]`，`deferred: ["seep"]`，并逐项记录证据和限制。

## 5. 未做与未核实

- Seep 未签出、未安装、未抽取。
- 没有启动 Ghidra/IDA 实际分析目标；只验证了 REA MCP 的握手和工具目录。`doctor` 的 `ghidra-java` 失败未修复。
- `.mcp.json` 里的项目级 `rea` 在 Claude Code 中显示「Pending approval」，同端点已用 local scope 注册并通过 `claude mcp list`（Connected）。两种 scope 并存会产生一条端点不一致警告，不影响本次连接。
- 未验证 `npx rea-agents@6.9.0` 的联网安装路径；本机用的是源码签出 + 编译产物。
- 三个技能副本未做内容哈希互比，只核对了 `SKILL.md` 存在。

## 6. 依据

- 锁定表与范围：`FUSION-FINAL-v2.1.md` §2、§4.1、§4.3、§5.2、§7。
- 签出证据：`cases/stage1/LOCAL-CHECKOUT.md`。
- 工具列表原始输出：`cases/stage1/tools-list-rea.json`（含 `raw_initialize`、`raw_tools`、`stderr_tail`）。
- doctor 原始输出：`cases/stage1/rea-doctor.txt`。
