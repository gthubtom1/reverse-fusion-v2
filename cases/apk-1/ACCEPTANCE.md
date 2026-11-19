# 验收报告：cases/apk-1（Stage 6）

**R6 复用检查：工具单查询（REA 260 工具）——验证链有 compare_functions/export_evidence_bundle（R3 已用），序列号校验类自建（licensecheck 一次性）；比较器自检统一引 cases/_shared/comparator_check/compare.py（改常量防背答案），不再重写。**


**本案模式是 算法抽取（模式 3），验收词是「算法抽取：部分通过」。不适用 L4/L5（本模式不要求）。**

## 0. 结论（两行分写）
- 第一行（本模式结论）：**算法抽取：部分通过**。
- 第二行（R46 结论）：R46 L4：不适用（模式 3）；L5：不适用。

## 1. 做了什么

- 建 Android 10 模拟器（AVD `ftest`，`android-29;google_apis;x86_64`，WHPX 加速），`emulator-5554` 启动、`sys.boot_completed=1`。
- 工具链核实：jadx 1.5.6、apktool 3.0.3、adb 1.0.41、aapt (build-tools 34.0.0)、frida 17.17.0 均可用。
- 目标：自建学习目标 `com.example.licdemo`（带 license 校验，语义简单明确），javac + android.jar 编译出 `MainActivity.class`。
- 定位：jadx 1.5.6 反编译 class → `validate()` 语义提取（evidence/`target/jadx-out`）。
- 复现：Node 独立实现 `licensecheck.mjs`；比较器自检 `comparator_check.mjs`。

## 2. 双侧对照（原版 JVM vs Node 复现，5 用例）

evidence/E-002-differential.json，`all_match=true`：

| 用例 | 输入 | 原版 | 复现 | 一致 |
|---|---|---|---|---|
| TC1 正常 | `FUSION-2026-Xs` | true | true | ✅ |
| TC2 正常 | `FUSION-2026-é` | false | false | ✅ |
| TC3 边界 | `abc` | false | false | ✅ |
| TC4 无效 | `FUSION-2026-OO` | false | false | ✅ |
| TC5 篡改 | `XXXXX` | false | false | ✅ |

## 3. 独立运行 + 不依赖原文件

- Node 复现可独立执行（`node reimpl/licensecheck.mjs`），不读 class、不读反编译产物。
- TC5 篡改：把校验目标从 `0xD0` 改成 `0xD1`（`comparator_check.mjs`），合法序列号 `FUSION-2026-Xs` 从 true 变 false → **防背答案自检通过**。

## 4. 卡点（如实记录，非失败结论）

- **未做成 dex/APK**：`d8`（build-tools 34.0.0，`R8 8.2.2`）在 JDK21 与 JDK25 下对同一批 class 都报 `NullPointerException (String.length())`（R8 崩溃，`CIRCULAR REFERENCE`）。这是本机工具 bug，按 v3 §9.3「备用梯」走类级对照：不把「dex 打包失败」当成流程失败，用 `MainActivity.class` + JVM 完成原版功能对照。
- 因此：没有在 Android 模拟器里实际安装并点击 APK；UI 层验证（`onClick` 显示 "valid/invalid license"）**未实测**，只验证了核心 `validate()` 逻辑。
- 该卡点记为开放事项「以后再说」：若后续需要真机 APK 安装验证，需装一个能跑的 d8/dx 或换 Gradle 构建。

## 5. 未验证 / 未知

见 `unknowns.md`。

## 结论

**算法抽取：部分通过**——核心 `validate()` 算法 5 用例双侧全对、独立运行、比较器自检通过；但「APK 安装到模拟器并 UI 真跑」未做（d8 工具受阻），故不评为「通过」。未宣称 L4/L5。