# 时间线：样本 1

- 2026-11-20 04:0x 建案子，写 `scope.md`；样本路径 `D:/tmp/fusion-samples/s1/CrackMe.exe`，SHA-256 `945e81e113e09002db42b26f69cd43de564c32a03971fdf335e2f81caca6c67a`（与 `cases/samples/MANIFEST.md` 一致）。
- 2026-11-20 04:09 第一次接线测试：`open_binary` 成功；`binary_overview` 返回 `provider_unavailable`。原因：Ghidra 12.1.3 低于 REA 要求的 12.2；REA 的 Windows 原生模块 `native/windows/build/` 缺失。证据：`evidence/wiring-transcript.json` 第一次运行。
- 2026-11-20 04:10 从 `rea-agents@6.9.0` npm 包取出 `manifest.json`、`rea-windows-x64.node` 放入 `engine/rea/native/windows/build/`；`rea doctor` 的 `ghidra-java` 转为 healthy。
- 2026-11-20 04:14 下载并解压 Ghidra 12.2 到 `D:/Tools/Ghidra-12.2/ghidra_12.2_PUBLIC`；Ghidra 12.2 要求 JDK 25，另装 Temurin JDK 25 到 `D:/Tools/jdk25`。
- 2026-11-20 04:1x 第二次接线测试（带 `GHIDRA_INSTALL_DIR`、`JAVA_HOME`）：结果见 `evidence/wiring-transcript.json` 与下方记录。
