# 融合最终方案 v2.1（当前执行版，只有一个文件、一个版本号）

> 版本：v2.1，日期 2026-11-20，冻结。
> 这就是当前执行版。不要再开新版本、不要开分支、不要开 PR、不要把方案拆成 v2.2、v2.3。想改，先写 CHANGE-REQUEST，等用户批了再改，改完整个文件版本号才动。
> 这份文件代替之前所有的 v2.0、v1.0、v1.1、补丁。以前那几份里和这份打架的地方，以这份为准。
> **v2.1 只做四项文档勘误，不改执行顺序、锁定提交、交接字段、验收标准。** v2.0 原文保留在 [FUSION-FINAL-v2.md](FUSION-FINAL-v2.md)，不覆盖。

## v2.1 改了什么（只改事实与证据口径，四条）

| # | 位置 | v2.0 的问题 | v2.1 改成什么 | 依据 |
|---|---|---|---|---|
| 1 | §5.1、§5.3、§10.2 | 把人读的交接单当成检查器输入；检查器路径写成 `tools/check_handoff.py`；示例把 TC5 原版输出写成 `6`，同节又说 6/6.0 未测清 | 人读 Markdown 与机器 JSON 指针清单分开，共用同一份原证据；路径更正为 `skills/reconstruction/scripts/check_handoff.py`；TC5 标为「未知、未验证」 | `VALIDATION-REPORT.md` 第 45 行；`cases/validation/notes-r46.md` 第 43–49 行；`REVIEW-2.md` 第 7 行 |
| 2 | §5.4、§5.5 | L0–L6 用简写代替上游定义；把「抓到坏变体」写进 L5 定义 | 照抄 R46 `SKILL.md` 第 29–39 行原文；L5 要求所选边界/错误/副作用的新鲜双侧对照；结构比对、双侧行为对照、独立运行、比较器自检分开记 | `cases/validation/notes-r46.md` 第 5–17 行；`REVIEW-2.md` 第 13–15 行 |
| 3 | §2、§4.4、§4.5、§6.2 | 把锁定提交的候选措辞误推成没有正式发布；把存在的 R44 记为缺号；把 `check_routing.py` 缺失扩大成整仓没有 | 正式 `v1.9.0` 存在且指向 `7cc3109…`，项目仍锁 `ce67509…`；缺号只有 R42、R43；脚本在被抽取的两个技能目录里没有、`Tool/upstream/` 两份镜像各有一份，镜像版未验证可运行 | `VALIDATION-REPORT.md` 第 31、36、38 行；`cases/validation/RECHECK.md` 第 9 行 |
| 4 | §5.2、§5.4、§10.2 | 把工具名「文档有写」和「本机跑过」混成一个状态；把 Spec Kit 文档基线写成安装回执 | 同一张表分「固定版本文档已核」「本机运行已核」两栏；Spec Kit `v1.3.0` 是文档/源码基线，`specify-cli` 包版本 `1.3.0`；本机安装与集成参数另测 | `cases/validation/notes-r46.md` 第 39–41 行；`REVIEW-2.md` 第 25–27 行 |

范围说明：本轮只执行前两个项目（REA、reverse-skill）。第三个项目（Seep）的抽取与运行记为「以后再说」，不阻塞第 1–3 阶段。

## 给零基础的 Davis 看的 1 页说明（你只需要看这一节，其他的都是给电脑上的智能体看的）

**这是什么？** 你想做的事很简单：你在 Codex 里说一句白话，比如“帮我看懂这个软件，再重做一个一样的”，电脑就能自己去看、自己去做，最后交给你一个能跑的新软件，还告诉你哪里做对了、哪里还没弄清。

**现在卡在哪？** 三个现成的工具各会一半，没有一个会全部。reverse-skill 会带路和记账，REA 会看代码，Seep 会对付难啃的锁和壳。这份方案就是把这三样拼成一条流水线，谁先谁后都定死了。

**你要做什么？只有 3 步，你不用懂技术：**
1. 把这份文件发给电脑上的智能体，跟他说：“按这份做，先做第 0 步。”
2. 他做完第 0 步会交一份报告，你不用看懂全文，只看他最后那句“能开始”还是“不能开始”。
3. 他说能开始，你就说“进下一段”，他做完一段停下来，你再说一次。一共 5 段，做完第 3 段那个小测试，才算真的有用。

**什么叫成功？** 不是他说“做完了”，是这 3 件事都真发生了：新软件能跑起来；至少 5 个地方，原版和新版结果一样；他故意弄坏一个地方，检查能发现。少一个都不算成功。

**你不用担心的事：** 不用记顺序，不用记版本号，不用懂 MCP、R46 这些词。那些都在文件里，智能体自己会查。你只需要记住：一次只做一段，做完就停，不要让他一次跑 10 个小时。

---

## 怎么读这份文件

- 一句话目标在第 1 节，顺序定死在第 1 节。
- 安装怎么写在第 3 节，照着放文件就行。
- 先做第 0 步（第 6 节），第 0 步没过不许往下做。
- 每做完一个阶段就停下，写文件，等用户说“进下一段”再进。
- “待核实”的意思是：报告里没写清楚，不要猜，第 0 步去原文里抄出来。

---

## 1. 一句话目标 + 最终顺序（定死）

### 1.1 一句话目标

用户在 Codex 里说一句白话，智能体能看懂一个软件，再重做一个功能一样的版本，并且能说清哪里对上了、哪里没测到。

- “看懂”指的是：知道软件有哪些功能、每个功能先干什么再干什么、关键算法怎么算。
- “重做”指的是：写一个能独立跑起来的新程序，不依赖原程序。
- “说清”指的是：每个结论都有证据编号，没测到的地方写进未知清单，不许假装知道。

### 1.2 执行顺序（每次干活时，谁先谁后，定死）

```
用户白话（Codex）
  ↓ ① 总控
reverse-skill（瘦身后）—— 接单、判断目标类型、建案子、记证据账
  ↓ ② 分析引擎
REA —— 看代码、拿证据
  ↓ ③ 只在硬骨头时临时叫（不是常驻）
Seep 提取件 —— 只解决许可证校验、加壳、Flutter 那一小块
  ↓ 回到 ①
reverse-skill R46 —— 行为模型 → 写规格（Spec Kit）→ Codex 写新程序 → 原版新版对照着测
  ↓ ④ 验收
REA 比对 + reverse-skill case-review —— 按 L4/L5 验收（L4、L5 的意思见第 5 节）
```

一句话记：**总控是 reverse-skill，干活的引擎是 REA，Seep 只是关键时刻翻的手册。**

为什么是这个顺序，不换：Seep 先最差，它的 14 个案例全是绕过许可证校验，交出来的是打过补丁的原程序，不是新程序；REA 先只有分析，没有路由、没有记账、没有复刻步骤；reverse-skill 是唯一有 R46 复刻流程和 L4/L5 验收标准的。这个结论有三份拆解报告做依据，不是感觉。

### 1.3 安装顺序（装到电脑上的顺序，和执行顺序不一样，定死）

1. 先装 REA（引擎）
2. 再装 reverse-skill（总控）
3. 最后只抽 Seep 的方法和工具，不装 Seep 整套工作台

安装顺序和执行顺序不一样是正常的：装的时候 REA 先，是因为它最重；干活的时候 reverse-skill 先，是因为它负责判断走哪条路。不要把两个顺序混在一起。

### 1.4 分目标走不同路（不要所有目标都走同一条长路）

- 普通 JS、Electron、.NET 软件：reverse-skill → REA → R46 → 验收。Seep 不上。
- 带许可证校验、加壳的 PE、APK：reverse-skill → REA → Seep 提取件（只做那一小块）→ 回到 R46 → 验收。
- Flutter 软件：reverse-skill → REA → Seep 的 Aotopsy（只做 Flutter/Dart 还原那一步）→ 回到 R46 → 验收。

---

## 2. 锁定版本表（定死）

| 项目 | 仓库 | 锁定版本 | 提交号 | 用法 |
|---|---|---|---|---|
| REA | morluto/rea | 6.9.0 | `4491c84c82140a43fa12390b727840a433875ba8` | 只当引擎，不改它的 `src/` |
| reverse-skill | gthubtom1/reverse-skill | 1.9.0 | `ce675096e6a2cd4789a76f9bd618feddc2b6f333` | 总控 + R46 复刻 |
| Seep | angusdevgo/Seep-Reverse-Lab | 1.15.0 | `1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e` | 只抽 5 样（见第 4 节），不装整套 |

注意四件事，写清楚，不藏着：

1. reverse-skill 的锁定提交 `ce67509…` 与正式发布 `v1.9.0` 是两件事。锁定提交的 `CHANGELOG.md:9–11` 使用候选版措辞，但上游存在正式 Release `v1.9.0`（`prerelease: false`），解析附注 tag 后指向 `7cc3109bf14a570c9c852dc76cce05fff424e88c`。本项目仍锁定 `ce67509…`，不自动跟到正式 tag；要不要换，按第 10 节评估。依据：`VALIDATION-REPORT.md` 第 36 行、`cases/validation/RECHECK.md` 第 9 行。
2. Seep 的 1.15.0 来自仓库的 VERSION 文件和 CHANGELOG，但在它的 248 个技能文件里 grep 不到 `1.15.0` 这个数字（A 路报告已核实）。所以版本号以 VERSION 文件为准，技能文件里的版本写法不要当成依据。
3. 不要用 Davis 的 fork 当基准：`gthubtom1/rea` 和上游不一样，没做过逐文件 diff；`gthubtom1/SRL` 相对 Seep 上游领先 480、落后 58，也不要直接当基准。
4. 不要用 `latest`、`main` 这种会自己变的版本。每次拉取都要按上面这张表的提交号 checkout，对不上就停下。
5. 表里的版本号是标签名义版本，锁的是提交号。两者冲突时以提交号为准，把冲突写进 MANIFEST。

