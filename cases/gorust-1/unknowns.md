# unknowns.md — cases/gorust-1

- 样本是自建 Go 程序（学习目标）；未覆盖真实 Go 剥离符号/静态链接、CGO、混淆。
- Rust 未测（本机无 Rust 目标编译；`go-rust-reverse` 技能要求 Rust 工具链，未装）。
- 未做 REA 对 Go ELF 的分析（Windows Ghidra 不支持 ELF，platform 限制同样本 2）。
