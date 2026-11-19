# 怎么跑第一个小目标（README 实操页）

## 前置

- 工作目录：`D:\Project\最终版聚合`（Windows，git bash）。
- REA 需要 Node 24.22.1：`D:/Tools/node-24.22.1/node-v24.22.1-win-x64/node.exe`。
- REA 需要 Ghidra 12.2（`D:/Tools/Ghidra-12.2/ghidra_12.2_PUBLIC`）与 JDK 25（`D:/Tools/jdk25`），通过 `.mcp.json` 的 `env` 注入。
- 原版样本文件放在仓库外：样本 1 `D:/tmp/fusion-samples/s1/CrackMe.exe`，样本 2 `D:/tmp/fusion-samples/s2/howo-not-to-simple-keygen`（不随仓库分发）。
- 样本 2 是 ELF，需要 Linux：用 QEMU `C:/Program Files/qemu/qemu-system-x86_64.exe` + Alpine 内核 `D:/tmp/alpine/vmlinuz-virt` + 静态 busybox `D:/tmp/alpine/busybox`。

## 怎么看装上了

- 工具列表：`python -I cases/stage1/mcp_probe.py <node.exe> engine/rea/scripts/rea.mjs cases/stage1/tools-list-rea.json mcp`，看 `tool_count=260`。
- REA 体检：`<node.exe> engine/rea/scripts/rea.mjs doctor`（`ghidra*` 应 healthy）。
- 技能安装：`.claude/skills/`、`.agents/skills/`、`.pi/skills/` 三个目录都有 `reverse-skill-router/SKILL.md` 和 `reconstruction/SKILL.md`。

## 怎么跑样本 1

```bash
# 反编译与验收（详见 cases/sample-1）
python -I cases/sample-1/reimpl/differential_test.py D:/tmp/fusion-samples/s1/CrackMe.exe cases/sample-1/evidence/E-006-differential.json
python -I cases/sample-1/reimpl/boundary_test.py D:/tmp/fusion-samples/s1/CrackMe.exe cases/sample-1/evidence/E-008-boundary.json
python -I cases/sample-1/reimpl/comparator_check.py D:/tmp/fusion-samples/s1/CrackMe.exe cases/sample-1/evidence/E-007-comparator-selfcheck.json
# 独立实现（密码 mr1337）
python -I cases/sample-1/reimpl/validator.py mr1337
```

预期：5 个核心用例 `all_match: true`，边界 6/6 `all_match: true`，坏变体 `detected_difference: true`。

## 怎么跑样本 2

```bash
# 生成序列号（需先装 capstone/unicorn/elftools）
python -I cases/sample-2/reimpl/keygen.py D:/tmp/fusion-samples/s2/howo-not-to-simple-keygen alice bob@example.com
# 五用例（2 个由 keygen 生成，3 个无效输入）
python -I cases/sample-2/reimpl/run_cases.py D:/tmp/fusion-samples/s2/howo-not-to-simple-keygen D:/tmp/s2cases.json cases/sample-2/evidence/E-005-five-cases.json
# 表一致性验证
python -I cases/sample-2/reimpl/verify_table.py D:/tmp/fusion-samples/s2/howo-not-to-simple-keygen cases/sample-2/evidence/E-004-table-alice.bin alice bob@example.com
```

预期：TC1/TC2 accepted（打印 flag），TC3–TC5 denied；`verify_table` 输出 `match True`。

## 出了问题先看哪里

- 写入成功与否，以命令退出码和生成的 json 为准，不靠聊天记录。
- 看 `cases/stage1/STAGE1-REPORT.md`（安装）→ `cases/stage2/WIRING.md`（接线）→ `cases/stage3/STAGE3-REPORT.md`（样本结果）。
- 若 REA 报 provider 不可用：重新核对 Ghidra/JDK 环境变量是否进了 `.mcp.json`；`node.exe` 是否为 24.22.1。
- 若样本 2 无法启动：QEMU 内核/initramfs 是否就位；`qemu_run.py` 的路径硬编码在顶部。
- 本项目的文件不在仓库里的部分（样本、运行库、工具）在仓库外，克隆后需按 README 前置补齐。

## 已完成 / 未完成

- 已做：v2.1 勘误；第 1–3 阶段（安装、接线、接线测试、样本 1 L4、样本 2 本轮口径）。
- 未做：样本 3；第 4 阶段的「定版」与 lifecycle 的完整性走查（本轮补齐了 lifecycle 5 件套，定版号仍为 v2.1）。

## v3 各领域怎么跑（Stage 11 汇总入口）

前置：Node `D:/Tools/node-24.22.1/node-v24.22.1-win-x64/node.exe`（或把 node 加入 PATH 后直接 `node`）。所有样本均为自建学习目标（第三方样本下载网络不稳，如实记录）。

| 领域 | 入口命令 | 案子路径 | 验收文件 |
|---|---|---|---|
| JS/网页算法 | `node cases/js-1/reimpl/differential_test.mjs` | `cases/js-1/` | `cases/js-1/ACCEPTANCE.md` |
| APK（算法抽取） | `node cases/apk-1/reimpl/licensecheck.mjs`（validate）+ `node cases/apk-1/reimpl/comparator_check.mjs` | `cases/apk-1/` | `cases/apk-1/ACCEPTANCE.md` |
| 浏览器扩展 | `node cases/ext-1/reimpl/extrepro.mjs`（tokenFor）+ `node cases/ext-1/reimpl/comparator_check.mjs` | `cases/ext-1/` | `cases/ext-1/ACCEPTANCE.md` |
| 协议 | `cd cases/protocol-1 && node reimpl/decode.mjs`（decode 对照）；抓包：tshark loopback | `cases/protocol-1/` | `cases/protocol-1/ACCEPTANCE.md` |
| 浏览器自动化（观察） | chrome-devtools 打开 `cases/js-1/target/index.html`（本地 8765 服务）→ 点击 → 录请求 | `cases/automation-1/` | `cases/automation-1/ACCEPTANCE.md` |
| 验证码 | `node cases/captcha-1/reimpl/captcharepro.mjs`（token）+ `node cases/captcha-1/reimpl/comparator_check.mjs` | `cases/captcha-1/` | `cases/captcha-1/ACCEPTANCE.md` |

「一个没看过方案的人照着跑」：每个领域先读其 `ACCEPTANCE.md`，再看 `reimpl/` 里的复现脚本，命令见上表；期望输出在验收文件里写明。

声明：v3 各领域样本均为自建学习目标；模式以「算法抽取（模式 3）」为主，验收词用「通过 / 部分通过 / 不通过」。样本 1、2（crackmes）仍按 v2.1 的 L4/L5 口径。
- 限制：样本 1/2 未声明 L5；Seep 未参与（以后再说）。