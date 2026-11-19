# 部署核对清单

基线审计见 [第三方审计 §5](cases/final/THIRD-PARTY-AUDIT.md#5-部署)。旧的同名清单未出现在可用历史中。本清单记录当前仓库的核对顺序与证据。

| 项 | 核对方式 | 当前证据 |
|---|---|---|
| 1. Git 与锁定源码 | `git submodule status`，比对 `lifecycle/versions.lock` | 原工作区两项一致。新机器下载待验。 |
| 2. Claude Code 项目入口 | 读根目录 `CLAUDE.md` | 追踪文档。 |
| 3. 通用项目入口 | 读根目录 `AGENTS.md` | 追踪文档。 |
| 4. 宿主技能发现 | 逐一核对当前宿主实际加载的路径 | 宿主级发现未验。 |
| 5. Claude Code MCP | 核对项目 `.mcp.json` 的有效路径与宿主显示 | 仓库旧配置含本机路径。实际本地配置由使用者管理。 |
| 6. Codex MCP | 核对本机 Codex 的 `config.toml` 与 `codex mcp list` | 此仓库没有 Codex 配置回执。 |
| 7. Pi | 核对当前客户端扩展和工具列表 | Pi/MCP 接线未验。 |
| 8. REA 技能隔离 | 检查宿主列表和子模块目录 | 聚合根未发现项目级副本。REA 子模块自带技能。 |
| 9. 运行依赖 | 对照 `versions.lock` 和本机版本 | 安装与 provider 体检是原机器历史记录。 |
| 10. REA 构建 | 核对 `engine/rea/dist/mcp/main.js` | 未进入 Git。入口缺文件时显示构建提示。 |
| 11. 工具索引 | 核对 `core/skills/tool-index.md` 的存在与来源 | 忽略产物。新检出默认缺失。 |
| 12. 同步脚本 | 先核对脚本写目标、语法和模板 | 历史 Bash 回执在 `cases/deploy/`。PowerShell 解析失败。两版均会写宿主级文件，自动部署未验。 |
| 13. STATE | `python -I lifecycle/check_state.py` | 以包含 STATE 更新的 Git 提交为检查点。运行 `git fetch origin main` 后，可加 `--require-origin-main` 比对缓存远端引用。 |

干净检出可先运行静态路由表检查与机械交接检查，两者不依赖样本二进制、REA 构建或宿主配置。命令与预期结果见 [独立验收单](cases/final/THIRD-PARTY-ACCEPTANCE.md)。历史安装步骤见 [Stage 1](cases/stage1/STAGE1-REPORT.md) 和 [Stage 2](cases/stage2/WIRING.md)。第二台机器的安装、启动与回执仍待验收。
