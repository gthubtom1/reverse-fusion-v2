# 引擎清单门（R7 防线 2）

阶段开始第 0 步：`rea doctor` 必须有至少一个可用引擎（ghidra-headless/ghidra 为 healthy 之一）。若所有引擎都是 missing/unavailable：
- 允许的停（v3.1 规则 C 第 4 种：一个能用的引擎都没有）。
- 否则记开放项继续。

REA 验证链（R3 已真调）依赖 ghidra 可用。样本 2 的 ELF 用 Ghidra 无头 + QEMU（§9.3 后备梯）。
