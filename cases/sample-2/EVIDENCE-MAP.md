# 样本 2 证据对应表（E- → ev_）

一个 E 号只指一个文件；多文件已拆分（a/b/c）。样本 2 的 E-003/E-004/E-006 原为多文件，已按单文件拆分。

| E 号 | 指的文件 | 对应 REA ev_ 号 | 说明 |
|---|---|---|---|
| E-002 | `evidence/E-002-overview.json` | 无（REA 返回 target_format_unsupported，无证据产出） | REA open_binary+overview 平台拒绝记录 |
| E-003a | `evidence/E-003-invalid-inputs.json` | 无（本机 QEMU 运行输出） | 5 个无效输入拒绝 |
| E-003b | `evidence/E-003-main-decompile.txt` | 无（Ghidra 无头反编译） | main 反编译 |
| E-004a | `evidence/E-004-gdb-dump.txt` | 无（gdb 断点） | 运行时表 dump |
| E-004b | `evidence/E-004-table-alice.bin` | 无（gdb 导出） | alice 表 |
| E-004c | `evidence/E-004-table-davis.bin` | 无（gdb 导出） | davis 表 |
| E-005 | `evidence/E-005-five-cases.json` | 无（QEMU 运行） | 5 用例（2 合法+3 无效） |
| E-006a | `evidence/E-006-table-verify-alice.txt` | 无（模拟 vs dump 对照） | alice 表一致性 |
| E-006b | `evidence/E-006-table-verify-davis.txt` | 无（模拟 vs dump 对照） | davis 表一致性 |

说明：样本 2 的 REA 在 Windows 不支持 ELF（`target_format_unsupported`），故无 REA `ev_` 证据；按 v3.1 §5.1，无 REA 证据号的条目注明原因（平台限制）。「哈希用 Unicorn 模拟原版机器码」是 unknowns 记录的主要限制，不影响本表完整性。