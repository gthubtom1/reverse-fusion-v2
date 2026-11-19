# USED-FUNCTIONS：我们到底用了上游哪些功能

状态两栏分开：**固定版本文档已核**＝锁定提交里有这份资料；**本机运行已核**＝有本机命令输出或工具列表作证。两者不一致以本机为准。

## REA（morluto/rea @ 4491c84c82140a43fa12390b727840a433875ba8，6.9.0）

| 文件/位置 | 函数名 / 工具名 | 用来干什么 | 固定版本文档已核 | 本机运行已核 |
|---|---|---|---|---|
| `src/` 全仓 | `rea mcp`（stdio 启动） | MCP 服务器入口 | 是 | 是（`cases/stage1/tools-list-rea.json` 握手成功） |
| MCP 工具 | `open_binary` | 打开本地样本并绑定分析 provider | 是 | 是（样本 1、样本 2 均调用成功） |
| MCP 工具 | `binary_overview` | 汇总二进制概览（pe/x86_64、分段） | 是 | 是（样本 1 返回 `ev_646685c7…`；样本 2 被平台拒绝） |
| MCP 工具 | `list_procedures` | 列出函数清单 | 是 | 是（样本 1 列出 701 个函数） |
| MCP 工具 | `search_procedures` | 按名字查找函数 | 是 | 是（样本 1 main 检索） |
| MCP 工具 | `analyze_function` | 反编译/分析单个函数 → 证据 | 是 | 是（样本 1 的 main、校验函数） |
| MCP 工具 | `get_evidence_bundle` | 读保留的证据记录与完整证据包 | 是 | 是（summary/complete 均成功） |
| MCP 工具 | `export_evidence_bundle` | 把会话确定性 Evidence 写到本地路径 | 是 | 历史成功一次（样本 1 E-010，2 条记录） |
| MCP 工具 | `compare_functions` | 函数比对 | 是 | 历史成功一次（样本 1 E-012）；E-011 不计成功 |
| `compare_artifacts` | 产物比对 | 是 | 未见调用回执 |
| `verify_reconstruction` | 重建验证 | 是 | 样本 1 E-013 返回 `invalid_request` |
| MCP 工具 | `compare_managed_members` | 比托管成员 | 是 | 本机未调用 |
| `scripts/rea.mjs` | `--version` | 版本核验 | 是 | 是（返回 6.9.0） |
| `scripts/rea.mjs` | `doctor` | 环境体检 | 是 | 是（`cases/stage2/rea-doctor-after.txt`；总体 healthy=false） |

## reverse-skill（gthubtom1/reverse-skill @ ce675096e6a2cd4789a76f9bd618feddc2b6f333，1.9.0）

| 文件 | 函数名 / 模块 | 用来干什么 | 固定版本文档已核 | 本机运行已核 |
|---|---|---|---|---|
| `skills/SKILL.md` | 总控 router | 路由、建案子、证据账 | 是 | 是（`core/skills/SKILL.md` 为准分发） |
| `skills/reconstruction/SKILL.md` | R46 | L0–L6、L4/L5 验收 | 是 | 未整体运行；本机按 R46 口径做了用例对照 |
| `skills/reconstruction/scripts/check_handoff.py` | 机械检查 | 机器核对交接单 | 是 | 样本 1/2 均有机械检查回执，见第三方审计 §2 |
| `skills/reconstruction/examples/synthetic-project` | 示例案子 | 参考格式 | 是 | 是（check_handoff 用其运行） |
| `skills/js-reverse` | Rebuild / js-reverse 方法流 | JS 签名本地复现 | 是 | 是（Stage 5：Node 本地复现 + chrome-devtools 观察浏览器，未用 js-reverse_* MCP） |
| reverse-skill `skills/apk-reverse`, `mobile-reverse` | jadx / apktool 方法流 | APK 解包、找关键算法 | 是 | 是（Stage 6：jadx 1.5.6 反编译 + Node 复现；apktool 未实际执行解包） |
| （工具）jadx | cli 反编译 | 反编译 class/APK | — | 是（jadx --version 1.5.6；反编译 MainActivity.class） |
| （工具）apktool | cli | APK 解包/重打包 | — | 是（--version 3.0.3；本阶段未实际解包） |
| （工具）adb / Android SDK | adb, emulator | 模拟器与设备 | — | 是（android-29 模拟器启动，adb devices device） |
| （工具）frida | frida-server / CLI | 动态 hook | — | 是（--version 17.17.0；本阶段未实际 hook） |
| （工具）d8 (R8) | dex 编译 | class→dex | — | 不适用（d8 8.2.2 在两个 JDK 下崩溃，本机未成 dex） |
| reverse-skill `skills/browser-extension-reverse` | 解包→manifest→background | 扩展逻辑定位 | 是 | 是（Stage 7：读 manifest、定位 service_worker tokenFor、浏览器上下文跑原版） |
| reverse-skill `skills/protocol-reverse` | 抓包→还原→decode | 协议字段/状态机还原 | 是 | 是（Stage 8：tshark 抓 loopback pcap→导出 payload→Node decode 对照） |
| （工具）tshark (Wireshark) | 抓包/导出 | loopback 抓包 | — | 是（4.6.8，NPF_Loopback；E-001 中 pcapng + payload 导出） |
| reverse-skill `skills/browser-automation` | 打开→点击→录制 | 动态观察支撑 | 是 | 是（Stage 9：chrome-devtools 打开测试页、点击、录制请求链路） |
| reverse-skill `field-journal/2026-07-05_dsl-vm-captcha-reverse.md` + `browser-automation/references/distilled-captcha-evidence.md` | 验证码方法 | 自有验证码定位/复现参考 | 是 | 是（Stage 10：借其常量表+函数追踪方法复现自建验证码 token） |
| `skills/case-review` | 只读审查 | 核对证据链与哈希 | 是 | 本机未调用 |
| `skills/docs-generator` | 报告模板 | 生成报告 | 是 | 是（用于 ACKNOWLEDGE 类标注的验收/交接单文档） |

## Seep（angusdevgo/Seep-Reverse-Lab @ 1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e，1.15.0）

本轮未签出、未安装、未抽取。sampler 1/2 无许可证校验或加壳，按 v2.1 §1.4 不需要 Seep。README 与 MANIFEST 均记为「以后再说」。

## 备注

- REA 的四个「导出/比对」类工具在 v2.1 里是「固定版本文档已核」；本机 `tools/list` 已确认名字存在，运行结果以对应样本 E-010 至 E-013 原始回执为准。
- 未把「查到名字」写成「安装成功/调用成功」。