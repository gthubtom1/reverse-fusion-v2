# scope.md — cases/netwin-1（Stage 13：Windows + .NET + 厚客户端）

**第一行（C4）：模式 3 算法抽取；第一个工具：REA `open_binary`（PE）→ dnSpyEx/dotnet 反编译（自建 .NET 程序）。**

- 目标：自建 .NET console 程序（含序列号校验）的校验算法，反编译定位、本地复现、5 用例双侧对照。
- 类型：.NET (C#) / 序列号校验算法（学习目标，模式 3）
- 要做：dotnet 编译 → 反编译定位 ValidateSerial → Python 复现 → 5 用例 vs 原版 exe 对照 → 比较器自检。
- 不做：不做厚客户端 GUI 逆向、不写 L4/L5。
- 验收：5 用例双侧一致 + 比较器自检通过。

## 测试集
| 用例 | 输入 | 预期原版 | 预期复现 |
|---|---|---|---|
| TC1 正常 | `AAA-AAA-AAA\|` | VALID | VALID |
| TC2 正常 | `BBB-BBB-BBB\|` | INVALID | INVALID |
| TC3 边界 | `abc`（短） | INVALID | INVALID |
| TC4 边界 | `ABCD-EFG-HIJK`（破折号错位） | INVALID | INVALID |
| TC5 无效 | `AAA-AAA-AAAZ`（sum 错） | INVALID | INVALID |

常量 `0x2F` 改 `0x2E` 后合法序列号必须变 INVALID（防背答案）。
