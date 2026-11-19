# 复刻交接单 — 验证码答案 token 算法（captcha-1）

target: 自建学习验证码的答案推导 token 算法
source: evidence E-000（样例哈希）、E-002（对照 JSON）、E-003（dsl-vm 笔记引用）
case: cases/captcha-1
模式: 算法抽取（模式 3），不适用 L4/L5

## 抽的是哪一段算法

- `compute(a, op, b)`：按运算符做算术（+ - * %）。
- `token(a, op, b)`：`h = (ans*2654435761 ^ a*40503 ^ b*73) >>> 0`，hex 8 位。
- 定位：Canvas 验证码的答案即 token；页面 `check` 用 `token(8,'+',5)===input` 判断。
- 方法沿用上游 DSL-VM 笔记的「常量表 + 函数追踪」：T 表是常量、compute/token 是函数体、2543… 是折叠常数。

## 复现

- `reimpl/captcharepro.mjs`（独立 Node），`reimpl/comparator_check.mjs`（改 40503→40504 防背答案）。

## 测试用例（见 evidence/E-002-differential.json，双侧对照全过）

| 用例 | 表达式 | 原版答案/token | 复现 | 一致 |
|---|---|---|---|---|
| TC1 | `8+5` | 13 / `08d5dd28` | 相同 | ✅ |
| TC2 | `3*7` | 21 / `fa8d20df` | 相同 | ✅ |
| TC3 | `10-4` | 6 / `b54af524` | 相同 | ✅ |
| TC4 | `7%3` | 1 / `9e332aeb` | 相同 | ✅ |
| TC5 | `0+0` | 0 / `00000000` | 相同 | ✅ |

## 未知清单

见 `unknowns.md`。