---

## 3. 标准安装写法（从 4 个成熟项目总结的）

这一节是新加的，来源是 4 个公开的、可部署的智能体项目，2026-11-20 查的：

- **anthropics/skills + Claude Code**：技能就是一个文件夹，里面一个 `SKILL.md`。
- **OpenAI Codex**：技能在 `~/.agents/skills/`，MCP（Model Context Protocol，一种让智能体调用外部工具的标准协议，简称 MCP）在 `~/.codex/config.toml` 里配。
- **github/spec-kit（Spec Kit）**：`specify init` 一次装好，Claude Code 的技能进 `.claude/skills/`，Codex 的技能进 `.agents/skills/`，两边共用同一套规格文件。
- **Pi（earendil-works/pi）**：技能在 `~/.pi/agent/skills/`，MCP 在 `~/.pi/agent/mcp.json`，也认 `AGENTS.md` 和 `~/.agents/skills/`。

四个项目总结出来的共同规律只有三条，记住这三条就够了：

1. **技能 = 文件夹 + `SKILL.md`。** 技能装上了，就是文件夹放对了位置，里面有 `SKILL.md`，智能体不用重启就能认出来（Claude Code 是这样，Codex、Pi 也是这个路子）。
2. **MCP 服务器 = 配置文件里的一行 + 一个能跑起来的程序。** 只在配置文件里写一行不算装上，程序要能启动、能握手（就是智能体和服务器互相打招呼、确认能通话）、能在工具列表里看到它。
3. **说明文件 = `AGENTS.md`。** 所有智能体都读项目根目录的 `AGENTS.md`。Claude Code 另外读 `CLAUDE.md`（Spec Kit 的做法是 `CLAUDE.md` 里只写一行 `@AGENTS.md`，意思就是“去看 AGENTS.md”）。Pi 也读 `AGENTS.md` 和 `CLAUDE.md`。

### 3.1 三张小表：文件放哪、配置怎么写

#### Codex

| 东西 | 放哪 | 怎么写 / 怎么装 |
|---|---|---|
| 技能（全局，所有项目都能用） | `~/.agents/skills/<技能名>/SKILL.md` | 把文件夹整个复制过去，里面必须有 `SKILL.md`，连同 `scripts/`、`references/` 一起复制 |
| 技能（只给这一个项目用） | `.agents/skills/<技能名>/SKILL.md` | 同上，放在项目根目录下 |
| 说明文件 | 项目根目录 `AGENTS.md` | 写清目标、顺序、不要做的事 |
| MCP 服务器（全局） | `~/.codex/config.toml`，每台服务器一段 `[mcp_servers.<名字>]` | 命令行装：`codex mcp add <名字> -- <启动命令>`；手写 TOML 也可以，`command` 是启动程序，`url` 是远程地址，二选一 |
| MCP 服务器（只给这一个项目用） | `.codex/config.toml` | 同上，只在被信任的项目里才会被读 |

#### Pi

| 东西 | 放哪 | 怎么写 / 怎么装 |
|---|---|---|
| 技能（全局） | `~/.pi/agent/skills/<技能名>/SKILL.md`，也可以用共用的 `~/.agents/skills/` | 同上，文件夹 + `SKILL.md` |
| 技能（只给这一个项目用） | `.pi/skills/<技能名>/SKILL.md` | 同上 |
| 说明文件 | `~/.pi/agent/AGENTS.md`（全局）或项目根目录 `AGENTS.md` | Pi 也读 `CLAUDE.md` |
| MCP 服务器（全局） | `~/.pi/agent/mcp.json` | 命令行装：`pi mcp add <名字> -- <启动命令>`，远程的用 `--url <地址>` |
| MCP 服务器（只给这一个项目用） | `.pi/mcp.json`，加 `--local` | 同上，只在被信任的项目里才会被读 |

#### Claude Code

| 东西 | 放哪 | 怎么写 / 怎么装 |
|---|---|---|
| 技能（全局） | `~/.claude/skills/<技能名>/SKILL.md` | 文件夹 + `SKILL.md`，也可以用 `npx skills add <仓库>` 让工具帮你放 |
| 技能（只给这一个项目用） | `.claude/skills/<技能名>/SKILL.md` | 同上 |
| 说明文件 | 项目根目录 `CLAUDE.md`，里面写一行 `@AGENTS.md` 就行 | 共用的说明写在 `AGENTS.md` 里 |
| MCP 服务器 | `claude mcp add` 命令写进它的配置文件（`.mcp.json`） | 命令行装：`claude mcp add --transport http <名字> <地址>`（远程）或本地启动命令；也可以直接改 `.mcp.json` |

### 3.2 本项目按上面三条怎么装

融合项目叫 `reverse-fusion-v2`，新建，不要直接改以前的 `reverse-fusion-next`。

```
reverse-fusion-v2/
├── AGENTS.md                     # 说明文件，所有智能体都读这一份
├── CLAUDE.md                     # 只有一行：@AGENTS.md（给 Claude Code 用）
├── .agents/skills/               # Codex 的技能放这里（项目级）
│   ├── reverse-skill-router/     # 总控（瘦身后的 reverse-skill）
│   └── reconstruction/           # R46
├── .claude/skills/               # Claude Code 的技能放这里（和上面是同一套文件，复制一份）
│   ├── reverse-skill-router/
│   └── reconstruction/
├── .pi/skills/                   # Pi 的技能放这里（同一套文件，再复制一份）
│   ├── reverse-skill-router/
│   └── reconstruction/
├── core/                         # reverse-skill 瘦身后的源文件（技能的源头）
├── engine/rea/                   # REA，用子模块固定在 6.9.0（见第 7 节第 1 阶段）
├── specialist/seep-extract/      # Seep 提取件（见第 4 节）
├── .codex/config.toml            # Codex 的 MCP 配置（项目级）
├── .pi/mcp.json                  # Pi 的 MCP 配置（项目级）
├── .mcp.json                     # Claude Code 的 MCP 配置（项目级）
├── cases/                        # 每次任务的案子，一任务一目录
└── lifecycle/                    # 生命周期文件夹，见第 10 节
```

装的命令（一次只装一个，装完查完再装下一个）：

```bash
# 1. 先装 REA 的 MCP（Codex 举例，Pi / Claude Code 按 3.1 的表换命令）
# 注意：下面这行包名是待核实，第 0 步先去 REA 仓库查它到底叫什么，查到了再跑，不要直接抄：
# codex mcp add rea -- npx -y rea-agents
# 2. 再把总控技能复制到三个位置（源头是 core/，不要直接改源头）
# 注意：三份是同一套文件的复制品，以后改只改 core/ 里的源头，再重新复制三份，不要各改各的。
cp -r core/skills/reverse-skill-router .agents/skills/
cp -r core/skills/reverse-skill-router .claude/skills/
cp -r core/skills/reverse-skill-router .pi/skills/
```

注意：`rea setup` 和插件不要同时用，二选一。用命令行装了，就不要再装插件那套。

### 3.3 怎么算装上了：两层检查（不要只查文件在不在）

**第一层：文件在不在（10 分钟能查完）。**

- `ls .agents/skills/reverse-skill-router/SKILL.md` 能看到文件
- `ls .claude/skills/reverse-skill-router/SKILL.md` 能看到文件
- `ls .pi/skills/reverse-skill-router/SKILL.md` 能看到文件
- `AGENTS.md` 在项目根目录
- MCP 配置文件里有 `rea` 这一段

文件在，只说明第一层过了，不说明能用。

**第二层：跑起来没有（一个命令看工具列表）。**

- Codex：`codex mcp list` 能看到 `rea`，进 Codex 打 `/mcp` 能看到它是在线的，能列出工具。
- Pi：`pi mcp list` 能看到 `rea`，显示已连接，进 Pi 打 `/mcp` 能看到它。
- Claude Code：`claude mcp list` 能看到 `rea`，进会话打 `/mcp` 能看到它。

第二层过了，才算装上了。第一层过了、第二层没过，就是“放对了但跑不起来”，停下，按第 11 节的停下规则写清楚：哪个命令、报了什么错、配置文件里写的是什么。不要反复重试同一个命令。

**一次只装一个服务器。** 五个一起装，出问题不知道是谁的问题。这是 Spec Kit、Codex 官方文档里都写的做法，不是新发明的。

---

## 4. 留什么、删什么（按 B 路报告原样列）

### 4.1 reverse-skill：留 15 个

