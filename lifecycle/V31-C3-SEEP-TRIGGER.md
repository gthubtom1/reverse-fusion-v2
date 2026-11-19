# V3.1 C3：Seep 分支触发条件（记录在计划层，不污染路由表）

日期：2026-11-20。v2.1 §1.4 第 87 行「带许可证校验、加壳的 PE、APK → Seep 提取件」是冻结文件原文，**不改动**（v2.1 冻结）。本文件在 v3.1 执行层给出可检查的触发条件，供 Track B 使用。

## 触发条件（满足任一条 → 走 Seep 分支 / Track B）

1. 目标是 PE/APK，且提示词/任务里有「许可证校验 / 卡密 / 加壳 / 壳 / 授权验证 / license / crackme serial」任一。
2. 或 REA 对目标返回 `target_format_unsupported` 以外的 provider 失败，且案子记录里写明「疑似加壳 / 许可证校验」。

## 在本执行（R1–R8，无 Track B 授权）的处理

- 遇到触发条件：**只记录到案子的 timeline.md / 开放事项**，不调用 Seep（Track B 未授权）。
- 记录格式：`seep_trigger: 命中（原因……）→ Track B 待执行`。
- 不因 Seep 未调而停下（v3.1 §9.3「永远不许停」）。

## 依据

- `FUSION-FINAL-v3.1.md` 第 3.2 节。
- v2.1 §1.4 第 87 行（冻结原文，不动）。