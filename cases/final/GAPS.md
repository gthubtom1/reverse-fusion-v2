# v3 完成标准缺口清单（Stage 12）

日期：2026-11-20。对照 `FUSION-FINAL-v3.md` §11.1（v2.1 §9 十条 + 6 条新增）逐项核对。**结论：基本完成，但有 3 项缺口未做/部分，如实列出，不宣称 100%。**

| # | 完成标准 | 状态 | 说明 |
|---|---|---|---|
| 1 | 三个仓库锁第 2 节版本 | ✅ | REA 4491c84、reverse-skill ce67509 已签出核对；Seep 1ea9399 未签出（deferred，属 Track B） |
| 2 | 完整版已恢复（671 文件）| ⚠️ 部分 | core 已恢复为完整版，实测 675 文件（上游 676 差 `.git`），与 v3 写的 671 有出入（统计口径未核实） |
| 3 | Seep 只抽 5 样 | ⛔ 未做 | 按 Track B 拆分，Seep 抽取/运行不在本轮执行提示词范围内（计划文件 §4.3 已列清单），记「以后再说」 |
| 4 | REA MCP 能调通，与总控互传证据 | ✅ | REA `tools/list` 260 工具，Connected；Stage 2 接线测试证据落盘；各领域 REA/浏览器/JVM 证据齐 |
| 5 | 交接单模板齐 | ✅ | `cases/templates/reconstruction-handoff.md` + 6 领域各案交接单 |
| 6 | 第一个小目标完整跑过 | ✅ | 样本 1 L4、样本 2 口径（v2.1）；v3 各领域也跑通 |
| 7 | 新程序能跑 + 5 用例一致 | ✅/⚠️ | JS/ext/协议/验证码的算法抽取（模式 3）5 用例全对；APK 未成 dex（d8 崩），模拟器 UI 未实测 → APK 部分通过 |
| 8 | 坏变体能被发现 | ✅ | 各领域比较器自检（改常量后输出变）全部 ok |
| 9 | 未知清单写清 | ✅ | 6 领域 unknowns.md 均列出未做/未验证项 |
| 10 | lifecycle 齐 + README 能照着跑 | ✅ | MANIFEST/USED/DECISION/UPDATE-CHECK/模板 + README（含各领域入口） |
| 11 | 每领域 ACCEPTANCE（四档） | ✅ | 6 领域全部有，结论格式合规 |
| 12 | 每领域 5 用例双侧 + 比较器自检 | ✅ | 各 reimpl 脚本 + 证据 |
| 13 | 未通过/部分有证据 | ✅ | APK 的 unknowns/ACCEPTANCE 记录 d8 卡点 |
| 14 | USED-FUNCTIONS 每领域两栏 | ✅ | js-1/apk-1/ext-1/protocol-1/automation-1/captcha-1 均有行 |
| 15 | README 照跑任一领域 | ✅ | 「v3 各领域怎么跑」入口表 |
| 16 | Stage 11 回归已记录、失败不覆盖 | ✅ | `cases/aggregation/REGRESSION.md` 无回归失败 |

**缺口汇总：**
- G1：Seep 抽取与运行未做（Track B，Davis 亲自触发；计划文件已有清单但执行提示词不含）。
- G2：APK 未做成 dex、模拟器 UI 未实测（d8 工具在本机 JDK21/25 都崩溃），APK 领域「部分通过」。
- G3：core 文件数与 v3 文档表述（671/463）不符，实测 675/676（差 .git），统计口径差异未核实。

以上三项都不阻塞 v3 定版本身（v3 允许「未做/部分通过」的领域如实记录），但按 §11.1「只要有一条没过就不许说 v3 做完了」，所以 V3-REPORT 结论写「基本完成，3 项缺口见 GAPS」。