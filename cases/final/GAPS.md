# v3.1 缺口清单（R8）

日期：2026-11-20。对照 v3.1 §10 十二条完成标准逐项；**有 2 项部分达标、若干领域推迟，不宣称「100% 全部做到」**。

## 部分达标（有证据但没到满）

| 缺口 | 状态 | 原因 / 下一步 |
|---|---|---|
| G1 真 Codex 往返 | 部分 | 无 Codex CLI/会话；`CODEX-RECEIPT.md` 记电脑智能体交付。下一步：有 Codex 会话后补一次真往返。 |
| G2 ledger/verify/coverage 工具未拼参调用 | 部分 | 三个工具存在，schema 可查，但参数需会话内构造（evidence_bundle/reviewed_obligations/coverage）；R3 已记确切情况。下一步：会话内构造后调。 |

## 推迟领域（verdict 明确）

| 领域 | 状态 |
|---|---|
| Rust（Stage 14 的一半） | 未测（本机无 Rust 目标；`go-rust-reverse` 技能要求 Rust toolchain） |
| 恶意软件（Stage 15） | 范围外（安全门：本执行不测恶意软件） |
| 固件（Stage 16） | 推迟（无合法固件样本 + 设备） |
| macOS / iOS | 推迟（Windows 电脑无法测 / 要 iOS 设备） |

## 一贯开放项

- `FUSION-REVIEW-v3-AUDIT.md` 不在仓库（v3 引用但未提交）；按 v3.1 正文/改动清单执行，缺口记为 open。
- `bootstrap-reverse.ps1/.sh` 未逐对 diff（TWIN-TABLE 记 open）。
- 样本均为自建/公开练习；真实第三方样本（APK/扩展/站点）的逆向仍缺（网络不稳）。

## 结论

除 G1/G2 与推迟领域外，§10 十二标准的其余全部达成（均有提交+命令证据）。不写「100% 完成」。