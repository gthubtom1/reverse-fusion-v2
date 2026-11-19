# 第三方独立审计

审计基线为 `cd99b9c424138e30c6840f57553bfb37cd001830`。`git fetch --no-tags origin main` 后，`git rev-list --left-right --count HEAD...origin/main` 返回 `0 0`。使用只读仓库检查、干净检出和 dry-run。历史记录、当前复现和仍待独立验收的项目分别标注。

## 1. 路由

- 项目入口是 [`core/skills/SKILL.md`](../../core/skills/SKILL.md)。交接点名的 `core/SKILL.md` 不存在。根 [`AGENTS.md`](../../AGENTS.md) 和 [`CLAUDE.md`](../../CLAUDE.md) 指向前者。`git -C engine/rea ls-files '*SKILL.md'` 返回 6 个 REA 本身的技能文件，其中 `.agents/skills` 下有 5 个。当前聚合根目录的 `.claude/skills`、`.agents/skills`、`.pi/skills` 均不存在。由此可核实仓库根没有第二份项目级总控，宿主全局加载状态仍需逐宿主验证。
- 下表分别运行 `bash core/skills/scripts/master-route.sh --hint "$hint" --dry-run` 和 `powershell.exe -NoProfile -File core/skills/scripts/master-route.ps1 -Hint "$hint" -DryRun`。结果与置信度一致，八项均退出 0。JS、PE、ELF 的裸格式提示落入通用回退，因此退出 0 不能作为专用路由命中的证据。[路由配置](../../core/skills/config/routing.json)

| 提示词 | Bash 与 PowerShell 的 PRIMARY | 置信度 |
|---|---|---|
| `JavaScript` | `reverse-engineering` | low |
| `APK` | `apk-reverse` | high |
| `PE file` | `reverse-engineering` | low |
| `ELF file` | `reverse-engineering` | low |
| `复刻这个APK` | `reconstruction` | high |
| `复刻这个 APK` | `reconstruction` | medium |
| `reconstruct this apk` | `reconstruction` | medium |
| `rebuild this apk` | `reconstruction` | medium |

- Seep 触发条件存在于 [`V31-C3-SEEP-TRIGGER.md`](../../lifecycle/V31-C3-SEEP-TRIGGER.md)，其中第 10–13 行明确主线只记录。`git submodule status` 仅列出 REA 和 reverse-skill。Seep 仅检查 Git 树，未安装、注册或执行。
- [`unique_router.py`](../../lifecycle/defenses/unique_router.py) 第 10–18 行只按调用者当前目录检查文件名，既不验证 JSON，也不验证技能指针。现有 `OK` 不能解释为启动路由或宿主发现通过。

## 2. 证据链

