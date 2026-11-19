# timeline.md — cases/apk-1

- 2026-11-20 05:2x 核实 APK 工具链：jadx 1.5.6、apktool 3.0.3、adb 1.0.41、aapt（build-tools 34.0.0）、frida 17.17.0 均可用。
- 05:3x 建 AVD `ftest`（system-images;android-29;google_apis;x86_64），启动模拟器，`emulator-5554` device，`boot_completed=1`。
- 05:3x 自建学习目标 `com.example.licdemo`：写 MainActivity（license 校验），javac + android.jar 编译出 class（构造 AAPT2 资源编不过，最后用纯 java class 方案）。
- 05:4x `d8`（R8 8.2.2）转 dex **两次失败**（JDK21、JDK25 均 `NullPointerException: String.length()`）——改为类级对照。
- 05:4x jadx 反编译 `MainActivity.class` → `validate()` 语义提取。
- 05:5x Node 复现 `licensecheck.mjs`；JVM 跑原版 5 用例、Node 跑同 5 用例 → all_match=true。
- 05:5x 比较器自检（改 0xD0→0xD1 后合法序列号变 false）通过。
- 结论：算法抽取**部分通过**（APK 未做成 dex、UI 未实测；核心算法对照全对）。