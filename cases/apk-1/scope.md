# scope.md — cases/apk-1

**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过 / 部分通过 / 不通过」，不适用 L4/L5。**

- 目标：一个带序列号校验的 Android 学习目标（license validation 算法），用 jadx 反编译定位校验函数，Node 本地复现，5 用例与「原版」双侧对照。
- 类型：Android (Java) / license check 算法
- 原版定义：本机用 javac + android.jar 编译的 `MainActivity.class`，其在 JVM 上跑的 `validate()` 就是「原版语义」；jadx 反编译同 class 得到可读伪码。**未做成 dex/APK**（d8 工具在两个 JDK 下崩溃，见 timeline；真机/模拟器安装受阻，改用 class 级对照）。
- 要做：jadx 定位校验算法 → Node 复现 → 5 用例 JVM vs Node 双侧对照 → 比较器自检（改常量）。
- 不做：不做整套 APK 重打包；不写 L4/L5；不声称在模拟器 UI 里点过按钮。
- 验收：TC1/TC2 正常（合法序列号）、TC3 边界（短串）、TC4 无效（错 sum）、TC5 篡改（改校验常量）→ 输出必须变。

## 测试集（事先写明）

| 用例 | 输入 | 预期原版 | 预期复现 |
|---|---|---|---|
| TC1 正常 | `FUSION-2026-Xs` | true | true |
| TC2 正常 | `FUSION-2026-é` | （按算法实际，不预设） | 一致 |
| TC3 边界 | `abc`（<4 长度） | false | false |
| TC4 无效 | `FUSION-2026-OO`（错 sum） | false | false |
| TC5 篡改 | `XXXXX`（前缀错） | false | false |

比较器自检：把校验常量 `0xD0→0xD1`，合法序列号必须变 false（防背答案）。