| 留下的 | 文件位置 | 留的理由 |
|---|---|---|
| 总控 | `skills/SKILL.md` | 路由、建案子、记证据账的总入口，没有它就没人判断走哪条路 |
| reverse-engineering | `skills/reverse-engineering/` | 唯一明文写“分析完交给重建”的模块，第 5-6 步写了先建行为模型再交给重建 |
| reconstruction（R46） | `skills/reconstruction/` | 复刻流程本身，L0-L6、L4/L5 验收都在这里 |
| js-reverse | `skills/js-reverse/` | Rebuild 阶段，在 Node 里把签名算法本地复现跑通，是局部复现 |
| apk-reverse | `skills/apk-reverse/` | Android APK 分析 + 改包，jadx、apktool、Frida 那条链 |
| dotnet-reverse | `skills/dotnet-reverse/` | .NET/C# 分析，de4dot、dnSpyEx 那条链 |
| binary-diff | `skills/binary-diff/` | 跨版本符号迁移，旧版有符号、新版无符号时用 |
| protocol-reverse | `skills/protocol-reverse/` | 自定义协议还原，产出可复现的解码脚本 |
| ghidra-reverse | `skills/ghidra-reverse/` | Ghidra 分析入口 |
| ida-reverse | `skills/ida-reverse/` | IDA 分析入口 |
| radare2 | `skills/radare2/` | radare2 分析入口 |
| binary-ninja-reverse | `skills/binary-ninja-reverse/` | Binary Ninja 分析入口，HLIL/MLIL 分层，和 IDA/Ghidra 互相印证 |
| mobile-reverse | `skills/mobile-reverse/` | Android + iOS 统一入口，apk-reverse 只管 Android，它补 iOS 那一半 |
| case-review | `skills/case-review/` | 只读审查案子包，查证据链、查 SHA-256，验收时用。B 路报告把它划为“无关”，是因为它不分析、不重建；留它是因为验收需要一个只读的检查员，不能让干活的人自己给自己验收 |
| docs-generator | `skills/docs-generator/` | 写报告、写文档的模板，验收报告、复刻交接单都要它。B 路报告把它划为“无关”，是因为它不分析；留它是因为最后要交一份人能看懂的报告 |

### 4.2 reverse-skill：删 25 个无关模块（B 路报告无关 27 个里，2 个留用，见 4.1）

下面 25 个全部删掉，不要带进融合项目。B 路报告把它们划为“无关”，意思是和“白话分析软件再重做一个功能一样的版本”这件事没有直接关系。

1. api-security——授权 API 渗透测试，找接口漏洞的，不是重做
2. attack-chain——多阶段攻击链编排，侦察、提权、横向、持久化，不是重做
3. cloud-k8s——云、容器、K8s 安全评估，不是重做
4. code-audit——源码安全审计、找漏洞，不是重做
5. ctf-sandbox——CTF、靶场入口，不是重做
6. database-security——数据库安全评估，不是重做
7. diagram-generator——画图的通用工具，不是重做
8. digital-forensics——数字取证、溯源，不是重做
9. edr-bypass-re——绕过 EDR（一种防护软件），不是重做
10. email-security——邮件安全、钓鱼分析，不是重做
11. firmware-pentest——固件、物联网渗透，不是重做
12. hardware-security——硬件接口安全，不是重做
13. identity-federation——联邦身份评估（SAML/OIDC/OAuth），不是重做
14. llm-security——大模型应用安全测试，不是重做
15. ot-ics——工控系统安全评估，不是重做
16. patch-diff-exploit——补丁差分到利用（武器化漏洞），不是重做
17. pentest-tools——主动渗透工具链，Nmap、SQLMap、Metasploit 那套，不是重做
18. pentest-tools/src-hunter——众测、漏洞挖掘，305 个 payload、263 个绕过、2887 个案例，不是重做
19. pwn-chain——从漏洞点到可用 exploit，不是重做
20. radio-sdr——无线电、SDR 研究，不是重做
21. supply-chain-security——供应链安全评估，不是重做
22. threat-hunting——蓝队威胁狩猎，不是重做
23. threat-intelligence——威胁情报、OSINT，不是重做
24. wifi-wireless——Wi-Fi 安全评估，不是重做
25. windows-ad——域、AD 身份攻击，不是重做

数账（第 0 步要重新数一遍）：B 路报告的汇总表写的是“无关 27 个”，就是上面 1-25 条这 25 个有名模块，加上 `case-review` 和 `docs-generator` 这 2 个，合计 27 个。`case-review` 和 `docs-generator` 留下了，理由见第 4.1 节；其余 25 个全部删掉。删完后数一遍：`skills/` 下应该只剩第 4.1 节的 15 个，不是 45 个。

另外单独删：`CTF-Sandbox-Orchestrator/`（136 个文件，CTF 旁路包）和 `pentest-tools/`（114 个文件），这两块合起来占 37% 的文件、52% 的 Markdown 词数，和复刻无关。

### 4.3 reverse-skill：删 7 个间接模块（逐个写为什么不要）

B 路报告里有 16 个“间接相关”模块（只解决“分析”那一半），其中 9 个留下了（见 4.1），下面 7 个删掉，每个都写理由：

1. browser-automation——只做浏览器自动化、点一点、截个图，本身不分析、不重建。动态观察目标软件行为可以用 REA 的进程捕获代替，不用单独留一个模块。
2. browser-extension-reverse——只管浏览器扩展（crx、xpi 两种格式），范围太窄。目标不是扩展时用不上，目标是扩展时按第 10 节走变更流程再加回来。
3. go-rust-reverse——只管 Go、Rust 剥离符号的二进制。v2.0 先做 JS、.NET、PE、APK 这四类，Go、Rust 不在第一批目标里。以后目标是 Go、Rust 时按第 10 节再加回来，不是永远删掉。
4. macos-reverse——只管 macOS、Mach-O。v2.0 的目标是 Windows x64 + Codex（用户一开始定的），macOS 不在第一批里。以后要做 macOS 时再加。
5. malware-analysis——目标是检测、定性、写 YARA 规则（一种给恶意软件打标签的规则），不是重做。分析方法论和 reverse-engineering 重叠，留 reverse-engineering 就够了。
6. reverse-engineering/dsl-vm-reverse——只管 JS 自定义 DSL/VM（一种风控引擎里的小语言），恢复字节码语义、复现 token 生成，范围太窄。通用 JS 复现走 js-reverse 就够了。
7. thick-client——桌面厚客户端安全测试，信任边界、配置、密钥、DLL 劫持那套。它的逆向验证分流到 dotnet、IDA、Ghidra、js-reverse，本身不重建，留那四个就够了。

### 4.4 Seep：只抽 5 样（每一样都是具体文件，不是“借个思路”）

| # | 抽什么 | 具体文件（Seep 仓库里的原路径） | 用来干什么 |
|---|---|---|---|
| 1 | exe-reverse | `Tool/skill/exe-reverse/`（SKILL.md 359 行 + references 41 份 + scripts 16 个） | Windows PE 分析、定位校验代码、恢复算法和密钥。注意：它自己写了“重建源码树”不在覆盖范围，所以它只负责分析那一半，重建那一半走 R46，不要指望它直接交出新程序 |
| 2 | apkseep | `Tool/skill/apkseep/`（SKILL.md 440 行 + references 50 份 + scripts 57 个） | Android 分析全链路，jadx、apktool、Frida、等长 dex 补丁 |
| 3 | client-license-validation-bypass | `Tool/skill/client-license-validation-bypass/SKILL.md`（413 行，只有一个文件） | 许可证校验手册，G0-G6 门、开测四问、7 路绕过决策树。只在目标有许可证校验时才用 |
| 4 | aotopsy | `Tool/aotopsy/`（aotopsy.exe + ghidra_scripts + ida_scripts） | 只用于 Flutter/Dart AOT（一种把 Dart 代码编译成机器码的方式）还原成 Dart 源码。只支持 Dart 2.10-3.13，字段名 97-99% 缺失、局部变量名全丢，这两个限制要写进案子包的未知清单里，不要夸大 |
| 5 | mcp-js-reverse-playbook | `Tool/skill/safe-skills/mcp-js-reverse-playbook/`（SKILL.md 137 行 + references 12 份） | JS 签名链路定位 + 在 Node 本地补环境复现，五阶段 Observe → Capture → Rebuild → Patch → DeepDive，第 3 阶段就叫 Rebuild。这是 Seep 那边最接近“重做”的一个，但复现对象只是签名、加密参数生成链路这一小段，不是重做整个产品 |

**Seep 不要带进来的：** 整套工作台、MCP 服务器（38 个工具不要全注册）、`Tool/upstream/`（2544 个文件，四个上游完整镜像）、`Tool/mcp/Tool/reverselab/` 和 `Tool/upstream/open-reverselab/` 两份不同步的快照（reverselab 是旧版 +73 份本地扩充，upstream 是新版，两份不同步）、webseep、`Tool/cases/`（248 个文件，14 个案例只当参考，不带代码）、`master-route.ps1`（不要直接用，见第 6 节）。

**不要做的事：** 不要把 Seep 当总控，不要注册它的 MCP 当主服务器，不要让它决定走哪条路。它只在总控说“这一步是许可证校验、加壳”时才被叫进来。

**关于 `check_routing.py`（只改事实，不新增任务）：** 它在 `Tool/skill/apkseep`、`Tool/skill/exe-reverse` 里被多次引用，但所抽的这两个目录中没有这个文件；`Tool/upstream/` 的两份镜像里各有一份。镜像里那份能不能运行没有实测，不当成可用依赖。本项目路由只走 reverse-skill 总控。依据：`VALIDATION-REPORT.md` 第 38 行。

### 4.5 先修三个数，再融合

