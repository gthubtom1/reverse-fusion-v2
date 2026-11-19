# 时间线：样本 2

- 2026-11-20 04:1x 建案子；样本 SHA-256 `8b685085320c61337679f34eedc5aa338b5cc38c782ab5034581f33ae6c08804`，与登记一致。
- 2026-11-20 04:2x REA 的 `open_binary` 成功，但 `binary_overview` / `list_procedures` 返回 `provider_unavailable`：Windows 版 Ghidra P0 只接受 PE/MZ，不支持 ELF。证据 `evidence/E-002-overview.json`。这属于已知平台限制，不停止，改用第二个项目的 Ghidra 入口做静态分析。
- 2026-11-20 04:22 用 Ghidra 12.2 无头模式导入 ELF，第一次脚本编译失败（`DataIterator` 导入错误），修正后成功；按字符串引用转储 20 个函数，但程序提示字符串不在明文中，说明有字符串混淆。
- 2026-11-20 04:23 本机没有 WSL/Docker/qemu；安装 QEMU 11.1.0，下载 Alpine 6.18.60 virt 内核与静态 busybox，自制 initramfs。
- 2026-11-20 04:2x 第一次 initramfs 启动 `No working init found`；补 `dev/console`、`dev/null` 和 `bin`、`dev` 目录项后 init 正常。
- 2026-11-20 04:3x 原版在 QEMU 中真跑：依次提示 `Please insert your full name:`、`Please insert your best email:`、`Please insert your serial:`；输入不完整时打印 `POLICE, THIS GUY IS A ROBBER BUT HE DON'T HAVE A VALID SERIAL KEY LOL!`，退出码 1。
- 2026-11-20 04:3x 五个纯无效输入用例全部 denied（`evidence/E-003-invalid-inputs.json`）。
- 2026-11-20 04:3x 用 gdb 连接 QEMU gdbstub，断在 0x4019f2，从 `rbx` dump 256 字节表；确认 `table[9]=0xfb`（有符号 -5）可用。用 `ABCDEFGHIJKLM\xECNOP` 让原版接受，得到 flag。证据 `E-004-gdb-dump.txt`、`E-004-table-alice.bin`。
- 2026-11-20 04:4x Ghidra 反编译 0x401d80 的哈希函数，用 Unicorn 模拟；模拟表与 alice、davis 两组运行时表逐字节一致（`E-006-table-verify-*.txt`）。
- 2026-11-20 04:5x `reimpl/keygen.py` 生成两组序列号，原版 TC1、TC2 接受；TC3–TC5 denied。五用例证据 `E-005-five-cases.json`，结论见 `ACCEPTANCE.md`。
