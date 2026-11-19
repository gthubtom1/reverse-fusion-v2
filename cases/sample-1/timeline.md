# 时间线：样本 1

- 2026-11-20 04:0x 建案子，写 `scope.md`；样本路径 `D:/tmp/fusion-samples/s1/CrackMe.exe`，SHA-256 `945e81e113e09002db42b26f69cd43de564c32a03971fdf335e2f81caca6c67a`（与 `cases/samples/MANIFEST.md` 一致）。
- 2026-11-20 04:09 第一次接线测试：`open_binary` 成功；`binary_overview` 返回 `provider_unavailable`。原因：Ghidra 12.1.3 低于 REA 要求的 12.2；REA 的 Windows 原生模块 `native/windows/build/` 缺失。证据：`evidence/wiring-transcript.json` 第一次运行。
- 2026-11-20 04:10 从 `rea-agents@6.9.0` npm 包取出 `manifest.json`、`rea-windows-x64.node` 放入 `engine/rea/native/windows/build/`；`rea doctor` 的 `ghidra-java` 转为 healthy。
- 2026-11-20 04:14 下载并解压 Ghidra 12.2 到 `D:/Tools/Ghidra-12.2/ghidra_12.2_PUBLIC`；Ghidra 12.2 要求 JDK 25，另装 Temurin JDK 25 到 `D:/Tools/jdk25`。
- 2026-11-20 04:17 第二次接线测试（带 `GHIDRA_INSTALL_DIR`、`JAVA_HOME`）：`binary_overview` 成功，证据 ID `ev_646685c7…`；证据包落盘。见 `evidence/wiring-transcript.json`。
- 2026-11-20 04:2x `list_procedures`：701 个函数（`evidence/E-002-procedures.json`，证据 ID `ev_e4bd46c8…`）。`invoke_main` → `FUN_140017cd0`（main）→ `FUN_1400173d0`（校验）。
- 2026-11-20 04:2x 反编译：校验逻辑为 `strlen==6` 且 `input[i] == [0x38,0x27,0x64,0x66,0x66,0x62][i] ^ 0x55`，得密码 `mr1337`。证据 `E-004`、`E-005`。
- 2026-11-20 04:3x 原版依赖调试版 CRT，本机缺 `ucrtbased.dll` 等四个 DLL。安装 VS Build Tools（含 VC 调试运行库）与 Windows SDK 10.0.26100（含 `ucrtbased.dll`），把四个 DLL 放到样本目录后原版可运行。
- 2026-11-20 04:3x 五个核心用例：5/5 一致（`E-006`）。六个边界用例第一轮 B3、B6 不一致，原因是 `cin >>` 的空白分词；补上分词后 6/6 一致（`E-008`）。
- 2026-11-20 04:4x 故意把异或键改成 `0x54` 的坏变体被比较器发现（`E-007`）。验收结论：L4 通过，L5 未声明通过（副作用未复刻）。见 `ACCEPTANCE.md`。
