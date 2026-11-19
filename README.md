# reverse-fusion-v2 | 第 1–3 阶段执行交接

这个仓库保存冻结方案、四条勘误写入后的 v2.1、第 1–3 阶段的安装与样本记录。供独立复核。

当前状态（2026-11-20）：

| 阶段 | 状态 | 入口文件 |
|---|---|---|
| 方案 | v2.1 已写入四条勘误，v2.0 原文保留 | [FUSION-FINAL-v2.1.md](FUSION-FINAL-v2.1.md) · [FUSION-FINAL-v2.md](FUSION-FINAL-v2.md) |
| 第 1 阶段 | 签出、安装、工具列表、安装回执完成 | [STAGE1-REPORT.md](cases/stage1/STAGE1-REPORT.md) · [INSTALL-RECEIPT.json](cases/stage1/INSTALL-RECEIPT.json) |
| 第 2 阶段 | REA MCP 接线、证据落盘、交接单模板完成 | [WIRING.md](cases/stage2/WIRING.md) |
| 第 3 阶段 | 样本 1 达到 L4；样本 2 达到本轮口径 | [STAGE3-REPORT.md](cases/stage3/STAGE3-REPORT.md) |
| 第 4 阶段 | 未开始 | — |

样本：

| 样本 | 结果 | 报告 |
|---|---|---|
| 样本 1（Windows x86-64，XOR） | 5/5 核心用例一致；L4 通过，L5 未声明 | [ACCEPTANCE.md](cases/sample-1/ACCEPTANCE.md) |
| 样本 2（ELF x86-64，自定义哈希） | 2 个有效序列号被接受、3 个无效输入被拒绝；验证规则与表生成已复现 | [ACCEPTANCE.md](cases/sample-2/ACCEPTANCE.md) |
| 样本 3（UPX/反调试） | 未执行 | — |

关键事实与限制：

- 两个上游都签出在锁定提交：REA `4491c84…`，reverse-skill `ce67509…`。Seep 本轮未签出、未安装（以后再说）。
- REA MCP 本机 `tools/list` 返回 260 个工具，`compare_functions`、`compare_artifacts`、`export_evidence_bundle`、`compare_managed_members` 均存在。
- REA 的 Windows Ghidra P0 只接受 PE/MZ，不支持 ELF；样本 2 的静态分析改用 Ghidra 12.2 无头模式与 gdb（见样本 2 报告）。
- 两个样本都没有声明 L5；样本 2 的哈希用 Unicorn 模拟原版机器码，不是高级语言独立重写。
- `lifecycle/MANIFEST.yaml` 记录了锁定版本、安装状态、阶段状态和已知限制。

其他文件：

| 文件 | 用途 |
|---|---|
| [AGENTS.md](AGENTS.md) | 本项目交接约定 |
| [CHANGE-REQUEST.md](CHANGE-REQUEST.md) | 四条勘误及其实施状态 |
| [REVIEW-2.md](REVIEW-2.md) | 独立复核与修订建议 |
| [VALIDATION-REPORT.md](VALIDATION-REPORT.md) | 第 0 步 15 项复核（历史结论） |
| [cases/validation/](cases/validation/) | 第 0 步笔记、复核和停点记录 |
| [cases/samples/MANIFEST.md](cases/samples/MANIFEST.md) | 三个样本的来源与指纹 |
| [cases/templates/reconstruction-handoff.md](cases/templates/reconstruction-handoff.md) | 复刻交接单模板 |

复核时请区分「有命令输出支持」「有文件行号支持」「未核实」。本仓库不把未执行的阶段写成通过。
