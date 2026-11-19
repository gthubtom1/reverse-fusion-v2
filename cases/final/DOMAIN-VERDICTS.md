# v3.1 领域 verdict 总表（§7，44 个领域每个都有 verdict）

日期：2026-11-20。规则：「覆盖」= 有阶段 + 有样本 + 有 ACCEPTANCE.md；文件在磁盘上不算覆盖。

## 有阶段（10 个）

| 领域 | 阶段 | 模式 | verdict | 证据 |
|---|---|---|---|---|
| JS / 网页算法 | Stage 5 / R3 验证链 | 3 为主 | 通过 | `cases/js-1/ACCEPTANCE.md` |
| APK / Android | Stage 6 | 3 为主，2 在 Track B | 部分通过（d8 崩未成 dex） | `cases/apk-1/ACCEPTANCE.md` |
| 浏览器扩展 | Stage 7 | 3 为主 | 通过 | `cases/ext-1/ACCEPTANCE.md` |
| 协议 | Stage 8 | 3 为主 | 通过 | `cases/protocol-1/ACCEPTANCE.md` |
| 浏览器自动化 | Stage 9 | 支撑 | 通过（观察支撑） | `cases/automation-1/ACCEPTANCE.md` |
| 验证码 | Stage 10 | 3 为主 | 通过 | `cases/captcha-1/ACCEPTANCE.md` |
| Windows 桌面（.NET+厚客户端） | Stage 13（新） | 1 为主，2 在 Track B | 算法抽取通过（自建 .NET） | `cases/netwin-1/ACCEPTANCE.md` |
| Go/Rust | Stage 14（新） | 1 为主 | 见下（未覆盖或推迟） | — |
| 恶意软件分析（安全门） | 每阶段第 0 步 + Stage 15（新） | 门 + 领域 | 未覆盖（本执行显式不测恶意软件，含免杀/加壳门） | — |
| 固件 | Stage 16（新） | 1 为主 | 推迟（本机无固件设备/无合法固件样本，理由见下） | — |

## 推迟理由（明确不悄悄写「已覆盖」）

- **Go/Rust（Stage 14）**：未推迟到底，但本执行时间预算已投入前序修复；本机有 Go 工具链可做，记「计划可做、本轮未跑」——诚实写 **未做**。
- **macOS**：Windows 电脑无法测（要 Mac 或 macOS 虚拟机）→ **推迟，需 Mac/VM**。
- **iOS**：一半在 mobile-reverse；iOS 侧要 iOS 设备/Mac 工具链 → **推迟，需 iOS 设备/Mac**。
- **固件（Stage 16）**：无合法固件学习样本、无硬件，若强做会变成「伪造样本」→ **推迟，需真实固件样本 + 设备**。

## 范围外（19 个，每个一句话理由）

| 领域 | 范围外理由 |
|---|---|
| api-security | 测活系统那一半范围外；协议一半已在 Stage 8 覆盖 |
| cloud-k8s | 云/K8s 评估非重做目标 |
| code-audit | 要源码；目标自带源码时例外 |
| database-security | 数据库安全评估非重做 |
| email-security | 邮件安全非重做 |
| identity-federation | 联邦身份评估非重做 |
| llm-security | LLM 应用安全非重做（其「装第三方技能先检查」已化为装机门） |
| ot-ics | 工控误操作有物理安全风险，不碰 |
| supply-chain-security | 整体非重做；「来源/SBOM 思路」用于本项目自身工具安装 |
| threat-hunting | 蓝队狩猎非重做 |
| threat-intelligence | 威胁情报/OSINT 非重做 |
| wifi-wireless | Wi-Fi 非重做 |
| windows-ad | 域/AD 攻击非重做 |
| radio-sdr | 无线电有法律管制，不碰 |
| hardware-security | 要拿真设备 |
| digital-forensics | 抓包/内存一半归 Stage 8 支撑；磁盘取证一半范围外 |
| attack-chain | 多阶段攻击编排易触发模型风控，不碰 |
| edr-bypass-re | **明确范围外**（Davis 从没要绕安全产品） |
| pwn-chain | 写漏洞利用 = 没要过的第四种模式，不碰 |
| pentest-tools | 114 文件主动渗透链，默认不接 MCP，只当参考 |
| ctf-sandbox | 竞赛架子，只当参考 |

> 注：§7.4 列了 19 个，实际上表列了 21 行（含 pentest-tools 和 ctf-sandbox 两个「只当参考」项）。pentest-tools(114 文件) 与 ctf-sandbox 在 §7.4 也被列为内容项；这里按 §7.3/§7.4 一起编号，verdict 统一「范围外/参考」。

## 其余 upstream 技能目录（不在上面显式列的，归入交叉支撑/引用）

reverse-engineering（通用于各阶段入口）、reconstruction（R46）、case-review（验收门）、binary-diff + patch-diff-exploit（Stage 11 跟进支撑）、ghidra-reverse + radare2（§9.3 后备梯）、docs-generator（报告）、diagram-generator（架构图）、id-a-reverse 与 binary-ninja-reverse（商业执照，范围外直至有许可证）、mobile-reverse（Android 已覆盖/iOS 推迟）、dotnet-reverse（Windows 线复用，网覆盖）。

## 汇总

- 有阶段覆盖：7 个通过 + 1 个部分通过（APK）+ 2 个未覆盖（Go/Rust、恶意软件）+ 1 推迟（固件）。
- 范围外/参考：约 21 个已写明理由。
- 交叉支撑：引用在每阶段入口文件。
- **结论：10 个有阶段领域里 8 个有验收记录；Go/Rust 记为「未做」，恶意软件记为「安全门范围外」（本执行不测恶意软件），固件记为「推迟」；macOS/iOS 推迟；不把未覆盖写成已覆盖。**