1. `README_zh.md:236` 的“175 条”改成 192（路由基准是 192 条）。
2. `skills/routing_zh.md:261` 的“63 tools”改成 78。
3. `docs/RELEASE-CHECKLIST.md:16` 的“25 项”改成 26。
4. 路由缺号写对：**缺的是 R42、R43 两个号，R44 存在**。固定提交的 `skills/config/routing.json:215,341` 明列 R44，路由优先级 45 项；R0–R41 共 42 条 + R44 + R45 + R46 共 3 条 = 45 条。R44 在原始清单里，本项目选不选用它是另一回事。缺号原因仓库里没说明，路由时不要猜，写进 MANIFEST。依据：`VALIDATION-REPORT.md` 第 31 行、`cases/validation/RECHECK.md` 第 9 行。
5. `.ps1` 和 `.sh` 两套启动脚本对不上，修法是：**两套都留着，不要统一成一套。** `.ps1` 是给 Windows 用的，`.sh` 是给 Linux/macOS 用的，v1.0 写“以 .ps1 为准”是错的。正确做法是：两套脚本装的工具清单要一样，逐项对一遍，缺哪个补哪个，补完后在 Windows 上跑 `.ps1`、在 Linux 上跑 `.sh` 各查一次。v1.0 说“`.sh` 缺 bkcrack、binaryninja”，报告里没写这个出处，第 0 步要先核实到底缺什么，不要照抄。

---

## 5. 交接格式做实（三个项目怎么衔接，写死）

三个项目之间只传下面 5 种东西，不传别的。每次交接都要落盘成文件，不要只在聊天里说。

### 5.1 案子包（reverse-skill 建案子时产出）

路径：`cases/<任务名>/`，里面必须有：

- `scope.md`：目标是什么、是什么类型（exe / apk / JS / .NET / Flutter）、哪些功能要复刻、哪些不做。
- `evidence/`：所有证据按编号存，文件名带 SHA-256（一种给文件算指纹的办法，文件变了指纹就变）。
- `timeline.md`：每一步几点、用了什么工具、结果是什么、失败了几次。
- `unknowns.md`：现在还不知道什么，不许把“不知道”写成“知道了”。

这是**人读**的案子包。上游检查器不读这些 Markdown；机器核验只引用同一案子里 R46 要求的 JSON 指针清单（见 5.3），两类文件都指向同一份原证据，不另抄一套账。依据：`cases/validation/notes-r46.md` 第 47 行。

### 5.2 REA 证据包（REA 分析完产出）

- 每个结论都要带证据 ID，带“已验证 / 未知 / 失败”三种状态之一。
- 静态事实不能直接当成“运行时也这样”，要写清这是静态看到的还是真跑出来的。
- 导出用命令行：`rea evidence-export <证据包> <规范化后的文件> --overwrite`，导入用 `rea evidence-import <文件>`。注意：这两个命令处理的是**已经存在的证据包**（规范化、导入导出），不是“从活动会话里现场抓一份新记录”。取出新记录和整理已有记录是两件事，记录时要分开写。
- 比对用命令行：`rea compare <左边证据> <右边证据>`，或 MCP 工具 `compare_functions`（跨版本比函数）、`compare_artifacts`（比产物清单）。
- **两级状态分开写，不要混：**
  - 「固定版本文档已核」：锁定提交 `4491c84…` 的 `docs/getting-started/cli.md:925–955` 记有导入、规范化导出和证据比对；`docs/reference/mcp-contracts.md:28–29、323、981` 记有 `compare_functions`、`compare_artifacts`、`export_evidence_bundle`、`compare_managed_members`。
  - 「本机运行已核」：本机 MCP 的 `tools/list` 实际列出这些工具名、并且调用成功，才算。没跑过就写「本机未实测」，不许把文档核验写成安装成功。
- `export_evidence_bundle`、`compare_managed_members` 在固定提交文档里有名字（见上），但本机是否真的发布、输入输出格式是什么，第 1 阶段列工具时核实；查不到就用命令行那套，不要发明工具名。依据：`VALIDATION-REPORT.md` 第 46 行。

### 5.3 复刻交接单（Seep 那一段结束、交给 R46 之前产出）

文件：`cases/<任务名>/reconstruction-handoff.md`。这是新加的人读文件，原版 Seep 没有，reverse-skill 也没有，所以字段、格式、示例、校验方法都在这里写死。

**这份 Markdown 不是 `check_handoff.py` 的输入。** 检查器读的是同一案子里的 JSON 指针清单（字段见上游 `skills/reconstruction/references/handoff-manifest.md:21–70`）；下面这张单子与 JSON 清单指向同一份原证据，不重复记两套账。依据：`cases/validation/notes-r46.md` 第 47 行。

**字段（一个都不能少，少一个就不许进 R46）：**

| 字段 | 格式 | 例子 |
|---|---|---|
| `target` | 目标名 + 版本 + 文件哈希 | `target: 小计算器 v1.2, sha256: 9f2c…` |
| `key_functions` | 表格：函数名 \| 地址 \| 输入 \| 输出 \| 干什么用 | `add \| 0x140001000 \| 两个整数 \| 一个整数 \| 把两个数加起来` |
| `key_algorithms` | 每条算法一段：怎么算、常量在哪、能不能本地复现 | `加法：直接相加，无常量，本地可复现` |
| `behavior_list` | 编号列表：用户做一步，程序先干什么、再干什么 | `1. 用户点“=” → 2. 程序读两个输入框 → 3. 调用 add → 4. 把结果写回界面` |
| `test_cases` | 至少 5 条：编号 \| 输入 \| 原版输出 | `TC1 \| 输入 2, 3 \| 原版输出 5` |
| `unknowns` | 列表：哪些还没看懂 | `不知道“历史记录”存在哪，没找到文件` |
| `source` | 每条上面写清证据 ID | `证据 E-003，函数 add 的反编译结果` |

**完整示例（照着这个格式写，不要只写半张）：**

```markdown
# 复刻交接单 — 小计算器 v1.2

target: 小计算器 v1.2, sha256: 9f2c…
source: 证据 E-001（REA 分析结果）、E-003（Seep exe-reverse 定位结果）

## 关键函数
| 函数名 | 地址 | 输入 | 输出 | 干什么用 |
|---|---|---|---|---|
| add | 0x140001000 | 两个整数 | 一个整数 | 把两个数加起来 |
| save_history | 0x140001120 | 一个整数 | 无 | 把结果写进历史记录 |

## 关键算法
- 加法：直接相加，无常量，本地可复现。证据 E-003。
- 历史记录：写到哪里还不知道，见 unknowns。

## 行为清单
1. 用户点“=” → 程序读两个输入框 → 调用 add → 把结果写回界面
2. 用户点“保存” → 调用 save_history

## 测试用例
| 编号 | 输入 | 原版输出 |
|---|---|---|
| TC1 | 2, 3 | 5 |
| TC2 | 0, 0 | 0 |
| TC3 | -1, 1 | 0 |
| TC4 | 999, 1 | 1000 |
| TC5 | 2.5, 3.5 | 未知、未验证（没测清是 6 还是 6.0） |

## 未知清单
- 不知道“历史记录”存在哪，没找到文件。
- 不知道小数是怎么处理的，TC5 的结果是 6 还是 6.0，没测出来。
```

**校验方法（这张单子怎么算合格）：**

1. 机器检查：跑 `skills/reconstruction/scripts/check_handoff.py`（不是 `tools/check_handoff.py`）。它只做机械检查：相对路径范围、原案上下文指针、文件 SHA-256、FR 映射唯一性、证据/义务/未知项指针；不运行目标、不联网、不判定内容真假。输出是 `machine_check_only`，`semantic_verification` 和 `target_execution` 均为 `not_performed`，`authorization` 为 `not_assessed`。跑过了只说明格式和指纹对上了，不说明内容对了。
2. 人工检查（第 0 步之后由执行智能体做，第 3 阶段验收时再做一次）：每个 `key_functions` 都要有证据 ID，每个 `test_cases` 都要在原版上真跑过一次，输出是抄下来的，不是猜的。
3. 机器检查过了、人工检查没过，这张单子还是不许进 R46。`semantic_verification="not_performed"` 的时候，不许说“已验证过”。

### 5.4 R46 复刻包（reverse-skill R46 产出）

Spec Kit 基线：**v1.3.0**。上游 `skills/reconstruction/references/spec-kit-workflow.md` 第 43 行以官方 Spec Kit v1.3.0 作为文档/源码核对基线；官方 v1.3.0 的 `pyproject.toml` 第 2–3、22 行定义包 `specify-cli`、包版本 `1.3.0`、命令入口 `specify`。这是**固定版本文档已核**，不是本机安装回执。安装时用 `specify` 命令，`integration`、`script` 参数按本机安装版的官方帮助选择；上游第 7 行写明本技能不硬编码宿主适配命令，v2.0 里写死的 `--integration codex` 不是上游原文。装完后 `.specify/` 和 `specs/` 要在项目里。R46 第 80 行的完整链路是 `constitution → specify → clarify → plan → tasks → analyze → implement → converge`，不要把它简写成五步。本机安装与集成是否跑通另记。

L0-L6 每一级定义（照抄上游 R46 `SKILL.md` 第 29–39 行，不用本项目简写替代）：

