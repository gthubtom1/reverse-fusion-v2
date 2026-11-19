# 验收报告：样本 2

日期：2026-11-20（北京时间）。标准按 `FUSION-FINAL-v2.1.md` §5.4、§5.5，并按用户本轮对样本 2 的口径：无效输入拒绝 + 验证算法复现。

**结论：本轮口径通过。** 原版在 QEMU 中真跑；2 个由 keygen 生成的序列号被接受、3 个无效输入被拒绝；哈希表生成与运行时 dump 逐字节一致。R46 的 L5 没有声明通过（keygen 不复刻提示文字等副作用，哈希用机器码模拟而非高级语言重写）。

## 1. 结构比对

- 文件：ELF 64-bit x86-64，静态链接，stripped，SHA-256 `8b685085…8804`。
- REA（Windows）拒绝 ELF：`target_format_unsupported: Windows Ghidra P0 accepts native PE, DOS MZ...`。证据 `evidence/E-002-overview.json`。
- 改用 Ghidra 12.2 无头模式；entry 0x401b00 → `__libc_start_main` 的 main 参数 0x401640。证据 `evidence/E-003-main-decompile.txt`。
- 校验循环在 0x4019ab–0x401aa4；哈希函数在 0x401d80。

## 2. 行为对照

| 用例 | 输入 | 原版 | keygen 预测 | 一致 |
|---|---|---|---|---|
| TC1 | alice / bob@example.com / 16 字节序列号 | accepted（flag） | accepted | 是 |
| TC2 | davis / davis@test.com / 16 字节序列号 | accepted（flag） | accepted | 是 |
| TC3 | 16 个 `A` | denied | denied | 是 |
| TC4 | `ABC`（长度 3） | denied | denied | 是 |
| TC5 | 64 个 `A` | denied | denied | 是 |

命令：`python -I cases/sample-2/reimpl/run_cases.py <sample> /d/tmp/s2cases.json cases/sample-2/evidence/E-005-five-cases.json`
输出：`[["TC1","accepted",0],["TC2","accepted",0],["TC3","denied",1],["TC4","denied",1],["TC5","denied",1]]`
原始 stdout 与退出码：`evidence/E-005-five-cases.json`。

另有五个纯无效输入用例（空输入、只有姓名、伪序列号、64 字符、短串）全部 denied，见 `evidence/E-003-invalid-inputs.json`。

## 3. 验证算法复现

- 表生成：`reimpl/emulate_hash.py` 用 Unicorn 模拟 0x401d80。对 alice 与 davis 两组输入，模拟结果与 gdb 断在 0x4019f2 时从 `rbx` dump 的 256 字节表逐字节一致（`evidence/E-006-table-verify-*.txt`，`match True`）。
- 校验规则：`reimpl/keygen.py` 的 `check()` 按 0x4019ab 的汇编重写：长度 16、`n=17`、i 取 0/3/6/9/12/15、三元组不等式 + `serial[(i+3)%17] == table[i]*4`（有符号 32 位）。
- 生成器：`python -I cases/sample-2/reimpl/keygen.py <elf> <name> <email>` 输出 16 字节序列号；alice 与 davis 两组都由它生成，并交给原版验收通过。

**限制：** H 没有用高级语言重写，而是模拟原版机器码。它依赖原始 ELF 的 0x401d80 代码，不能算“脱离原程序的独立实现”。这一点直接影响下面的 L4/L5 判定。

## 4. 独立运行

keygen 可脱离原程序进程运行（它只读 ELF 的代码段做模拟，不启动原程序）。但它仍依赖原 ELF 文件本身，不是从零重写的等价程序。

## 5. 比较器自检

用错误序列号（TC3–TC5）与原版对照，三次都判 denied；把序列号字节改错（TC2 的 0x04 位置）同样 denied。未单独做“坏变体被检查器发现”的脚本化自检。

## 6. 未知项

见 [unknowns.md](unknowns.md)。

## 7. 判定

- 用户本轮口径（无效输入拒绝 + 验证算法复现）：**通过**。2 个有效序列号被原版接受，3 个无效输入被拒绝，规则与表生成都有运行时对照。
- R46 L4：**部分通过**。行为对照通过，但“独立实现”依赖原 ELF 的哈希机器码，不是完全独立重写。
- R46 L5：**未声明通过**。没有复刻提示文字/退出行为等副作用面。
- Seep：未使用。样本没有加壳或反调试；字符串混淆由哈希与运行时解密处理，本轮没有调用 Seep（第三个项目记为以后再说）。
