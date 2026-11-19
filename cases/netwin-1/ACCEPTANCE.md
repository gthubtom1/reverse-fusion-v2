# 验收报告：cases/netwin-1（Stage 13）

**R6 复用检查：工具单查询——REA 验证链已有（compare_functions 等）；.NET 校验自建（licensecheck 一次性）；比较器自检统一引共享，不再重写。**


**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过」。不适用 L4/L5。**

## 结论（两行分写）
- 第一行：**算法抽取：通过**。
- 第二行：R46 L4：不适用（模式 3）；L5：不适用。

## 做了什么
- 自建 .NET console 程序（`target/Program.cs`），dotnet 8.0 编译出 `build.exe`。
- 静态定位 `ValidateSerial` 规则（见 handoff），Python 独立复现（`reimpl/licensecheck.py`）。
- 双侧对照：5 用例原版 exe vs 复现，`ALL_MATCH True`（TC1 VALID、TC2-5 INVALID）。
- 比较器自检（`comparator_check.py`）：改 `0x2F→0x2E` 后合法序列号 `AAA-AAA-AAA|` 由 VALID 变 INVALID；无效输入保持 INVALID（语义）。`ok=True`。

## 未验证
- 未用真实第三方 .NET 程序（自建学习目标）；未做厚客户端 GUI 全链路。
- 未做脱壳/混淆（.NET 混淆器 ConfuserEx 等）。
- 未走 R46 规格链（模式 3 不需要新 specs）。

## 结论
**算法抽取：通过**。5 用例双侧全一致、独立复现、防背答案自检通过。
