# 怎么跑第一个小目标（README 实操页）

> **v3.2：路径不写死。** 下面所有 `<...>` 占位符的实际值都在唯一配置文件 `%USERPROFILE%/.fusion/fusion-home.yaml`（`shared_folder` / `node_exe` / `ghidra_install_dir` / `java_home`）。换盘只改这一行，再跑 `tools/fusion-sync.sh`（同步脚本会重写 `.mcp.json`、根 CLAUDE.md、全局技能指针）。

## 前置

- 工作目录：共享文件夹（`fusion-home.yaml` 的 `shared_folder`）。
- REA 需要 Node：`fusion-home.yaml` 的 `node_exe`（版本见 `lifecycle/versions.lock`）。
- REA 需要 Ghidra + JDK：`fusion-home.yaml` 的 `ghidra_install_dir` / `java_home`，经 `.mcp.json` 的 `env` 注入。
- 原版样本：样本 1/2 的原始文件在共享文件夹（本轮为 D 盘，路径随部署；快速复制见 `cases/deploy/DEPLOY-REPORT.md`）。
- 样本 2（ELF）跑 Linux 侧：QEMU + Alpine 内核，路径同为部署时配置。

## 怎么看装上了

- 工具列表：`python -I cases/stage1/mcp_probe.py <node_exe> engine/rea/scripts/rea.mjs cases/stage1/tools-list-rea.json mcp`，看 `tool_count=260`。
- REA 体检：`<node_exe> engine/rea/scripts/rea.mjs doctor`（`ghidra*` 应 healthy）。
- 技能安装（v3.2 指针式）：`~/.claude`、`~/.codex`、`~/.pi` 三个全局技能目录都有 `reverse-skill-router/SKILL.md`（仅指针，指向 `shared_folder/core/skills/SKILL.md`）。旧的 `.claude/skills`、`.agents/skills`、`.pi/skills` 三份拷贝按 v3.2 §11.2 废止。

## 怎么跑样本 1

```bash
# 反编译与验收（详见 cases/sample-1）
python -I cases/sample-1/reimpl/differential_test.py <SHARED_FOLDER>/samples/s1/CrackMe.exe cases/sample-1/evidence/E-006-differential.json
python -I cases/sample-1/reimpl/boundary_test.py <SHARED_FOLDER>/samples/s1/CrackMe.exe cases/sample-1/evidence/E-008-boundary.json
python -I cases/sample-1/reimpl/comparator_check.py <SHARED_FOLDER>/samples/s1/CrackMe.exe cases/sample-1/evidence/E-007-comparator-selfcheck.json
# 独立实现（密码 mr1337）
python -I cases/sample-1/reimpl/validator.py mr1337
```

预期：5 个核心用例 `all_match: true`，边界 6/6 `all_match: true`，坏变体 `detected_difference: true`。

## 怎么跑样本 2

```bash
# 生成序列号（需先装 capstone/unicorn/elftools）
python -I cases/sample-2/reimpl/keygen.py <SHARED_FOLDER>/samples/s2/howo-not-to-simple-keygen alice bob@example.com
# 五用例（2 个由 keygen 生成，3 个无效输入）
python -I cases/sample-2/reimpl/run_cases.py <SHARED_FOLDER>/samples/s2/howo-not-to-simple-keygen <SHARED_FOLDER>/tmp/s2cases.json cases/sample-2/evidence/E-005-five-cases.json
# 表一致性验证
python -I cases/sample-2/reimpl/verify_table.py <SHARED_FOLDER>/samples/s2/howo-not-to-simple-keygen cases/sample-2/evidence/E-004-table-alice.bin alice bob@example.com
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

## v3 各领域怎么跑（Stage 11 汇总入口 + V3.1 R5 追加）

前置：Node `<node_exe>`（或把 node 加入 PATH 后直接 `node`）。所有样本均为自建学习目标（第三方样本下载网络不稳，如实记录）。

| 领域 | 入口命令 | 案子路径 | 验收文件 |
|---|---|---|---|
| JS/网页算法 | `node cases/js-1/reimpl/differential_test.mjs` | `cases/js-1/` | `cases/js-1/ACCEPTANCE.md` |
| APK（算法抽取） | `node cases/apk-1/reimpl/licensecheck.mjs`（validate）+ `node cases/apk-1/reimpl/comparator_check.mjs` | `cases/apk-1/` | `cases/apk-1/ACCEPTANCE.md` |
| 浏览器扩展 | `node cases/ext-1/reimpl/extrepro.mjs`（tokenFor）+ `node cases/ext-1/reimpl/comparator_check.mjs` | `cases/ext-1/` | `cases/ext-1/ACCEPTANCE.md` |
| 协议 | `cd cases/protocol-1 && node reimpl/decode.mjs`（decode 对照）；抓包：tshark loopback | `cases/protocol-1/` | `cases/protocol-1/ACCEPTANCE.md` |
| 浏览器自动化（观察） | chrome-devtools 打开 `cases/js-1/target/index.html`（本地 8765 服务）→ 点击 → 录请求 | `cases/automation-1/` | `cases/automation-1/ACCEPTANCE.md` |
| 验证码 | `node cases/captcha-1/reimpl/captcharepro.mjs`（token）+ `node cases/captcha-1/reimpl/comparator_check.mjs` | `cases/captcha-1/` | `cases/captcha-1/ACCEPTANCE.md` |
| Windows+.NET+厚客户端（V3.1 R5） | `python -I cases/netwin-1/reimpl/licensecheck.py`（+ 原版 `target/build/out/build.exe`） | `cases/netwin-1/` | `cases/netwin-1/ACCEPTANCE.md` |
| Go/Rust（V3.1 R5） | `cd cases/gorust-1 && go run reimpl/check.go` | `cases/gorust-1/` | `cases/gorust-1/ACCEPTANCE.md` |

「一个没看过方案的人照着跑」：每个领域先读其 `ACCEPTANCE.md`，再看 `reimpl/` 里的复现脚本，命令见上表；期望输出在验收文件里写明。

声明：v3 各领域样本均为自建学习目标；模式以「算法抽取（模式 3）」为主，验收词用「通过 / 部分通过 / 不通过」。样本 1、2（crackmes）仍按 v2.1 的 L4/L5 口径。
- 限制：样本 1/2 未声明 L5；Seep 未参与（以后再说）。