# DECISION-LOG：为什么这样接、为什么删那一块

按时间顺序记录重要决定。每条都写：决定、理由、证据位置。

## 2026-11-20

### D1 把四条勘误写入 v2.1，v2.0 保留
- 决定：新建 `FUSION-FINAL-v2.1.md`，四条勘误全部写入；不覆盖 v2.0。
- 理由：用户明确指令；第 0 步的历史结论是不通过、勘误已核对未写入。
- 证据：`CHANGE-REQUEST.md`、`cases/validation/LONG-RUN-STOP.md`。

### D2 本轮只做前两个项目，Seep 记为「以后再说」
- 决定：REA、reverse-skill 签出并安装；Seep 不签出、不安装、不抽取。
- 理由：用户指令「第 3 条提到第三个项目脚本那句只是改事实，不是让你去做第三个项目」；样本 1/2 不需要 Seep。
- 证据：`FUSION-FINAL-v2.1.md` 范围说明、`lifecycle/MANIFEST.yaml`。

### D3 用 Node 24.22.1 而非系统 Node 24.20
- 决定：下载官方 Node 24.22.1 到 `D:/Tools/node-24.22.1`，仅 REA 相关命令用它。
- 理由：REA `engines.node` 要求 `^24.22.1`，系统 24.20 被 `engine-strict` 拒绝；不改系统环境。
- 证据：`cases/stage1/LOCAL-CHECKOUT.md` 第 4 节。

### D4 REA 用 `npm ci --ignore-scripts` + 单独编译，绕过 cmd 子进程拿不到 PATH
- 决定：先 `npm ci --ignore-scripts`，再 `npm run compile`。
- 理由：本机 npm 的 esbuild 等生命周期脚本由 cmd.exe 子进程执行，其 PATH 为空；`scripts-prepend-node-path` 无效。绕过不影响产物（dist 编译完成）。
- 证据：`cases/stage1/STAGE1-REPORT.md` 第 2.1 节。

### D5 从 npm 包取回 Windows 原生模块，升级 Ghidra 12.2 + JDK 25
- 决定：`native/windows/build/` 的两文件从 `rea-agents@6.9.0` tarball 恢复；Ghidra 升级到 12.2（`D:/Tools/Ghidra-12.2`），JDK 换 Temurin 25（`D:/Tools/jdk25`）。
- 理由：REA 文档指定的恢复方法；Ghidra 12.2 要求 JDK 25。
- 证据：`cases/stage2/WIRING.md` 第 1.1 节。

### D6 样本 1 的边界不一致用「cin >> 分词」修复
- 决定：`validator.py` 增加 `read_token`（按空白分词）。
- 理由：第一轮 B3/B6 不一致，原版用 `cin >> std::string`；补上后 6/6 一致。
- 证据：`cases/sample-1/evidence/E-008-boundary.json`。

### D7 样本 2 改用 Ghidra 无头 + gdb，因为 REA 的 Windows Ghidra 只收 PE/MZ
- 决定：不用 REA 的 ELF 分析；用 Ghidra 12.2 `analyzeHeadless` + gdb 断点 dump 表。
- 理由：`binary_overview` 返回 `target_format_unsupported`；这是 REA 的 Linux/Windows 差异，不是安装故障。
- 证据：`cases/sample-2/evidence/E-002-overview.json`。

### D8 样本 2 复现用 Unicorn 模拟哈希，而不是高级语言重写
- 决定：`emulate_hash.py` 模拟 0x401d80 机器码；与 gdb dump 的运行时表逐字节一致。
- 理由：哈希反编译太复杂（大量 16 字节变量短循环），机器码级复现能保证行为一致且可验证。
- 影响：这让 L4 只算「部分通过」（依赖原 ELF），L5 未声明。
- 证据：`cases/sample-2/evidence/E-006-table-verify-*.txt`。

### D9 不声明 L5
- 决定：样本 1、2 都只报 L4（部分）/本轮口径，不写「基本成功」。
- 理由：v2.1 §5.4 明确抓坏变体不等于 L5；两边都没有复刻控制台等副作用面。
- 证据：`cases/sample-1/ACCEPTANCE.md`、`cases/sample-2/ACCEPTANCE.md`。

### D10 把 reverse-skill 恢复成完整版（v3 §1.3 / §4.1 的冻结决定）
- 决定：v2.1 §4 的瘦身作废，把锁定提交 `ce67509…` 的整个 reverse-skill 复制回 `core/`，覆盖瘦身后的 208 个文件。
- 理由：Davis 2026-11-20 纠正——v2.1 的瘦身是 Muse 自作主张，Davis 从来没让瘦身；reverse-skill 是当全领域手册建的，瘦身砍掉了以后能做 APK/扩展/协议/验证码的模块，还断掉了 9 个技能对 `field-journal/precedent-reverse.md` 的引用。
- 办法：不用删领域来避免路由打架，改用 v3 §3.3 的三条：reverse-skill 唯一总控、REA 只当 MCP 工具、Seep 不当总控。
- 实测：core 恢复后 675 个文件（上游 676，只差 `.git/`）；`field-journal/precedent-reverse.md` 已存在，18 个技能文件引用全部能解析；REA 子模块 5 个技能无 reverse-skill 式路由（无 master-route/case-init）。
- 证据：`lifecycle/MANIFEST.yaml`（stage_5a）、命令 `diff -rq core upstream/reverse-skill`、`test -f core/skills/field-journal/precedent-reverse.md`。

## 未来待办（卡点，未解决）

- 样本 3 未执行；第 4 阶段之后才做。
- Seep 的抽取与运行未开始。
- `check_handoff.py` 没有为本轮交接单生成 JSON 指针清单（需要 `handoff-manifest.json`）。
- REA 的可选引擎（hopper/ida/jadx/kuna）未装，`doctor` 总体系 healthy=false。