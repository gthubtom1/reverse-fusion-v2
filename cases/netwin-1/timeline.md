# timeline.md — cases/netwin-1

- 2026-11-20 07:0x 建自建 .NET 目标，dotnet 编译 build.exe 成功。
- 07:0x 找合法序列号（`AAA-AAA-AAA|`），原版 subprocess 精确测 VALID。
- 07:0x 写 Python 复现 + 5 用例双侧对照 → ALL_MATCH True。
- 07:0x 比较器自检（改 0x2F→0x2E 合法号变 INVALID）→ ok=True。
- 结论：算法抽取**通过**。