| 级别 | 上游 Claim 原文 | 上游 Minimum evidence 原文 | 算不算复刻完成 |
|---|---|---|---|
| L0 | target/protection triage | exact identity, format/protection observations and unknowns | 不算，只是接单和定范围 |
| L1 | readable decompilation/pseudocode | reproducible analysis output with addresses and limitations | 不算，只是分析进度 |
| L2 | key calls/data flow | Evidence-linked calls, data transformations and hypotheses | 不算，只是分析进度 |
| L3 | selected behavior model | observed inputs/outputs, states, error and boundary requirements | 不算，只是分析进度 |
| L4 | independent implementation passes core differential tests | frozen core scenarios executed against original and independent implementation | 算，通常交付线 |
| L5 | selected boundary/error/side-effect differential tests pass | required edge/state/regression surfaces pass with fresh proof | 算，比 L4 严 |
| L6 | near-original source recovery | source/symbol/build inputs and provenance support the claim | 算，须有原生来源与构建证据 |

L0–L3 是分析进度，L4/L5 是有限范围交付，L6 要有原生来源和构建证据，不能只从反编译推断（R46 第 39–41 行）。

**四种证据分开记，不许互相顶替：**
1. 结构比对（函数或产物清单相似）：只能说明“看起来像”，不能替代运行行为。
2. 双侧行为对照（原版与独立实现用同一组输入、同一环境分别跑）：L4/L5 的核心。
3. 独立运行（新程序脱离原程序能自己跑）：单独一条证据。
4. 比较器自检（故意弄坏一个变体，检查器能发现差异）：这是 R46 第 90 行的错误变体测试，只证明比较器有效，不单独等于 L5。

只承诺“选定范围内的有限等价”，不承诺“源码完全恢复”或“全局等价”。这是 R46 自己写的承诺范围，不要夸大。

### 5.5 验收报告

- 结构比对：REA 的 `compare_functions` / `compare_artifacts` 结果，单独一节，写明这是结构层面。
- 行为对照：原版与独立实现同一组输入的实测输出，逐条列，带证据 ID 和时间。
- 独立运行：新程序脱离原版的运行记录。
- 比较器自检：故意做坏的变体是否被检查器抓到，单独记。
- reverse-skill 的 case-review 哈希校验。
- 结论只能写三档：通过 / 部分通过（列出哪几项没过）/ 不通过。不许写“基本完成”“大体上可以”“应该没问题”这种模糊词。结构相似、抓到一个坏变体、五条只覆盖正常输入，都不能单独构成完整行为验收。

---

## 6. 第 0 步：验证（必须先做，不验证不许融合）

**限时：3 小时。超过 3 小时还没出报告，就停下，交一份半成品报告，写清做到哪了、卡在哪。不要为了“读完”一直读下去。**

### 6.1 先补读总控和 R46（这一步是第三方评审要求加的，不能跳过）

之前三份拆解报告里，总控 `skills/SKILL.md` 和复刻 `skills/reconstruction/SKILL.md` 这两份是明确没读过的（B 路报告第 6 行、第 135 行写了“不在本路范围内，未读”）。整个融合的核心就是这两份，没读过就谈融合，证据链是断的。所以第 0 步第一件事就是补读。

做法：

1. 按第 2 节的提交号把 reverse-skill 拉下来，全文读 `skills/SKILL.md` 和 `skills/reconstruction/SKILL.md`，不要抽读。
2. 交出两份逐条笔记，文件放在 `cases/validation/` 里：
   - `notes-router.md`：总控这份，每一条写“原文说什么、我理解成什么、和 v2.0 第 1 节的顺序有没有冲突”。
   - `notes-r46.md`：R46 这份，抄出 L0-L6 每一级的原文定义，抄出 Spec Kit 的版本和集成方式，抄出 `check_handoff.py` 到底检查什么、不检查什么。
3. 如果读完发现 v2.0 的顺序错了，不要悄悄改顺序。写进 VALIDATION-REPORT，写清“哪里错了、证据是哪一行、建议改成什么”，等用户批了再改。

### 6.2 再核对 15 个衔接问题（逐项打勾，打不上的写清楚）

下面 15 条都是彻底拆解时已经核对过的，融合时逐项复核。打勾的意思是“我自己重新核实过，确认是这样”；打不上的写“没法确认，原因是……”。

| # | 问题 | 出处 | 融合时怎么处理 |
|---|---|---|---|
| 1 | Seep 不支持 Codex，CHANGELOG 明确写了只支持 Pi 和 DeepSeek Harness | Seep CHANGELOG [Unreleased] | 不装 Seep MCP，只抽技能文件当参考 |
| 2 | Seep 的 `lab:` 门和 G-Auth 门，和 reverse-skill 的授权门是两套 | Seep AGENTS.md、softseep SKILL.md | 只留一套：reverse-skill 的 scope + `auth.status`，Seep 的门不要另起 |
| 3 | Seep 和 reverse-skill 都有总控，都会抢路由 | 两份报告 | 只留 reverse-skill 当总控，softseep 不当总控 |
| 4 | Seep 知识库数字打架：294 / 316 / 183+ / 289+ / 69 / 178+ / 197，实测正文 195 篇 | Seep C 路报告 | 不要引用“294 篇”，写“实测 195 篇正文” |
| 5 | Seep 的 `Tool/mcp/Tool/reverselab/` 和 `Tool/upstream/open-reverselab/` 是两份不同步的快照 | Seep C 路，blob 哈希比对 | 两份都不要，工作台实际读的是旧的那份，容易错 |
| 6 | Seep 好多构建脚本按提交状态跑不起来（缺文件、路径错） | Seep B 路，14 个案例 | 不要直接跑它的 build.ps1，先核对文件在不在 |
| 7 | reverse-skill 的 `.ps1` 和 `.sh` 两套启动脚本内容对不上 | reverse-skill 彻底报告 | 两套都留着，逐项对清单，缺哪个补哪个（见第 4.5 节第 5 条） |
| 8 | reverse-skill 数字错误三处；路由缺 R42、R43，R44 存在 | 彻底报告 + 固定提交 `skills/config/routing.json:215,341` | 先改三处数字；缺号只写 R42、R43，R44 不写成缺号，原因不猜 |
| 9 | reverse-skill 硬目标方法全是“未复现”，27 份带“本方状态”的参考资料全写“未复现” | reverse-skill C 路 | 不要把“方法可信”当成“已经跑通过”，R46 验收必须真跑 |
| 10 | REA 工具数没有 6.9.0 的仓内精确数，最接近是 2026-11-06 的 241 个；SKILL.md 是 674 行不是 1029 行 | REA 彻底报告 | 不要引用“260 个工具”“1029 行”这两个旧数字 |
| 11 | REA 在 Windows 上 Ghidra 是实验性、只读 27 个操作；Hopper 在 Windows 上没有自动安装 | REA 彻底报告 | Windows 目标先走 JS、.NET、静态分析这条路，原生硬目标要先在案子包里写清用的哪个引擎 |
| 12 | REA 和 reverse-skill 的证据口径不一样：REA 是保守的“不知道就是不知道”，reverse-skill 是“证据-发现-路径”链 | 两份报告 | 统一用第 5.2 节的三档状态：已验证 / 未知 / 失败 |
| 13 | 锁定提交 `ce67509…` 的 CHANGELOG 用候选版措辞，但上游已有正式 `v1.9.0`，tag 指向 `7cc3109…` | CHANGELOG + GitHub Release `v1.9.0` | MANIFEST 同时写“锁定提交 ce67509”和“正式 tag v1.9.0 → 7cc3109”；不自动跟 tag，按第 10 节评估 |
| 14 | Seep 的 Aotopsy 只支持 Flutter/Dart 2.10-3.13，字段名 97-99% 缺失 | Seep C 路 | 只在 Flutter 目标用 Aotopsy，限制写进未知清单，不要夸大 |
| 15 | Seep 的 `master-route.ps1` 读的是 `Tool/config/routing.json`，但仓库里没有 `Tool/config/`，唯一 routing.json 在 `Tool/scripts/routing.json`；它引用的 `verify-routing-coherence.ps1`、`test-routing.ps1`、`extract-summaries.ps1`、`skills/MASTER-ROUTING.md` 不存在；`check_routing.py` 在被抽取的 `apkseep`、`exe-reverse` 目录里没有，但 `Tool/upstream/` 两份镜像各有一份 | Seep A 路、D 路 + 固定提交完整文件树 | 不直接跑 `master-route.ps1`；镜像里的 `check_routing.py` 未验证可运行，不当依赖。路由只走 reverse-skill 的总控（本轮第三个项目记为以后再说） |

### 6.3 第 0 步的出口（必须全过才算通过）

- 三个 HEAD 都对上第 2 节的表。
- 15 个问题里，能确认几个就写几个，确认不了的必须写原因，不许用凑数来过关。
- 对最终顺序没有根本性反对；如果认为 Seep 先或 REA 先更好，必须在报告里写出证据和打分，不能悄悄换顺序。
- 交出 `VALIDATION-REPORT.md`，写清：v2.0 哪里对、哪里错、哪里不同意、建议怎么优化。只改报告，不改代码。等用户看完说“可以开始”，再进第 1 阶段。

### 6.4 复核与二次优化规则（这一节是用户最新加的，优先于其他写法）

前面写方案的人承认：读取不够完整，没逐行读完所有文件。所以拿到这份方案的智能体，必须自己再做一次独立复核，不要盲信这份方案。

