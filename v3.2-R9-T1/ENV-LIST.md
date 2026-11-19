# 环境清单（R9 T1 快照，Pi 对照用）

- OS: Windows 10 Enterprise 10.0.19045（x64）
- Node: 24.22.1（`D:\Tools\node-24.22.1\node-v24.22.1-win-x64\node.exe`）
- Python: 3.12.0
- Git: 2.55.0
- Ghidra: 12.2（`D:\Tools\Ghidra-12.2\ghidra_12.2_PUBLIC`）
- JDK: Temurin 25（`D:\Tools\jdk25`）
- QEMU: 11.1.0（`C:\Program Files\qemu\qemu-system-x86_64.exe`）
- jadx 1.5.6 / apktool 3.0.3 / adb 1.0.41 / frida 17.17.0
- tshark: 4.6.8（`D:\Tools\Wireshark\`）
- Go: 本地 go toolchain（/d/Tools/runtime/go）
- REA MCP: 经 `.mcp.json`（同步脚本生成；rea 单服务器，cwd=共享文件夹，env 注入 GHIDRA/JAVA_HOME）
- .mcp.json 模板: `.mcp.json.template`；`fusion-home.yaml` 在 `%USERPROFILE%/.fusion/`（shared_folder/node_exe/ghidra/java_home）
