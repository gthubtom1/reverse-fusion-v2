# unknowns.md — cases/apk-1

- **未做成 dex/APK**：`d8`（R8 8.2.2，build-tools 34.0.0）在 JDK21 和 JDK25 下均崩溃（`NullPointerException: String.length()`，`CIRCULAR REFERENCE`）。原因未核实（可能是 R8 对 JDK21+ 生成的 classfile 的兼容 bug，或本机 d8 环境问题）。因此没有真实 APK 安装到模拟器。
- **UI/活动层未实测**：`onClick` 显示 "valid/invalid license" 的界面路径未在模拟器验证；只验证了核心 `validate()` 静态逻辑（JVM 真跑 + Node 对照）。
- java 在中文路径（`D:/Project/最终版聚合`）下用 `-cp` 会 ClassNotFound；需要先复制到纯 ASCII 路径（`/d/tmp/...`）再跑。这是 Windows + 中文目录的环境限制，已规避。
- 样本是**自建学习目标**（非第三方 APK）：这符合 v3 §6.3「公开学习用」的精神但严格说是自有样本。真实第三方 APK（如 OWASP 或 Git 上 crackme）的下载链路在本机经 Clash 代理不稳定，未成功取得稳定官方 APK；后续可在网络稳定的会话重试。
- 只验证了 license 校验算法；未覆盖 Android 的签名校验、资源混淆、代码混淆、native .so 等更复杂面。
- adb/frida 连模拟器可用，但未实际执行 frida hook（本案例走的是静态 + JVM 对照，没用到 frida 动态）。