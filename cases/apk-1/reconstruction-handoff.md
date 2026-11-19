# 复刻交接单 — APK license 校验算法（com.example.licdemo）

target: Android license check 算法（自建学习目标）
source: evidence E-001（jadx 反编译）、E-002（对照 JSON）
case: cases/apk-1
模式: 算法抽取（模式 3），不适用 L4/L5

## 抽的是哪一段算法

- 目标函数：`MainActivity.validate(String)`
- 反编译定位（jadx 1.5.6 反编译 `MainActivity.class`，见 `target/jadx-out/sources/.../MainActivity.java`）：
  - 长度 < 4 → false
  - `sum = Σ(char[i] ^ KEY[i%6])`
  - 接受条件：`(sum & 0xFF) == 0xD0 && serial.startsWith("FUSION")`
  - KEY = [0x46,0x55,0x53,0x49,0x4f,0x4e]（"FUSION" ASCII）

## 复现

- `reimpl/licensecheck.mjs`：独立 Node 复现，不加载 class、不 eval 反编译代码。
- `reimpl/comparator_check.mjs`：改 0xD0→0xD1 后合法序列号必须变 false。

## 测试用例（双侧对照 5 条，见 evidence/E-002-differential.json）

| 用例 | 输入 | 原版(JVM) | 复现(Node) | 一致 |
|---|---|---|---|---|
| TC1 | `FUSION-2026-Xs` | true | true | ✅ |
| TC2 | `FUSION-2026-é` | false | false | ✅ |
| TC3 | `abc` | false | false | ✅ |
| TC4 | `FUSION-2026-OO` | false | false | ✅ |
| TC5 | `XXXXX` | false | false | ✅ |

## 未知清单

见 `unknowns.md`。