做法：
1. 先按 6.1、6.2 把总控、R46 和 15 个问题重新核对一遍，交出你自己的思考：你是怎么理解这个顺序的、你觉得哪里合理、哪里不合理、你的依据是哪一行。
2. 再单独写一份 `REVIEW-2.md`，只写三件事：这份方案哪里可以优化、为什么要优化、优化后对这个聚合项目到底有什么用。每一项优化都要写清：现在有什么问题、不改会怎么样、改完能省多少时间或少出多少错、改的风险是什么。
3. **不要为了优化而优化。** 只有同时满足下面三条，才算“真的有用”，才能提出来改：
   - 能让链路更通、更少返工，或者能让验收更严、更少假通过；
   - 改动小、能回滚，不会把已经定死的顺序、交接格式、完成标准推翻；
   - 有报告或原文做依据，不是凭感觉。
   不满足三条的想法，写进 REVIEW-2 的“想过但不建议改”那一节，不要动手改。
4. 优化要用户批了再改。REVIEW-2 交上去，等用户说“改这一条”你再改那一条，用户没说的，一条都不许改。不要自己一边复核一边改方案，不要把复核报告和改方案混在一起。
5. 如果复核完你觉得这份方案不用改，也要明说“不用改，原因是……”，不要为了显得认真硬找几个优化点。

---

## 7. 分 5 个阶段执行（每阶段单独跑、单独验收）

**不要一次连续跑 10 个小时。** 上次那个项目就是这样没完的：没有分段，没有出口，智能体越跑越偏，上下文越压越糊。

**总时间：** 第 0 步验证完再重新估算。不要写拍出来的总小时数。下面每阶段给的是“最长做到多久就停下交半成品”的上限，不是“需要多久”的估计。到了上限没做完，就停下，交半成品，写清做到哪了、卡在哪。

本轮范围：第 1–3 阶段只做 REA 与 reverse-skill 两个项目；Seep 的签出、抽取和调用记为「以后再说」，不阻塞、不算本次失败。依据：用户 2026-11-20 指令与 `cases/validation/SAFE-V4-STOP.md` 第 11 行。

| 阶段 | 做什么 | 上限（到了就停） | 出口（必须有文件才算完） | 做不完怎么办 |
|---|---|---|---|---|
| 0 | 验证方案（第 6 节） | 3 小时 | `VALIDATION-REPORT.md` + 两份逐条笔记 | 超时就交半成品，停下 |
| 1 | 拉取锁定 + 瘦身 reverse-skill + 抽 Seep | 2 小时 | `lifecycle/MANIFEST.yaml` 已填实 + 删完后的文件清单 | 删不完就只做一半，写清删到哪了 |
| 2 | 接线：REA MCP + 总控 + 复刻交接单模板 | 2 小时 | 接线测试通过的日志 + `reconstruction-handoff.md` 模板 | 接不通就停下，不要硬写代码绕过去 |
| 3 | 第一个小目标全流程测试 | 3 小时 | 小目标的案子包 + 5 个测试用例结果 + 验收报告 | 跑不过 L4/L5 就回滚，写清失败原因 |
| 4 | 收尾：补 lifecycle、写 README、定版 | 1 小时 | lifecycle 文件全齐 + README 能照着跑 | 缺文件就列清单，不要说“差不多齐了” |

**每阶段的做法：**

### 第 1 阶段：拉取锁定 + 瘦身 + 抽 Seep

```bash
# 三个仓库都用子模块，固定在第 2 节的提交号，不要用 latest
git submodule add https://github.com/morluto/rea engine/rea
git submodule add https://github.com/gthubtom1/reverse-skill upstream/reverse-skill
git submodule add https://github.com/angusdevgo/Seep-Reverse-Lab upstream/seep
cd engine/rea && git checkout 4491c84c82140a43fa12390b727840a433875ba8 && cd ../..
cd upstream/reverse-skill && git checkout ce675096e6a2cd4789a76f9bd618feddc2b6f333 && cd ../..
cd upstream/seep && git checkout 1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e && cd ../..
```

然后按第 4 节瘦身 reverse-skill、抽 Seep 的 5 样、修三个数字。删完后数一遍：`core/skills/` 下应该只剩第 4.1 节的 15 个，不是 45 个。跑一次 `check_handoff.py`，确认机器检查还能跑（它只是机器检查，不代表内容对了）。

### 第 2 阶段：接线

1. 按第 3 节装 REA 的 MCP，一次只装一个，装完按第 3.3 节两层检查查完再装下一个。
2. 把总控技能复制到 `.agents/skills/`、`.claude/skills/`、`.pi/skills/` 三个位置（源头是 `core/`，不要直接改源头）。
3. 写一个最小的接线测试：让总控发一个任务给 REA，REA 返回一个带证据 ID 的结果，总控能把它存进 `cases/` 的 evidence 里。跑不通就停下，不要往下走。
4. 写好 `cases/<任务名>/reconstruction-handoff.md` 的模板（见第 5.3 节），没有模板不许进下一阶段。

### 第 3 阶段：第一个小目标测试（必须做，不做不算融合成功）

不要只测一个 100 行的小玩具，要测第 11 节的 3 个样本：样本 1 简单、样本 2 中等、样本 3 困难（反调试、加密、UPX 加壳）。样本 1 和样本 2 必须过，样本 3 争取过。每个样本按第 1.2 节的执行顺序完整跑一遍：

1. reverse-skill 建案子、写 scope
2. REA 分析、导出证据包
3. 如果撞上许可证校验、加壳，才叫 Seep 提取件，产出复刻交接单；没撞上就跳过这一步
4. R46 写行为模型、写规格、Codex 写新程序
5. REA 比对原版和新版，case-review 校验

验收标准（必须全过才算成功）：
- 新程序能跑起来，不是只写了代码
- 至少 5 个测试用例，原版和新版输出一致，带新鲜证据
- 故意弄坏一个变体，检查器能发现
- unknowns.md 里列出的未知项都写清了，没有假装知道

做不到就不要说“融合成功了”。把失败原因写进 DECISION-LOG，再修，不要硬说成功。

### 第 4 阶段：收尾

1. 按第 10 节建好 lifecycle 文件。
2. 把这次融合的实际文件清单、版本号、删了什么、改了什么，都写进 MANIFEST。
3. 在 README 里写清：怎么跑第一个小目标、出了问题先看哪里。

---

## 8. 防偏移机制（针对“上下文压缩后越跑越偏”）

智能体连续跑，上下文会被压缩，压缩几次就忘了最初的顺序和验收标准，开始钻牛角尖。所以这样防：

1. **文件是真理，聊天不是。** 每次做完一步，都要把结果写进文件（MANIFEST、DECISION-LOG、案子包）。下次开始时，先读文件，不读聊天记录。文件里没有的，就当没发生过。
2. **计划是冻结的。** v2.0 就是冻结版。执行中不许悄悄改顺序、改验收标准、加新模块、开分支、开 PR。想改，就写一份 `CHANGE-REQUEST.md`，写清“想改什么、为什么、证据是什么”，等用户批了再改。
3. **一个任务只做一件事。** 每个阶段只派一个小任务，不要让一个智能体同时管路由、分析、复刻、验收。主智能体只负责按阶段推进，具体干活分给子任务，做完就回收。
4. **失败两次就停。** 同一个命令、同一个方法失败两次，不许原样再试第三次。必须换方法，或者停下写清楚。原样重试是跑偏最常见的样子。
5. **不许用“差不多”交差。** 验收只能写“通过 / 部分通过（列出哪几项没过）/ 不通过”。出现“基本完成”“大体上可以”“应该没问题”这种词，就当没验收过。
6. **每阶段结束要用户看一眼。** 每阶段结束交一次文件，用户说“进下一段”再进。用户不说话，就停在那，不要自己往下冲。
7. **每 45 分钟一个检查点。** 不管做到哪，都要把现在的状态写进 `lifecycle/DECISION-LOG.md`：做到哪一步、改了什么文件、测试结果是什么、下一步是什么。写不出来就说明已经偏了，停下。

---

## 9. 最终完成标准 10 条（少一条都不算成功）

1. 三个仓库都锁定在第 2 节的版本，MANIFEST 里写得和实际一致。
2. reverse-skill 瘦身完成：25 个无关模块已删（B 路无关 27 个里留了 case-review、docs-generator），7 个间接模块已按第 4.3 节删掉，CTF 和 pentest-tools 已删，三处数字错误已改，`.ps1`/`.sh` 两套脚本的清单已对齐。
3. Seep 只抽了第 4.4 节的 5 样，整套工作台、upstream、cases、webseep 都没带进来。
4. Codex 里 REA 的 MCP 能调通，reverse-skill 总控能调通，两者能互相传证据文件（第 3.3 节第二层检查过了）。
5. `reconstruction-handoff.md` 模板已建好，有关键函数、行为清单、测试用例、未知清单四项，字段齐全。
6. 第一个小目标完整跑过一遍：建案子 → REA 分析 →（如有硬骨头）Seep 提取件 → R46 → REA 比对验收。
7. 新程序能跑起来，至少 5 个测试用例原版和新版输出一致，带新鲜证据。
8. 故意弄坏一个变体，检查器能发现差异（证明验收不是摆设）。
9. unknowns.md 里列出的未知项都写清了，没有假装知道。
10. lifecycle 文件全齐，README 能让一个没看过方案的人照着跑第一个小目标。

**只要有一条没过，就不要说“融合成功了”。** 写清哪条没过、为什么没过、下一步修什么。这比硬说成功重要得多。