- 逐个对八份 `cases/*/reconstruction-handoff.md` 正则计数 `\bev_[0-9a-f]{64}\b`，八份均为 0。样本 1 的 [`EVIDENCE-MAP.md`](../sample-1/EVIDENCE-MAP.md) 第 7–14 行有 5 个完整 `ev_`，其中清单通过 E-005 间接关联校验函数证据。样本 2 的 [`EVIDENCE-MAP.md`](../sample-2/EVIDENCE-MAP.md) 第 7–17 行记录了无 `ev_` 及平台拒绝原因。仓库仅追踪样本 1、2 两份真实清单。其余六份人读交接未见同级机器清单。
- 使用 `python -I core/skills/reconstruction/scripts/check_handoff.py . cases/sample-N/notes/handoff-manifest.json`。原 Windows 检出 `core.autocrlf=true`，样本 1 `PASS` 11 个文件、样本 2 `PASS` 15 个文件。用 `git -c core.autocrlf=false worktree add --detach <空路径> <基线>` 创建干净检出后，两份均 `FAIL sha256.mismatch`。首个失败字段分别为 `requirements[0].evidence_refs[0].record_ref`、`context_refs.workitems`。逐一比对 Git blob 和 CRLF 还原字节后，12 个承诺值对应 CRLF，14 个对应 Git 原始字节。验收依赖换行设置。
- 机械检查只校验路径、散列、引用结构。语义、证据真实性与目标运行未验证。真实 Codex 往返未做，原 [`CODEX-RECEIPT.md`](../sample-1/CODEX-RECEIPT.md) 已写明。[检查器返回字段](../../core/skills/reconstruction/scripts/check_handoff.py#L234)

## 3. 上游工具与本地实现

[`tools-list-rea.json`](../stage1/tools-list-rea.json) 的 260 工具是历史握手清单。针对 v3.2 的八个行为样本，已在样本 1 的 E-010/E-012 找到 `export_evidence_bundle`、`compare_functions` 成功证据各一次，E-013 有 `verify_reconstruction` 调用一次并返回 `invalid_request`。E-011 是比较尝试，不能算成功。其余样本未见这几项的成功回执。`compare_artifacts` 未见成功或调用回执。逐案实际分析和比较记录如下。

| 样本 | 上游能力位置 | 实际记录及本地代码 |
|---|---|---|
| PE | [`reconstruction/SKILL.md`](../../core/skills/reconstruction/SKILL.md)，REA 的 `binary_overview`、`compare_functions`、`export_evidence_bundle` | REA 原始答复和本地差分有历史记录。源码语义对比与输入输出差分各自独立。[验收](../sample-1/ACCEPTANCE.md) |
| ELF | [`ghidra-reverse/SKILL.md`](../../core/skills/ghidra-reverse/SKILL.md)，REA `binary_overview` | REA 平台拒绝后使用 Ghidra、gdb、QEMU 和 Unicorn。机器码模拟限制另列。[验收](../sample-2/ACCEPTANCE.md) |
| JS | [`js-reverse/SKILL.md`](../../core/skills/js-reverse/SKILL.md) | 历史记录描述浏览器观察与 Node 本地实现。未见 JS MCP 运行回执。[验收](../js-1/ACCEPTANCE.md) |
| APK | [`apk-reverse/SKILL.md`](../../core/skills/apk-reverse/SKILL.md) | jadx 与 JVM/Node 对照。缺少 dex/APK 实机验收。[验收](../apk-1/ACCEPTANCE.md) |
| 扩展 | [`browser-extension-reverse/SKILL.md`](../../core/skills/browser-extension-reverse/SKILL.md) | 解包与本地对照。缺安装到浏览器的实测。[验收](../ext-1/ACCEPTANCE.md) |
| 协议 | [`protocol-reverse/SKILL.md`](../../core/skills/protocol-reverse/SKILL.md) | 本机 loopback 抓包及本地解码器。工具目录与活动证据分开。[验收](../protocol-1/ACCEPTANCE.md) |
| 算术验证码样例 | [`browser-automation/SKILL.md`](../../core/skills/browser-automation/SKILL.md) | 自建 fixture 与本地实现的历史记录。未复测第三方验证码。[验收](../captcha-1/ACCEPTANCE.md) |
| Windows/.NET | [`dotnet-reverse/SKILL.md`](../../core/skills/dotnet-reverse/SKILL.md)，REA `compare_managed_members` | 自建 .NET 样例与本地 Python 对照。未见 REA 比较回执。[验收](../netwin-1/ACCEPTANCE.md) |

额外的 Go 历史验收另见 [`gorust-1/ACCEPTANCE.md`](../gorust-1/ACCEPTANCE.md)，浏览器观察另见 [`automation-1/ACCEPTANCE.md`](../automation-1/ACCEPTANCE.md)。`git ls-files 'cases/*/*/comparator_check*'` 列出 7 个旧入口。共享实现存在，但不能从 R6 增补文字推断旧程序都调用了它。后续只以源码导入或实际调用为证。

## 4. 领域

锁定 reverse-skill Git 树中，`skills/*/SKILL.md` 有 44 条。历史 [`DOMAIN-VERDICTS.md`](DOMAIN-VERDICTS.md) 混用场景、技能名和交叉支撑，无法按路径核对。第 27 行标题称 19 项，表实体为 21 行。第 22、64 行称 Go 未做，与 [`gorust-1/ACCEPTANCE.md`](../gorust-1/ACCEPTANCE.md) 的 Go 历史验收和 [`MANIFEST.yaml`](../../lifecycle/MANIFEST.yaml#L135) 冲突。Rust 仍缺验收。用锁定路径作键的表可区分历史、支撑、待测与范围外。

## 5. 部署

`git log --all -- FUSION-REVIEW-v3-AUDIT.md DEPLOYMENT-INVENTORY.md` 无输出。两份点名文件在基线检出均缺失。无法核对原清单的逐字 13 项。下表按交接涉及的可验证事项建立替代核对表。

| # | 检查点 | 基线结论 |
|---|---|---|
| 1 | 克隆与上游 | 两个子模块 HEAD 与锁定表一致。干净 worktree 实测，不代表新机器重装。 |
| 2 | Claude 项目入口 | 根 `CLAUDE.md` tracked。 |
| 3 | 通用项目入口 | 根 `AGENTS.md` tracked。 |
| 4 | 项目级技能 | `.claude/skills`、`.agents/skills`、`.pi/skills` 在本次检出均缺失。 |
| 5 | Claude MCP | tracked `.mcp.json` 与模板存在。当前本地 `.mcp.json` 有既有修改，未用于发布。 |
| 6 | Codex MCP | 两个同步脚本只写 Claude JSON，没有 Codex 的独立 MCP 配置写入。本轮未运行 Codex。 |
| 7 | Pi MCP | 未见 Pi MCP 项目接线或真实运行回执。 |
| 8 | REA skill 隔离 | 子模块自带 REA 技能，聚合根没有同名项目级副本。宿主级隔离未核实。 |
| 9 | Node、Ghidra、Java | 本机历史诊断见 [安装](../stage1/STAGE1-REPORT.md)和[接线](../stage2/WIRING.md)。新机器版本及 provider 未测试。 |
| 10 | REA dist | 现有检出 `engine/rea/dist` 存在，Git 树无追踪 dist。缺失时入口会报告需要构建。[入口](../../engine/rea/scripts/rea.mjs#L60) |
| 11 | 工具索引 | `git check-ignore -v core/skills/tool-index.md` 命中 `core/.gitignore:39`。历史生成记录不能充当新机器索引。 |
| 12 | 同步脚本 | [历史部署材料](../deploy/DEPLOY-REPORT.md)记录了 Bash、未测 PowerShell。PowerShell 使用 `$key:`，会被解析成作用域变量，还在 JSON 解析前插入未转义路径。两个脚本均可能写宿主级设置，本轮只检查静态输入和语法。 |
| 13 | STATE | 字段为 `6756be7…`，基线 HEAD 为 `cd99b9c…`。`git rev-list --left-right --count HEAD...6756be7` 返回 `8 0`，旧检查误报“本地 HEAD 落后”并退出 0。根因见 [`check_state.py`](../../lifecycle/check_state.py#L68)。将当前提交号写入其包含的文件会产生新提交号，无法按原流程收敛。 |

R9 快照文件夹 [`v3.2-R9-T1`](../../v3.2-R9-T1/PI-CHECKLIST.md) 只包含说明和目标提交号。在目录中运行 `git rev-parse --show-toplevel HEAD` 仍定位父仓库及其 HEAD。`PI-PASS.md` 不存在。

## 6. 数字

- 锁定上游树和 `HEAD:core/` 分别为 675 条追踪文件路径。`git ls-tree -r -z --name-only` 做集合差，两侧各独有 0 条。`git ls-tree -r -z` 比 blob 哈希得 5 个内容差异，分别是 `README_zh.md`、`VERSION`、`docs/RELEASE-CHECKLIST.md`、`skills/config/routing.json`、`skills/routing_zh.md`。
- 恢复提交 `e4ec16b` 的 `core/` 前后路径分别为 208 和 675。前后集合差新增 541、移除 74、路径沿用 134，净增 467。469 无已核实的统计依据。净增与新增路径代表不同指标。
- GitHub `repos/angusdevgo/Seep-Reverse-Lab/git/trees/1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e?recursive=1` 返回 `truncated=false` 和 4,942 个 blob。`Tool/cases/` 下直接识别 14 个项目目录 A–N。入口为 `Tool/mcp/seep_mcp_server.py`。195、294、321 的知识库正文口径未核实，文件后缀和路径计数不能证明正文数量。38 个工具为历史记录，当前没有服务握手证据。

## 7. 接手与运行风险

| 视角 | 触发点 | 发现方式 | 防线 |
|---|---|---|---|
| 运营 | 新检出即读取缺失旧审计 | `git log --all -- <文档>` 与 `Test-Path` | 仓库入口先定位当前审计及部署清单。 |
| 产品 | 看到历史状态就误以为可全领域重跑 | 逐条检查实际验收、真实宿主回执与缺项 | 分开列历史、机械检查、设备实测和独立验收。 |
| 工程 | 没网、没有 dist 或原始样本 | 检查本机产物、子模块和样本目录 | 保留只读核对入口，缺项留开放，不下载或运行替代物。 |
| 工程 | 切换系统后证据散列改变 | 同一提交以两种换行配置检出并跑原检查器 | 固定承诺文件的检出字节。 |
| 工程 | 配置切换主目录时覆盖项目或客户端设置 | 对照同步脚本的写目标，核查 `git status` | 部署检查与写入分开，对现有本地配置单独处理。 |

缺失历史审计、清单原文、Codex 往返、Pi 全新会话、第二台机器部署及全量案例重跑均列开放。独立验收不沿用本轮作者检查结果。
