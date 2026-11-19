# 锁定上游 44 个技能目录的审计状态

键来自 `ce675096e6a2cd4789a76f9bd618feddc2b6f333` 的 `skills/*/SKILL.md`。历史样本只说明对应记录存在。独立验收见 [验收单](THIRD-PARTY-ACCEPTANCE.md)。

| 上游目录 | 状态 | 依据 |
|---|---|---|
| [`api-security`](../../core/skills/api-security/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`apk-reverse`](../../core/skills/apk-reverse/SKILL.md) | 历史部分通过 | JVM/Node 对照有记录，dex 与设备未验。 [案例验收](../apk-1/ACCEPTANCE.md) |
| [`attack-chain`](../../core/skills/attack-chain/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`binary-diff`](../../core/skills/binary-diff/SKILL.md) | 参考/支撑 | 未见单独领域验收。 |
| [`binary-ninja-reverse`](../../core/skills/binary-ninja-reverse/SKILL.md) | 待验 | 未见对应工具许可与回执。 |
| [`browser-automation`](../../core/skills/browser-automation/SKILL.md) | 历史观察支撑 | 本地页面观察。 [案例验收](../automation-1/ACCEPTANCE.md) |
| [`browser-extension-reverse`](../../core/skills/browser-extension-reverse/SKILL.md) | 历史部分通过 | 本地对照有记录。浏览器安装未验。 [案例验收](../ext-1/ACCEPTANCE.md) |
| [`case-review`](../../core/skills/case-review/SKILL.md) | 参考/支撑 | 未见单独领域验收。 |
| [`cloud-k8s`](../../core/skills/cloud-k8s/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`code-audit`](../../core/skills/code-audit/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`ctf-sandbox`](../../core/skills/ctf-sandbox/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`database-security`](../../core/skills/database-security/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`diagram-generator`](../../core/skills/diagram-generator/SKILL.md) | 参考/支撑 | 未见单独领域验收。 |
| [`digital-forensics`](../../core/skills/digital-forensics/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`docs-generator`](../../core/skills/docs-generator/SKILL.md) | 参考/支撑 | 未见单独领域验收。 |
| [`dotnet-reverse`](../../core/skills/dotnet-reverse/SKILL.md) | 历史样本 | 自建 .NET 算法对照。 [案例验收](../netwin-1/ACCEPTANCE.md) |
| [`edr-bypass-re`](../../core/skills/edr-bypass-re/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`email-security`](../../core/skills/email-security/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`firmware-pentest`](../../core/skills/firmware-pentest/SKILL.md) | 待验 | 无设备和样本验收。 |
| [`ghidra-reverse`](../../core/skills/ghidra-reverse/SKILL.md) | 历史支撑 | Ghidra 无头用于历史样本。 [案例验收](../sample-2/ACCEPTANCE.md) |
| [`go-rust-reverse`](../../core/skills/go-rust-reverse/SKILL.md) | Go 有历史样本，Rust 未验 | 自建 Go 对照 6 用例。Rust 无结果。 [案例验收](../gorust-1/ACCEPTANCE.md) |
| [`hardware-security`](../../core/skills/hardware-security/SKILL.md) | 待验 | 无硬件环境验收。 |
| [`ida-reverse`](../../core/skills/ida-reverse/SKILL.md) | 待验 | 无本轮工具运行回执。 |
| [`identity-federation`](../../core/skills/identity-federation/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`js-reverse`](../../core/skills/js-reverse/SKILL.md) | 历史样本 | Node 双侧记录。专用 MCP 未见运行回执。 [案例验收](../js-1/ACCEPTANCE.md) |
| [`llm-security`](../../core/skills/llm-security/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`macos-reverse`](../../core/skills/macos-reverse/SKILL.md) | 待验 | 无 macOS 主机或验收。 |
| [`malware-analysis`](../../core/skills/malware-analysis/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`mobile-reverse`](../../core/skills/mobile-reverse/SKILL.md) | Android 历史部分覆盖，iOS 未验 | iOS 缺设备与验收。 [案例验收](../apk-1/ACCEPTANCE.md) |
| [`ot-ics`](../../core/skills/ot-ics/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`patch-diff-exploit`](../../core/skills/patch-diff-exploit/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`pentest-tools`](../../core/skills/pentest-tools/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`protocol-reverse`](../../core/skills/protocol-reverse/SKILL.md) | 历史样本 | 本机 loopback 样本。 [案例验收](../protocol-1/ACCEPTANCE.md) |
| [`pwn-chain`](../../core/skills/pwn-chain/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`radare2`](../../core/skills/radare2/SKILL.md) | 参考/支撑 | 未见单独领域验收。 |
| [`radio-sdr`](../../core/skills/radio-sdr/SKILL.md) | 待验 | 无射频设备与验收。 |
| [`reconstruction`](../../core/skills/reconstruction/SKILL.md) | 历史样本 | 样本 1 有差分与机械交接。真实宿主往返待验。 [案例验收](../sample-1/ACCEPTANCE.md) |
| [`reverse-engineering`](../../core/skills/reverse-engineering/SKILL.md) | 历史样本 | 只证明该 PE 样本。 [案例验收](../sample-1/ACCEPTANCE.md) |
| [`supply-chain-security`](../../core/skills/supply-chain-security/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`thick-client`](../../core/skills/thick-client/SKILL.md) | 历史样本 | 自建 Windows/.NET 样本。 [案例验收](../netwin-1/ACCEPTANCE.md) |
| [`threat-hunting`](../../core/skills/threat-hunting/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`threat-intelligence`](../../core/skills/threat-intelligence/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`wifi-wireless`](../../core/skills/wifi-wireless/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |
| [`windows-ad`](../../core/skills/windows-ad/SKILL.md) | 本轮范围外 | 未纳入交接与部署修复的验收。 |

另有浏览器观察和自建算术验证码的[历史案例](../captcha-1/ACCEPTANCE.md)。自建验证码不构成独立上游技能目录。