上次 20-30 小时没完成，很可能就是没有这 10 条。没有完成标准，智能体就不知道什么时候停，只能一直“优化”下去。这次先把标准定死，时间自然就收得住。

---

## 10. 生命周期（以后怎么快速更新，不用每次都从头读三个项目）

### 10.1 本地是自己的，上游是别人的，分开管

- **本地融合项目是自己的：** `reverse-fusion-v2` 是你自己的项目，里面的 `core/`（瘦身后的总控）和 `specialist/seep-extract/` 是你复制、改过的，归你管。
- **上游是别人的：** REA、reverse-skill、Seep 是别人的，用子模块、固定提交引用，不直接改他们的代码。
- **这样以后更新才快：** 上游变了，你只需要对照 MANIFEST 看“变了什么、影响我用的那几块吗”，不用重新把三个项目从头读一遍。
- **不要做的事：** 不要把上游整仓复制进来就当成自己的，不要用 `latest` / `main` 这种会自己变的版本，不要把三个项目的文件混在一个文件夹里分不清谁是谁的。

### 10.2 lifecycle/ 文件夹里只有 5 个文件（不要重复抄两遍）

v1.0 里 MANIFEST 和 PINNED-VERSIONS 是同一张表抄了两遍，以后改一处、忘一处，就会打架。v2.0 只留一份：

```
lifecycle/
├── MANIFEST.yaml                  # 唯一的一份：锁定版本 + 用了哪些功能 + 不用哪些 + 顺序
├── USED-FUNCTIONS.md              # 我们到底用了上游的哪些功能，精确到文件和函数名
├── DECISION-LOG.md                # 每次决定为什么这样接、为什么删那一块
├── UPDATE-CHECK.md                # 每次检查更新的记录（日期、结果、决定）
└── UPDATE-REPORT-TEMPLATE.md      # 以后每次更新报告的模板（照着填）
```

#### MANIFEST.yaml（模板，融合成功后照实填）

```yaml
fusion_version: v2.1
fusion_date: 2026-11-20
goal: 白话 in Codex -> 分析软件 -> 重做功能一样的版本

pinned:
  rea:
    repo: morluto/rea
    version: 6.9.0
    commit: 4491c84c82140a43fa12390b727840a433875ba8
    used_as: engine_only
  reverse-skill:
    repo: gthubtom1/reverse-skill
    version: 1.9.0
    commit: ce675096e6a2cd4789a76f9bd618feddc2b6f333
    used_as: router_and_reconstruction
  seep:
    repo: angusdevgo/Seep-Reverse-Lab
    version: 1.15.0
    commit: 1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e
    used_as: specialist_extract_only

execution_order:
  - reverse-skill
  - rea
  - seep-extract-if-hard-target
  - reverse-skill-r46
  - rea-compare-and-case-review

install_order:
  - rea
  - reverse-skill
  - seep-extract

do_not_use:
  - seep_mcp_server_as_main
  - seep_lab_gate_standalone
  - seep_upstream_duplicates
  - reverse-skill_unrelated_modules
  - ctf_sandbox_orchestrator
  - pentest_tools_src_hunter
```

#### USED-FUNCTIONS.md（按“文件 + 函数名 + 用来干什么”写，不要写空话）

v1.0 的 USED-FUNCTIONS 只有 10 行，每行只写“用：证据、比对”这种空话，根本没做到“精确到文件和函数”。v2.0 按下面这个格式重写，融合时逐项填实：

| 上游 | 文件 | 函数名 / 工具名 | 用来干什么 | 固定版本文档已核 | 本机运行已核 |
|---|---|---|---|---|---|
| REA | `SKILL.md`（674 行） | — | 证据、比对、义务清单的写法 | 是 | 未实测 |
| REA | `docs/reference/mcp-contracts.md:28–29` | `compare_functions` | 跨版本比函数 | 是 | 未实测 |
| REA | `docs/reference/mcp-contracts.md:323` | `compare_artifacts` | 比产物清单 | 是 | 未实测 |
| REA | `docs/getting-started/cli.md:925–955` | `rea evidence-export` / `rea evidence-import` / `rea compare` | 规范化、导入导出、比对已有证据包 | 是 | 未实测 |
| REA | `docs/reference/mcp-contracts.md:981` | `export_evidence_bundle` | 导出证据包 | 是 | 未实测（本机工具列表待核实） |
| REA | `docs/reference/mcp-contracts.md:981` | `compare_managed_members` | 比托管成员 | 是 | 未实测（同上） |
| reverse-skill | `skills/SKILL.md` | 总控 | 路由、建案子、记证据账 | 是（已补读，见 `cases/validation/notes-router.md`） | 未实测 |
| reverse-skill | `skills/reconstruction/SKILL.md` | R46 | L0-L6、L4/L5 验收 | 是（已补读，见 `cases/validation/notes-r46.md`） | 未实测 |
| reverse-skill | `skills/reverse-engineering/SKILL.md` | 第 5-6 步 | 分析完交给重建的衔接点 | 是 | 未实测 |
| reverse-skill | `skills/js-reverse/SKILL.md` | Rebuild 阶段 | 在 Node 里把签名算法本地复现跑通 | 是 | 未实测 |
| reverse-skill | `skills/reconstruction/scripts/check_handoff.py` | 机械检查 | 只查引用、指纹和格式，不运行目标、不联网 | 是 | 未运行 |
| Seep | `Tool/skill/exe-reverse/SKILL.md` | G1-G5 门 | Windows PE 分析 | 是 | 未抽取（以后再说） |
| Seep | `Tool/skill/apkseep/SKILL.md` | G1-G4 门 | Android 分析 | 是 | 未抽取（以后再说） |
| Seep | `Tool/skill/client-license-validation-bypass/SKILL.md` | G0-G6 门 | 许可证校验手册 | 是 | 未抽取（以后再说） |
| Seep | `Tool/aotopsy/aotopsy.exe` | Aotopsy | 只用于 Flutter/Dart AOT 还原 | 是，限制见第 4.4 节 | 未抽取（以后再说） |
| Seep | `Tool/skill/safe-skills/mcp-js-reverse-playbook/SKILL.md` | Observe → Capture → Rebuild → Patch → DeepDive | JS 签名链路本地复现 | 是 | 未抽取（以后再说） |

**两栏必须分开填：** 「固定版本文档已核」只说明锁定提交里有这份资料；「本机运行已核」必须有本机命令输出或工具列表作证。两者不一致时以本机结果为准，并把差异写进 DECISION-LOG。

**这份清单就是以后快速更新的关键。** 上游更新了，智能体只需要看“更新的那几行在不在这份清单里”，在，就要评估；不在，就直接写“不影响我们”，不用全读。

### 10.3 以后怎么检查更新（先抽查最近 20 个提交）

**给以后智能体的原话指令（直接复制去用）：**

> 你是更新检查员，不是融合员。先读 `lifecycle/MANIFEST.yaml` 和 `lifecycle/USED-FUNCTIONS.md`，弄清我们现在锁了哪个版本、用的是上游的哪些功能。
> 再去读这三个仓库的最新提交和 CHANGELOG / Release：morluto/rea、gthubtom1/reverse-skill（也要看它基于的 zhaoxuya520/reverse-skill 有没有变）、angusdevgo/Seep-Reverse-Lab。
> **先只抽查最近 20 个提交。** 20 个看不完、或者 20 个里就有影响我们的变化，就停下，先交一份抽查报告，不要一次把几个月的提交全读完。
> 然后对照 USED-FUNCTIONS 清单，逐项判断：变了的那几行，在不在我们用的清单里？
> 最后交一份报告，格式按 `lifecycle/UPDATE-REPORT-TEMPLATE.md`，不要直接改代码、不要直接拉取、不要自动合并。等用户说“要跟”你再动手。

**检查步骤：**
1. 读 MANIFEST，记下三个锁定提交号。
2. 用 `git log <锁定提交>..HEAD` 看最近 20 个提交，列出清单。
3. 对照 USED-FUNCTIONS，标出“影响我们”和“不影响我们”。
4. 对“影响我们”的每一条，写：变了什么、原来我们是怎么用的、现在要怎么改、风险多大。
5. 打分，见 10.4。
6. 把报告存到 `lifecycle/UPDATE-CHECK.md`，附上日期，不要覆盖以前的记录。

### 10.4 值不值得跟？打分标准（风险方向改对了，高风险直接判不跟）

每条变化打 0-2 分，三项加起来。注意：三列的方向现在是一致的，都是“分数越高越好”，v1.0 里风险那一列是反的，已经改过来了。

| 维度 | 2 分 | 1 分 | 0 分 |
|---|---|---|---|
| 影响我们吗 | 在 USED-FUNCTIONS 清单里，直接影响 | 间接影响，比如依赖的工具变了 | 不在清单里，不影响 |
| 是修 bug 还是加功能 | 修了我们已经踩过的坑（比如构建脚本、路由配置） | 加了我们正好需要的新功能 | 只是改文档、改数字、加了无关模块 |
| 风险低吗 | 改动小、能回滚、有测试 | 改动中等，要重新跑小目标测试 | 改动大、会断开衔接、总控换了、MCP 工具名全变了 |

