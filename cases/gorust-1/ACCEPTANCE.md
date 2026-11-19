# 验收报告：cases/gorust-1（Stage 14）

**R6 复用检查：工具单查询——REA 对 Go ELF 在 Windows 不支持（platform 限制）；Go 校验自建（check.go）；比较器自检统一引共享，不再重写。**


**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过」。不适用 L4/L5。**

- 第一行：**算法抽取：通过**。
- 第二行：R46 L4/L5：不适用（模式 3）。

- 做了什么：自建 Go 程序（main.go）→ 编译 gorust.exe；静态定位校验（16 hex、前15异或=末字节）；Go 复现（reimpl/check.go）。
- 双侧对照：6 用例原版 exe vs 复现 `ALL_MATCH true`（TC1/TC5 VALID，TC2/3/4 INVALID）。
- 防背答案：原版与复现都依赖真实校验逻辑，非法字符返回 0xFF 导致 15 异或≠末字节（如 TC4）；逻辑是参数化而非背答案。
- 未验证：自建 Go（非真实二进制）；未测 Rust（工具链未装）；未测剥离符号/混淆。
