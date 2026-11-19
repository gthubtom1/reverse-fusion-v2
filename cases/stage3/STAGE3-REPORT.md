# 第 3 阶段报告：样本 1、样本 2

日期：2026-11-20（北京时间）。范围：前两个项目（REA、reverse-skill）。样本 3 未执行；Seep 未参与（第三个项目记为以后再说）。

**结论：样本 1 达到 L4；样本 2 达到用户本轮口径（无效输入拒绝 + 验证算法复现）。两者都没有声明 L5。** 逐项证据见各自案子的 `ACCEPTANCE.md`。

## 1. 样本 1（CrackMe.exe，Windows x86-64）

- 目标 SHA-256：`945e81e113e09002db42b26f69cd43de564c32a03971fdf335e2f81caca6c67a`，与登记一致。
- 流程：REA `open_binary` → `binary_overview` → `list_procedures`（701 个函数）→ 反编译 main（0x140017cd0）与校验（0x1400173d0）。
- 算法：`strlen == 6` 且 `input[i] == [0x38,0x27,0x64,0x66,0x66,0x62][i] ^ 0x55`，密码 `mr1337`。
- 运行环境：原版需要调试版 CRT；本机补 `ucrtbased.dll`（Windows SDK 10.0.26100）与 `msvcp140d.dll`、`vcruntime140d.dll`、`vcruntime140_1d.dll`（VS Build Tools 14.44.35112）后可运行。
- 五个核心用例 5/5 一致（`cases/sample-1/evidence/E-006-differential.json`）；六个边界用例 6/6 一致（`E-008-boundary.json`）；坏变体被比较器发现（`E-007`）。
- 判定：**L4 通过**；L5 未声明（控制台副作用未复刻）。详见 `cases/sample-1/ACCEPTANCE.md`。

## 2. 样本 2（howo-not-to-simple-keygen，ELF x86-64）

- 目标 SHA-256：`8b685085320c61337679f34eedc5aa338b5cc38c782ab5034581f33ae6c08804`，与登记一致。
- REA 平台限制：Windows Ghidra P0 只收 PE/MZ，`binary_overview` 返回 `target_format_unsupported`（`evidence/E-002-overview.json`）。改用 Ghidra 12.2 无头模式与 gdb，不阻塞阶段。
- 运行环境：本机无 WSL/Docker，安装 QEMU 11.1.0 + Alpine 6.18 virt 内核 + 静态 busybox，自制 initramfs 启动原版（`cases/stage3/qemu_run.py`、`initramfs_build.py`）。
- 算法：
  - `table = H(H(name) || H(email))`，H 为 0x401d80，返回 256 字节；
  - 序列号 16 字节，n=17，对 i=0,3,6,9,12,15：三元组不等式成立时，要求 `serial[(i+3)%17] == (signed char)table[i]*4`。
- 复现：
  - `reimpl/emulate_hash.py` 用 Unicorn 模拟 0x401d80；模拟表与 alice、davis 两组运行时 dump 逐字节一致（`E-006-table-verify-*.txt`）。
  - `reimpl/keygen.py` 生成 16 字节序列号；两组都由原版接受。
- 用例：TC1、TC2 accepted（退出码 0，打印 flag）；TC3–TC5 denied（退出码 1）。证据 `E-005-five-cases.json`。另有五个纯无效输入用例全部 denied（`E-003-invalid-inputs.json`）。
- 判定：用户本轮口径**通过**；R46 L4 部分通过（哈希用机器码模拟，不是独立重写）；L5 未声明。详见 `cases/sample-2/ACCEPTANCE.md`。

## 3. 第三个项目（Seep）

未签出、未安装、未抽取。样本 1 没有许可证校验或加壳；样本 2 没有加壳/反调试标签。按 v2.1 §1.4，两者都不需要 Seep。记为「以后再说」，不影响本阶段结论。

## 4. 未做与未核实

- 样本 3 未执行。
- 样本 1：未做动态调试或内存观察；调试 CRT 四个 DLL 的哈希未记录。
- 样本 2：提示字符串的混淆方式未逐条还原；哈希未用高级语言重写；未做动态内存观察（除 gdb 断点 dump 表）。
- 两例都未声明 L5；检查器 `check_handoff.py` 只在自带示例上跑过（结果 FAIL：示例引用的文件缺失），没有为本轮交接单生成 JSON 指针清单。

## 5. 复现命令

```bash
# 样本 1
python -I cases/sample-1/reimpl/differential_test.py D:/tmp/fusion-samples/s1/CrackMe.exe cases/sample-1/evidence/E-006-differential.json
python -I cases/sample-1/reimpl/boundary_test.py D:/tmp/fusion-samples/s1/CrackMe.exe cases/sample-1/evidence/E-008-boundary.json
python -I cases/sample-1/reimpl/comparator_check.py D:/tmp/fusion-samples/s1/CrackMe.exe cases/sample-1/evidence/E-007-comparator-selfcheck.json

# 样本 2
python -I cases/sample-2/reimpl/keygen.py D:/tmp/fusion-samples/s2/howo-not-to-simple-keygen alice bob@example.com
python -I cases/sample-2/reimpl/run_cases.py D:/tmp/fusion-samples/s2/howo-not-to-simple-keygen D:/tmp/s2cases.json cases/sample-2/evidence/E-005-five-cases.json
python -I cases/sample-2/reimpl/verify_table.py D:/tmp/fusion-samples/s2/howo-not-to-simple-keygen cases/sample-2/evidence/E-004-table-alice.bin alice bob@example.com
```