- **总分 5-6 分：值得跟。** 按 10.5 的适配步骤做。
- **总分 3-4 分：可跟可不跟。** 写清利弊，让用户决定，不要自己决定。
- **总分 0-2 分：不跟。** 写进 UPDATE-CHECK，说明为什么不跟，下次再看。
- **硬规则：风险那一列得了 0 分（高风险、会断开衔接），不管总分是多少，直接判“不跟”。** 不要让一个高风险更新靠另外两项的高分混过去。

**不跟的几种情况（直接写“不跟”，不要犹豫）：**
- 只改了文档、徽章、数字，没有改我们用的功能
- 加了和复刻无关的新模块（比如新的渗透、CTF、云安全）
- 改动会断开现在的衔接（比如 MCP 工具名全变、路由号全变）
- 新版本只是候选版、预发布，没有正式 tag

### 10.5 值得跟的时候，怎么适配更新（不是直接拉下来就能用）

更新不是直接 `git pull` 就行，因为上游一改，三个项目之间的衔接可能就断了。要按下面这个顺序做：

1. **先备份：** 用 git 打一个分支或标签，比如 `backup-2026-12-01`，不要只复制文件夹。复制出来的备份以后分不清，分支和标签能查到是哪一天、从哪个提交备的。
2. **只更新变了的那一块：** 比如只有 REA 变了，就只更新 `engine/rea` 那个子模块，不要同时更新另外两个。一次只动一个，动完测完再动下一个。
3. **对照 USED-FUNCTIONS 改接线：** 上游改了函数名、改了文件路径，就在我们的接线处改，不要去改上游的代码。改完把 USED-FUNCTIONS 和 MANIFEST 一起更新。
4. **跑第 7 节第 3 阶段那个小目标测试：** 必须重新跑一遍 L4/L5 验收，5 个测试用例全过、故意弄坏的变体能被发现，才算更新成功。跑不过就回滚到备份，不要硬修。
5. **更新生命周期文件：** MANIFEST 里的版本号和提交号改成新的，DECISION-LOG 写清“这次跟了什么、为什么跟、改了哪里、测试结果是什么”，UPDATE-CHECK 写清日期和决定。
6. **不要做的事：** 不要一次更新三个项目，不要把上游的新模块顺手带进来，不要把“检查通过”写成“已经验证过”。

### 10.6 UPDATE-REPORT-TEMPLATE.md（以后每次报告照着填）

```markdown
# 更新检查报告 - 日期：____

## 1. 现在锁定的版本
- REA：6.9.0 / 4491c84...
- reverse-skill：1.9.0 / ce67509...
- Seep：1.15.0 / 1ea9399...

## 2. 上游这段时间变了什么（先只列最近 20 个提交）
| 仓库 | 新版本/提交 | 变了什么 | 在不在我们用的清单里 |
|---|---|---|---|
|  |  |  | 是 / 否 |

## 3. 对我们的影响
- 影响我们的有几条，每条写：原来怎么用、现在要怎么改、风险多大
- 不影响我们的有几条，一句话带过

## 4. 打分
- 影响：__ / 2
- 价值：__ / 2
- 风险低吗：__ / 2（0 分 = 高风险，直接判不跟）
- 总分：__ / 6
- 结论：值得跟 / 可跟可不跟 / 不跟

## 5. 如果跟，要怎么适配（分步写，不要只写“拉下来”）
1. 先备份到哪个分支/标签
2. 先更新哪一块，后更新哪一块
3. 接线要改哪里
4. 跑哪个小目标测试，验收标准是什么
5. 回滚条件是什么

## 6. 如果不跟，为什么
- 一句话原因

## 7. 需要用户决定的事
- 要不要跟？（只问这一句，不要问一堆）
```

---

## 11. 测试样本：3 个，由易到难（第 3 阶段用这 3 个，不用再找）

用户要求加的：不要只测一个 100 行的小玩具，要测 3 个真样本，一个简单、一个中等、一个难的，难的要有反调试、加密、混淆、加壳。这样做完才算一个完整的、符合心意的聚合版。

样本来源：crackmes.one。这个网站就是专门给人练逆向用的，上面有几千个别人上传的小程序，按难度、语言、平台分好类，下载来拆是合法的学习用途。下载要注册账号，解压密码永远是 `crackmes.one`。不要去网上随便下一个来路不明的 exe，不要用真实商业软件当测试样本。

**第 0 步就要把 3 个样本定下来，写进 `cases/samples/MANIFEST.md`，写清每个样本的网址、名字、难度、文件哈希值。** 下面给的是类型和例子，不是死命令：如果下面某个具体样本下不到了，就在 crackmes.one 上按同一个难度、同一个类型换一个，换完把新样本的网址和哈希写进 MANIFEST，不要硬找一个已经下架的。

| 样本 | 难度 | 是什么样的程序 | 用来测什么 | 必须过吗 |
|---|---|---|---|---|
| 样本 1：简单 | 难度 1-2 | 一个小程序，输密码，程序用 XOR（一种很简单的加密，就是把每个字节和一个固定数字做异或）算一下再比对，没有反调试、没有加壳、没有加密字符串。比如 crackmes.one 上“Yuri's Simple Keygen”这类，或“awakx's simpleCrackme”这类 | 总控能不能带路、REA 能不能看懂、R46 能不能重做一个 | 必须过。过不了，融合就不算成功 |
| 样本 2：中等 | 难度 2-3 | 一个带许可证检查的小程序，密码不是明文，要经过自定义哈希或多步变换才能算出来，可能带一点字符串混淆。比如 crackmes.one 上难度 2-3 的 keygen 类 | 关键算法能不能抠出来、能不能在本地复现 | 必须过。过不了，写清卡在哪一步 |
| 样本 3：困难 | 难度 4 | 带反调试、加密字符串、UPX 加壳的程序。反调试就是程序会检查“有没有人在调试我”，比如 `IsDebuggerPresent`、PEB 检查、计时检查；加密字符串就是要用的字平时是加密的，跑起来才解密；UPX 加壳就是程序被压过，静态看不到真代码，要先脱壳。比如 hasherezade 那种带反调试函数的 crackme，或 crackmes.one 上难度 4、带 anti-debug、UPX 标签的 | Seep 提取件有没有用、脱壳和反调试那一段能不能过、动态那一步能不能接上 | 争取过，不过也算一种结果。过不了不算融合失败，但必须写清卡在哪、是哪个工具不行、以后要补什么 |

**怎么测（3 个样本都按同一套来）：**
1. 每个样本单独建一个案子：`cases/sample-1/`、`cases/sample-2/`、`cases/sample-3/`，不要混在一个案子里。
2. 每个样本都按第 1.2 节的顺序完整跑一遍：建案子 → REA 分析 →（难的才叫 Seep）→ R46 重做 → REA 比对验收。
3. 每个样本都要 5 个测试用例：原版输入什么、输出什么，新版输入什么、输出什么，两边对得上才算过。
4. 每个样本都要写 `unknowns.md`，没看懂的地方写清，不要假装知道。

**第 3 阶段的验收改成这样：** 样本 1 和样本 2 必须过，才算融合成功；样本 3 过了最好，没过要写清失败原因和下一步，不许说“基本成功”。第 9 节的完成标准第 6、7 条，按这个改。

---

## 12. 停下规则 + 冻结声明（执行智能体必须遵守）

### 11.1 停下规则

遇到下面任何一条，先停下，写清楚问题，不要自己猜、不要硬往下做：

1. 三个锁定提交号对不上第 2 节的表。
2. 上游改了我们用的函数名、文件路径、MCP 工具名。
3. 小目标测试跑不过 L4/L5。
4. Seep 的新版本又加了 `lab:` 门或者删了 Codex 支持（如果以后它支持 Codex 了，也要先报告，不要直接换）。
5. reverse-skill 的 R46 流程变了，L4/L5 标准变了。
6. 同一个命令、同一个方法失败两次，不要原样再试第三次。
7. 到了阶段上限还没做完，不要硬撑，先交半成品。

**停下时要写：** 现在做到哪一步、卡在哪、已经查到什么、需要用户决定什么。不要只写“失败了”。

### 11.2 冻结声明

- 这份文件就是最终版，版本号 v2.0，日期 2026-11-20。
- 执行中不许悄悄改顺序、不许加模块、不许开分支、不许开 PR、不许把方案拆成多个版本。
- 想改，先写 `CHANGE-REQUEST.md`，写清“想改什么、为什么、证据是什么”，等用户批了再改。改完后整个文件版本号才动，旧版本留着，不要覆盖。
- 以前所有的 v1.0、v1.1、补丁，以这份为准，和这份打架的地方，以这份为准。

---

*依据：REA 彻底拆解（9,357 文件，6.9.0，SKILL.md 674 行）；reverse-skill 彻底拆解（675 真实文件，45 路由 R0-R46，缺 R42、R43，27 份参考资料全写“未复现”）；Seep 彻底拆解（4,942 文件，1.15.0，38 工具，14 案例，知识库实测 195 篇）；第三方评审（顺序认同，5 条必须改，其中第 4 条按用户要求不执行）；成熟项目安装写法（anthropics/skills、Codex、github/spec-kit、Pi，2026-11-20 查）。*
*老实说明：没有逐字逐行读完每一个文件。REA 一个 `src/` 就有 1,323,777 行，Seep 有 4,942 个文件，reverse-skill 有 500 个 .md。做的是“文件树全清点 + 关键文件全读 + 大文件结构化核对 + 明确列出没读的部分”。没读的部分，第 0 步补读。*
