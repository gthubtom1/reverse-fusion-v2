# 复刻交接单 — .NET 序列号校验算法（netwin-1）

target: 自建 .NET 序列号校验（学习目标）
source: cases/netwin-1/target/Program.cs（反编译/静态分析）、reimpl/ 对照
case: cases/netwin-1
模式: 算法抽取（模式 3）

## 抽的是哪一段算法
- `Program.ValidateSerial(string)`：长度 12、`s[3]=='-' && s[7]=='-'`、跳过破折号后 `Σ(s[i] ^ (i*7)) % 256 == 0x2F`。
- 复现：`reimpl/licensecheck.py`（validate()）。原版：编译的 `build.exe`（真跑）。

## 测试用例（5 条，双侧对照全过 -> ALL_MATCH True）
TC1 `AAA-AAA-AAA|` VALID；TC2 `BBB-BBB-BBB|` INVALID；TC3 `abc` INVALID；TC4 破折号错位 INVALID；TC5 `AAA-AAA-AAAZ` INVALID。

## 未知清单
见 unknowns.md。
