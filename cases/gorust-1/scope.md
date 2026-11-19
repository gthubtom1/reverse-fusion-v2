# scope.md — cases/gorust-1（Stage 14：Go/Rust）

**第一行（C4）：模式 3 算法抽取；第一个工具：REA `open_binary`（PE/mach-o 先试）→ go toolchain 静态分析（自建 Go 程序）。**

- 目标：自建 Go 序列号校验程序，静态定位规则、本地复现、多用例双侧对照。
- 类型：Go（编译原生 exe）/ 序列号校验算法（模式 3）
- 验收：与原版 exe 双侧一致 + 防背答案自检。

## 测试集
TC1 `0123456789abcdef` VALID；TC2 `0123456789abcdea` INVALID；TC3 `abc` INVALID；TC4 `0123456789abcdefx`（16位含非法）INVALID；TC5 `ffffffffffffffff` VALID。
