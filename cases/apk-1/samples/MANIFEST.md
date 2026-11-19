# Stage 6 APK 样本登记

日期：2026-11-20。

| 编号 | 样本 | 难度 | 来源 | 为什么代表这个领域 |
|---|---|---|---|---|
| apk-1-simple | `com.example.licdemo`（自建学习目标） | 简单 | 本仓库 `cases/apk-1/src/`（javac + android.jar 编译的 `MainActivity.class`）| 单函数 license 校验（XOR-sum + 前缀 + 长度），代表「APK 里定位关键算法」的轻量场景 |

## SHA-256

```bash
sha256sum cases/apk-1/target/MainActivity.class cases/apk-1/../../cases/apk-1/src/app/src/main/java/com/example/licdemo/MainActivity.java
```

（记录在 evidence/E-000。）

## 说明

- 严格说是**自建学习目标**（非第三方 APK）。v3 §6.3 允许「公开学习用」+ 不以真实商业软件为样本；本机经 Clash 代理获取 OWASP/Git 开源 crackme APK 不稳定，未取到可下载的官方 APK 前，先用自建样本走通 Stage 6 全流程；后续可换第三方样本重跑。
- 原版侧用「JVM 直接跑 `MainActivity.class`」作为可复现语义；未做成 dex（d8 工具受阻，见 unknowns）。