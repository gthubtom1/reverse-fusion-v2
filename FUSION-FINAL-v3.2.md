# 融合最终方案 v3.2（最终版：修衔接 + 共享文件夹部署 + 独立测试员）

> 版本：v3.2，日期 2026-11-20，冻结。v2.1、v3、v3.1 全部冻结不动，留着当底子。v3.2 只在 v3.1 上改下面这张表里列的东西，不改目标、不改锁定版本、不改三种模式。
> v3.1 现在的真实进度（执行方已做到 R2，2026-11-20 06:28，提交 `81fc67e`“V3.1 R2”；R3–R8 一个都没做）：v3.2 不是从头重做，是从 R2 之后继续做，R1、R2 的成果留着，R2 里发现错的地方按下面改。

## 改动清单（先看这张表，再看正文；v3.1 对照）

| # | 改了什么 | 为什么改 | 证据 |
|---|---|---|---|
| D1 | 新增第 11 章：共享文件夹部署。1 个公共文件夹 + 3 根细指针 + 1 个配置文件 | 仓库里根目录没有 CLAUDE.md、没有 .claude/skills/，.mcp.json 写死 D:\Tools\ 路径，换电脑就坏 | 仓库 HEAD `81fc67e` 实测 |
| D2 | 新增第 12 章：独立测试员 R9。建造者 ≠ 测试员，Pi 全新对话测，最多 3 轮，通过才有 PI-PASS.md | 建造者自己测自己，STATE 滞后、tool-index 不在仓库、路由回归没证据，8 个样本全是自说自话 | Pi 测试员报告第 0 节 |
| D3 | 恢复数字写“未核实”：469 和 467 都作废，以 `git diff` 差集命令输出为准 | 两处数字互相打架，675−208=467，v3.1 说 469 的理由加不出这个数 | 整合报告 C1 |
| D4 | 范围外改成 21 个（O1–O21），不是 19 个 | 名单数出来是 21 个 | 整合报告 C2 |
| D5 | v3.1 §3.2“删掉 v2.1 那句话”作废；Seep 触发条件只记在 `lifecycle/V31-C3-SEEP-TRIGGER.md`，v2.1 原文不动 | v2.1 是冻结文件，不许改 | 整合报告 C3 |
| D6 | 执行提示词“做到 100% 再停”作废，改成“做到 R8/R9，或命中停下条件之一就停” | R1–R8 合计约 35.5 小时，一夜跑不完；停下规则本来就允许停 | 整合报告 C4 |
| D7 | 完成标准第 10 条改成“回归重跑过，记录齐全；失败只追加记录、不改旧结论、不阻塞冻结” | v3 的回归规则就是这样，v3.1 写成了“零失败” | 整合报告 C5 |
| D8 | macOS / iOS 写死：范围外，直到有 Mac / iOS 设备。完成标准改成“42 个有 verdict，2 个待定” | v3.1 里 macOS/iOS 没决定，却要求 44 个全有 verdict | 整合报告 C6 |
| D9 | R2 第 4 项改判“未做（无真 Codex）”，STATE“R2 完成”改成“R2 部分通过”；完成标准拆两档 | `cases/sample-1/CODEX-RECEIPT.md` 自己写明“无真实 Codex 会话历史” | 整合报告 C7 |
| D10 | 样本 1 的 L5 改成只写“L5：未做” | 验收文件第 65 行还写“未通过 / 未声明”两种混写 | 整合报告 C8 |
| D11 | v3 §13.2、§11.1 的错句进附录 A 作废对照表，v3 原文不动 | “比较工具真调过”“671 个文件”都是假的，冻结文件不能改原文 | 整合报告 C9、C15 |
| D12 | R0“开新分支”作废，改成“只打标签，v3.1/v3.2 就在 main 上做” | 标签有了，远程只有 main，R1/R2 已直接上 main | 整合报告 C10 |
| D13 | 安装拷贝证明改成“电脑本地证明”，新克隆后必须重跑 `refresh-tool-index.sh` 生成 tool-index.md | tool-index.md 被 gitignore，仓库永远证明不了；MANIFEST 说“已生成 5.8KB”，新克隆里没有这个文件 | 整合报告 C11 |
| D14 | Stage 10 前置门改成“Stage 5–9 有一个‘不通过’就不开测；‘部分通过’不拦门” | 原话没写部分通过拦不拦门 | 整合报告 C12 |
| D15 | 测试员接口：测试员不与执行方并行同写，只读仓库、只写自己目录；总数仍 ≤6 | v3.1 并发规则没写测试员算不算工人 | 整合报告 C13 |
| D16 | 三宿主目录检查改成四档记录；“删掉”只针对 REA 文件，不删目录 | 新电脑上目录可能不存在，Codex 宿主目录不在三者里 | 整合报告 C14 |
| D17 | `versions.lock` 和 `check_state.py` 从 R7 提前到 R0；STATE 滞后是复发病，提交后立即回写 | HEAD `81fc67e` 时 STATE 又落后一个提交；防线来得太晚 | 整合报告 P5、P11 |
| D18 | 停下条件统一成三种（第 4 种“一个能用的引擎都没有”并进第 1 种） | v3.1 写四种，R9 设计写三种，打架 | Pi 测试员报告第 8 节 |
| D19 | 恶意软件门顺序改对：每个阶段第 0 步先过门，Stage 15 是 dedicated 领域阶段，门在 13/14 之前 | v3.1 说门在 Stage 15，R5 顺序却是 13/14 先 | 整合报告缺失 6 |
| D20 | 每夜节奏总表：R0–R9 合计约 47.5 小时，一夜 1–2 个阶段，跑不完交半成品进下一夜 | v3.1 只有各阶段上限，没有总表 | 整合报告缺失 7 |

## 从磁盘恢复清单（没有任何聊天记录时，照这张单子做）

> 聊天会被压缩、被总结，压缩几次就忘了最初的顺序。所以仓库才是真理，聊天不是。任何一个新智能体，只靠仓库就能接手。

1. 先 `git pull`，以 GitHub main 为准。本地 `~/workspace/reverse-fusion/` 不是真理：它里面没有 `FUSION-FINAL-v2.1.md`，本地 MANIFEST 还是 v1.0 旧版。**唯一真理是 GitHub main。**
2. 读本文件（`FUSION-FINAL-v3.2.md`）+ `FUSION-REVIEW-v3-AUDIT.md` + `lifecycle/MANIFEST.yaml`。
3. 读 `lifecycle/STATE.yaml`：看 `current_stage`、`next_step`、`last_commit`。用 `git log` 核对 `last_commit` 在不在远程 main 上；对不上就以 `git log` 为准，改 STATE，不许改 git 记录。阶段开始前先跑 `python lifecycle/check_state.py`（R0 已建，见 D17），它说对不上，就按它给的修法命令修，不许猜。
4. 核对锁定提交：REA `4491c84…`、reverse-skill `ce67509…`。Seep `1ea9399…` 只在 Track B 里核对，本执行里跳过。
5. 克隆不要放 `/tmp`：`/tmp` 是 512M，克隆两次都失败（`fatal: invalid index-pack output`）。仓库目录必须放在 ≥2G 磁盘的工作目录，例如 `D:\reverse-fusion-v2` 或 `~/workspace/_scratch/`。
6. 从 STATE 的 `next_step` 继续做。**v3.2 是续接，不是重做：** R1、R2 已做完（提交 `81fc67e`），从 R3 开始，R1/R2 里按 D9/D10 返工的除外。做完一小步就更新 STATE，提交到 GitHub，报告哈希值和链接。没有提交、没有核实过的远程提交哈希值和链接，就不算做完。
7. 停下条件只有三种（见第 9 节规则 C）。其他问题记成开放事项“以后再说”，继续走。

---

## 给零基础的 Davis 看的 1 页说明（你只需要看这一节）

**v3.1 又出了什么问题？** 电脑上的智能体按 v3.1 做到 R2，看着挺快，但深查发现还是老毛病：第一，数字又打架了，469 还是 467、范围外是 19 还是 21，两处都算不对；第二，样本 1 说有一次“真正的 Codex 往返”，回执自己写着“无真实 Codex 会话历史”，STATE 却写“R2 完成”；第三，部署根本没做完，根目录没有 CLAUDE.md，技能没装到智能体能读到的地方，MCP 路径写死在 D 盘，换电脑就坏；第四，测试还是自己测自己，没有第二个人从零跑过。

**v3.2 是干什么的？** 在 v3.1 上补两件大事，再修上面那些小账。第一件，部署按你说的公共文件夹来：一个文件夹放全部东西，每个智能体只拿三根细指针，不复制、不装三份，换盘只改一个配置文件。第二件，测试换一个人：Pi 全新对话从零测，测完写报告，建造者修，修完再测，最多测三轮，通过了才有 PI-PASS.md，没有这份文件就不许说完成。

**你要做什么？** 把这份文件交给电脑上的智能体，让他从 R3 继续做（R1、R2 不用重做），做到 R9，Pi 测通过了才算完。你睡觉的时候他自己往前走，早上看仓库里的 STATE 和提交记录就知道做到哪了。**Track B（样本 3 + Seep）还是单独线，你自己直接安排，不进这份执行提示词。**

**什么叫 v3.2 做完了？** 第 13 节的 13 条完成标准全过，一条没过就不许说做完了。最关键的一条是第 13 条：没有 PI-PASS.md，就不算完成。

---

## 1. v3.2 的目标（和 v2.1、v3、v3.1 一样，三种做法，三种验收词）

一句话：**一个什么都能搞的逆向平台。** 能重做的就重做一个功能一样的；太难重做不出来的，就绕过它的卡密系统，能用就行；只想要一段算法的，就只抽那段算法。

|  | 模式 1：全重建 | 模式 2：绕过 | 模式 3：算法抽取 |
|---|---|---|---|
| 目标 | 重做一个功能一样的**新程序** | 让原程序的卡密 / 许可证检查失效，原程序其余功能照常 | 只抽出一段算法，能单独跑 |
| 用 L4/L5 吗 | 用 | **不用，不许写 L4/L5** | **不用，不许写 L4/L5** |
| 结论只写哪三档 | 通过 / 部分通过 / 不通过 | 通过 / 部分通过 / 不通过 | 通过 / 部分通过 / 不通过 |

**禁词：** “基本完成”“大体上可以”“应该没问题”一律不许写。结论只许四档：**通过 / 部分通过（列出哪几项没过）/ 不通过 / 未做**。没核实的东西写“未核实”，永远不许写成“通过”。

## 2. 锁定版本与数字冻结表（和 v2.1、v3、v3.1 一样，一个字不改；数字错了就写未核实）

| 项目 | 版本 | 锁定提交 | 用法 |
|---|---|---|---|
| REA | 6.9.0 | `4491c84c82140a43fa12390b727840a433875ba8` | 只当分析引擎（MCP 工具调） |
| reverse-skill | 1.9.0 | `ce675096e6a2cd4789a76f9bd618feddc2b6f333` | 唯一总控 + R46（完整版，文件数见下） |
| Seep | 1.15.0 | `1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e` | 只抽 5 样，Track B，不进本执行 |

**数字冻结表（D3、D11）：** reverse-skill 上游是 **675** 个文件（`git ls-files core | wc -l` = 675，实测一致），不是 671；v3 §11.1 那句“671 个文件”作废，见附录 A。恢复清单是 469 还是 467，**两个数字都作废，写“未核实”**：算法是 `git diff --stat 瘦身提交` 的差集计数，命令写进 R4，数字以该命令输出为准，在此之前不许写死总数。数量检查一律跑 `git ls-files | wc -l`，和 MANIFEST 里存的那次输出比对，不许凭印象写总数。

## 3. 路由：修到只有 1 个总控说了算（v3.1 §3 全保留，D5、D16 两处修正）

**原则（只许这一句）：** reverse-skill 是唯一总控。REA 只当 MCP 工具调，不许加载它的技能文件当总控。Seep 只抽 5 样，不许加载 softseep、SYSTEM.md、Lab Gate、MCP 服务器。

### 3.1 修 R1/R46 翻盘

1. **改表：** `core/skills/config/routing.json` 里，R1 的 `\bapk\b` 改成能匹配中文后面直接跟 apk 的写法（比如 `apk` 前面不要求词边界，或加一条 `复刻.*apk|apk.*复刻` 的组合规则）。改完跑一遍：提示词“复刻这个APK”“复刻这个 APK”“reconstruct this apk”“rebuild this apk”四个都要进 R46，错一个就不算修好。
2. **改调用：** 进 R46 一律用明确开关，不许靠提示词猜。命令是 `master-route.ps1 --primary R46`（或 `.sh` 的同款）。每个模式 1 的案子，`scope.md` 里必须写“进 R46 的命令是 `--primary R46`，输出里 `confidence: explicit`”。宿主不支持 `--primary` 时，改走 routing.json 关键词 + 人工复核记录，不许只写“走过了”。
3. **回归集文件化：** 回归提示词扩到中英各 6 句 + 大小写变体，存为 `cases/_shared/routing-regression.txt`，每阶段开头必跑，R8 必跑。只测 4 句不算回归。

### 3.2 Seep 分支触发条件（D5）

v2.1 §1.4 原文不动（冻结文件不许改）。触发条件只记在执行层文件 `lifecycle/V31-C3-SEEP-TRIGGER.md` 里：目标是 PE/APK 且提示词里有“许可证校验 / 卡密 / 加壳 / 壳 / 授权验证”，或 REA 返回 `target_format_unsupported` 以外的原因且案子记录写明“疑似加壳/许可证校验”，就走 Seep 分支（Track B 里走，本执行里只记录、不执行）。v3.1 §3.2 那句“加不上就把 v2.1 那句话删掉”作废。

### 3.3 JS/APK 定死走哪个工具

| 目标 | 第一个工具（定死） | 备用 |
|---|---|---|
| JS | 先试 `js-reverse_*` MCP；装不上才走 REA `analyze_javascript_application` | 两个都试过、都写下报错，才走 Node 本地复现 |
| APK | 先试 REA `open_binary` → `inspect_android_package`；再试 jadx/apktool | 两个都试过、都写下报错，才走手动反编译 |
| PE | REA `open_binary` → `binary_overview`（样本 1 已证明） | Ghidra 无头 |
| ELF | REA `open_binary` 先试（会拒绝，有记录）；然后 Ghidra 无头 + QEMU（样本 2 已证明） | — |

**每个案子的 `scope.md` 第一行必须写模式 + 第一个工具名。**

### 3.4 REA 的技能文件不许加载——变成可检查的清单（D16）

装机时（R4）逐项核对，写进 MANIFEST，四档记录：存在并清理 / 存在但无 REA 文件 / 不存在 / 宿主是 Codex（目录另查）。“删掉”只针对 REA 文件，不删目录本身。检查结果写一句话进 MANIFEST：“REA 技能文件检查：找到 X 个，已绕开 / 没找到。”没这句话，Stage 5 不许开。

### 3.5 tool-index.md 必须生成（D13）

跑 `core/skills/scripts/refresh-tool-index.ps1`（或 `.sh`），生成 `core/skills/tool-index.md`。**新克隆后必须重跑一次**（它是 gitignored，克隆后一定没有；MANIFEST 说“已生成 5.8KB”从仓库里证实不了，不许当证据）。生成不了就写明为什么、用的什么代替。没有这个文件，任何技能说的工具路径都不算有根据。

### 3.6 路由器回归检查

**每阶段开头必跑：** `master-route.sh --hint "apk" --dry-run` 和 `--hint "复刻这个APK" --dry-run`，两个都要退出 0、分别指到 `apk-reverse` 和 `reconstruction`。错一个就停下修，不许继续。命令 + 输出原文要存进该阶段的证据文件，只记结论不算回归。

## 4. 恢复的数字和旧修正（v3.1 §4 全保留，D3、D13 两处修正）

1. **数字：** 上游 675，本地 core 675，恢复清单数按 §2 的算法复核，在此之前写“未核实”。以后不许写死总数。
2. **重补 3 个被覆盖的旧修正（Stage 1 改对了，恢复时被覆盖回去了）：** `core/README_zh.md` 里“192 条”、`core/docs/RELEASE-CHECKLIST.md` 里“26 项”、`core/skills/routing_zh.md` 里“78 个工具”。重补后写进 DECISION-LOG（D11）。`RELEASE-CHECKLIST.md` 仍写“25 项”的也要改成 26 项，一并在 R4 做。
3. **MANIFEST 改对：** `modules_kept` 写 675；`upstream_count` 写 675（`.git` 不是 tracked 文件，不许算）；`do_not_use` 里删掉 `reverse-skill_unrelated_modules`、`ctf_sandbox_orchestrator`、`pentest_tools_src_hunter`（正是刚恢复的模块）。
4. **安装拷贝刷新要证明（D13）：** 旧的三份安装拷贝（`.claude/skills`、`.agents/skills`、`.pi/skills`）按第 11 章废止，改成第 11 章的三个细指针。证明改成“电脑本地证明”（文件数 + 时间 + 命令输出写进 STATE，仓库只存 STATE）。

## 5. 证据链：从 REA 到 Codex 再回来（v3.1 §5 全保留，D9、D10 两处修正）

**目标：** 一个证据号从 REA 出来，要能一路跟到账本、交接单、Codex，再回来。

### 5.1 每个真案子必须有的 4 样东西（缺一样就不算接上）

1. **`notes/handoff-manifest.json`：** 按 `check_handoff.py` 要的形状写。先要有这些它才认：`workitems.md`、一个项目 `specs/`（里面有 FR 编号）、`evidence/E-xxx.md` 记录（每条一个 `### E-xxx` 标题 + `- artifact_path:` + `- content_hash:`）。
2. **`E-` 号 → `ev_` 号对照表：** `cases/<案子>/EVIDENCE-MAP.md`，每行写“`E-002` = `ev_646685c7…`（`binary_overview`）”。一个 E 号只许指一个文件，多文件的拆成 `E-003a`、`E-003b`，不许一个号指两个文件。
3. **检查器真跑一次：** 对真清单跑 `python skills/reconstruction/scripts/check_handoff.py <案子根目录> <清单路径>`，把命令 + 输出（PASS 还是 FAIL、几个问题）原样记进验收文件。之前那个 FAIL 是用法错了，按正确用法重跑两次都是 PASS（0 个问题，10 个文件）。以后再报 FAIL，要把命令贴出来。
4. **一次真正的 Codex 往返（D9，两档）：** 有真 Codex 回执（交接单进去，Codex 写实现，回来有回执文件）= 通过；无真 Codex = **未做**。`reimpl/` 由电脑智能体直接写了就当往返，永远不许。样本 1 的 R2 第 4 项现在改判“未做（无真 Codex）”，STATE 的“R2 完成”改成“R2 部分通过”，在 R3 返工时补做或写明为什么做不了。

### 5.2 证据文件自己要带身份

每个证据文件里或同名 `.md` 记录里，必须有：E 号、对应的 `ev_` 号（没有就写“无 REA 证据号，因为……”）、时间。只靠文件名认身份不算数。

### 5.3 措辞纠正（D10）

- `INSTALL-RECEIPT.json` 里的 `"check_handoff_runs": true` 改成 `"check_handoff_help_runs": true`，并加一句“真案子校验未做，见 R2”。
- 样本 1 验收文件里 L5 只写一种：**“L5：未做”**（从没选 L5 范围、没测）。不许写“未通过 / 未声明”两种混写。
- 样本 2 验收文件第一行“用户本轮口径通过”下面必须加一行“R46 L4：部分通过 / L5：未做”，不许只写口径那一行。
- “R46”这个名字保留，第一次出现时加一句“上游叫‘重建交接与等价级别’，R46 是本地叫法”。

## 6. “先找工具，再写脚本”（v3.1 §6 全保留，硬规矩）

```
第 6 条：先找工具，再写脚本（复用优先）

1. 写任何新脚本之前，先查三家的工具单：
   REA 的 260 个工具（cases/stage1/tools-list-rea.json）、
   reverse-skill 的技能方法（core/skills/*/SKILL.md）、
   Seep 的 38 个 seep_* 工具（Tool/mcp/seep_mcp_server.py）。
2. 有现成工具，就用它，并写下工具名 + 证据编号（比如 REA 的 ev_…），
   不要只写一句“用过了”。
3. 没有现成工具，才能自己写。写之前，在验收文件里写一句话：
   “查过了，没有这个工具，因为……”，再开始写。
4. 自己写不犯规，100% 自己写才犯规。
   每个案子至少要真正调一次上游的比对或验证工具，
   比如 compare_functions、verify_reconstruction、export_evidence_bundle。
5. 路由不是每件小事都要走：跑一次测试、算一个数，可以直接做。
   但是，凡是真的需要路由、REA 或 Seep 的活，必须走它们，
   验收文件里必须有工具名 + 证据编号，光说“走过了”不算数。
6. 已经写过的脚本，下个案子要接着用，不要每个案子重写一份。
   比如“改一个常量、看比较器能不能发现”这个检查，只写一份大家共用，
   放在 cases/_shared/comparator_check/ 下面。
7. 工具不支持也要留记录：写清楚试了哪个工具、报了什么错、
   然后走备用办法，不要一声不吭地跳过。
```

**共用比较器：** R1 已把现有的 7 份比较器脚本合并成一份 `cases/_shared/comparator_check/`（一个入口 + 每个领域的适配参数），以后每个新领域只加参数，不许再写一份新的。JS/扩展/自动化用了三家之外的 chrome-devtools MCP，要在验收文件里补一句“为什么不用三家的工具”，没理由的记成缺口。

## 7. 领域表：44 个，每个都有 verdict（v3.1 §7 全保留，D4、D8、D14、D19 四处修正）

**规则：** “覆盖” = 有阶段 + 有样本 + 有 ACCEPTANCE.md。文件在磁盘上不算覆盖。总表文件是 `cases/_shared/domains-verdict.md`，44 行逐项打勾，R8 机器核对。

### 7.1 有阶段的（v3 的 6 个 + 新加的 4 个 = 10 个）

| 领域 | 阶段 | 模式 |
|---|---|---|
| JS / 网页算法 | Stage 5（已做，R3 重跑验证链） | 3 为主 |
| APK / Android | Stage 6（已做部分，R3 重跑 + 补 dex） | 3 为主，2 在 Track B |
| 浏览器扩展 | Stage 7（已做，重跑） | 3 为主 |
| 协议 | Stage 8（已做，重跑） | 3 为主 |
| 浏览器自动化 | Stage 9（只做观察支撑） | 支撑 |
| 验证码 | Stage 10（前置门，见 D14） | 3 为主 |
| Windows 桌面（含 .NET + 厚客户端） | 新 Stage 13 | 1 为主，2 在 Track B |
| Go/Rust | 新 Stage 14 | 1 为主 |
| 恶意软件分析（安全门 + 领域） | **每个阶段第 0 步先过门** + 新 Stage 15 | 门 + 领域 |
| 固件 | 新 Stage 16（可推迟，写理由） | 1 为主 |

**恶意软件门顺序（D19）：** 门在每个阶段第 0 步，Stage 13/14 之前就要过门，Stage 15 是 dedicated 领域阶段，不许写成“门在 15 才出现”。

**Stage 10 前置门（D14）：** Stage 5–9 的阶段结论里有一个“不通过”就不开测；“部分通过”不拦门。写进 Stage 10 第一行。

**macOS / iOS（D8）：** 范围外，直到有 Mac / iOS 设备。完成标准里写“42 个有 verdict，2 个待定”，不许写“44 个全有 verdict”。

### 7.2 交叉支撑（9 个，不用单独立阶段，但每阶段要引用）

`reverse-engineering/`、`reconstruction/`（R46）、`case-review/`（验收门）、`binary-diff/` + `patch-diff-exploit/`（Stage 11 下面的“跟新版”支撑）、`ghidra-reverse/` + `radare2/`（写进 §9.3 后备梯）、`docs-generator/`（Stage 11/12 生成正式报告时引用）、`diagram-generator/`（报告里的架构图用）。

### 7.3 先标范围外，直到有许可证（2 个）

`ida-reverse/`、`binary-ninja-reverse/`：商业工具，没许可证之前不许默认能用。

### 7.4 明确范围外（21 个，O1–O21，每个一句话理由）

api-security、cloud-k8s、code-audit（要源码；目标自带源码时例外）、database-security、email-security、identity-federation、llm-security（例外：它引用的“装第三方技能/MCP 之前先检查”变成 Stage 5A 的强制装机门）、ot-ics（工业控制，误操作有物理安全风险）、supply-chain-security（例外：来源/SBOM 的思路用在平台自己的工具安装上）、threat-hunting、threat-intelligence、wifi-wireless、windows-ad、radio-sdr（无线电发射有法律管制）、hardware-security（要拿到真设备）、digital-forensics（抓包/内存那一半是 Stage 8 的支撑，磁盘取证那一半范围外）、attack-chain（多阶段攻击编排）、edr-bypass-re（明确范围外，Davis 从没要过绕安全产品）、pwn-chain（写漏洞利用是没要过的第四种模式）、pentest-tools（114 个文件，主动渗透工具链，默认不接它的 MCP，只当参考）、ctf-sandbox（竞赛架子，只当参考）。

**计数核对：** 10 个有阶段 + 9 个交叉支撑 + 2 个许可证门 + 21 个范围外 + macOS/iOS 2 个待定 = 44 个，一个不少。

## 8. 分阶段执行（R0–R8，v3.1 §8 全保留，D12、D17、D20 三处修正）

**顺序不许换。先修衔接，再补领域。R1、R2 已做完（提交 `81fc67e`），v3.2 从 R3 开始。**

| 阶段 | 做什么 | 出口文件 | 时间上限 |
|---|---|---|---|
| R0 | 打标签 `v3-frozen`（HEAD `dafdd9e`，已打）；**只打标签，不开新分支，v3.2 就在 main 上做**（D12）；建 `lifecycle/versions.lock` + `lifecycle/check_state.py`（D17，从 R7 提前）；旧证据一个文件不许删 | 标签 + versions.lock + check_state.py | 30 分钟 |
| R1 | 已做完（提交 `b8ccdcd`）：修路由、Seep 触发条件文件、JS/APK 定死第一个工具、REA 技能文件检查、生成 tool-index.md、路由器回归检查。返工：路由回归命令 + 输出原文要存进证据文件（只记结论不算） | routing.json 改动记录、MANIFEST 检查清单、scope.md | 4 小时 |
| R2 | 已做完（提交 `81fc67e`），改判部分通过（D9）：样本 1、2 各补清单 + 对照表 + 检查器输出；样本 1 的 Codex 往返第 4 项改判“未做”；样本 1 的 L5 改成“未做”（D10）；样本 2 scope.md 第一行补模式 + 第一个工具（R1 说做了 6 个，样本 2 漏了） | 2 份清单、2 份对照表、检查器输出、CODEX-RECEIPT 修正 | 4 小时 |
| R3 | 补一次真正的 REA 验证调用：样本 1 上调 `export_evidence_bundle` + `compare_functions` + `build_reconstruction_obligation_ledger` + `verify_reconstruction` + `evaluate_reconstruction_coverage`，把结果或确切的 `unsupported` 报错记进验收文件；旧领域重跑验证链 | 样本 1 验收文件更新 + 证据文件 | 3 小时 |
| R4 | 修数字和安装：恢复数按 §2 算法复核、重补 3 个旧修正（D11，含 RELEASE-CHECKLIST 的 25→26 项）、MANIFEST 改对、按第 11 章废止旧三份拷贝、Seep“不装”检查清单写进 MANIFEST | MANIFEST、DECISION-LOG D11、STATE 里的数字 | 2 小时 |
| R5 | 补领域：新 Stage 13（Windows + .NET + 厚客户端）、Stage 14（Go/Rust）、Stage 15（恶意软件分析门 + 领域，门在 13/14 之前）、Stage 16（固件，可推迟写理由）；macOS/iOS 写明范围外；21 个范围外写进总表；每个新领域简单样本必须进仓库（没网也能跑） | 每个新领域 1 个案子包（scope/交接单/ACCEPTANCE/unknowns/evidence/reimpl） | 每个领域 3 小时 |
| R6 | 共用比较器 + 复用检查：合并 7 份比较器脚本成 `cases/_shared/comparator_check/`；每个旧案子补一句话“复用检查：查过工具单，结论是……”；以后每个新案子照第 6 条做 | `cases/_shared/comparator_check/` + 8 份验收文件更新 | 3 小时 |
| R7 | 换电脑防线（审计 §7 的 12 条，一条一条做）：版本锁已在 R0 建好，这里补引擎清单门、单写者规则、子模块硬门、唯一路由文件、授权模板、离线待推箱、样本本地备用、`.ps1`/`.sh` 孪生表、REA 技能检查、样本下载先过恶意软件门 | versions.lock（已建）、check_state.py（已建）、STATE 待推队列、授权模板 | 4 小时 |
| R8 | 回归 + 冻结：全领域重跑（第 6 条共用比较器 + R3 验证链）、对照第 13 节 13 条完成标准逐项核对、写 V3.2-REPORT + GAPS、README 能照着跑任一领域、冻结 | `cases/final/V3.2-REPORT.md`、`cases/final/GAPS.md` | 3 小时 |

**每夜节奏总表（D20）：** R0–R9 合计约 47.5 小时（R0–R8 约 35.5 小时 + R9 最多 12 小时）。一夜 1–2 个阶段，跑不完就交半成品进下一夜，STATE 写清“做到哪、没做到哪”，不许靠“做到 100%”硬撑。每阶段记实际用时进 STATE；超时走 CHANGE-REQUEST 调上限。

**Track B（单独线，不编号进 R0–R9，不进 Muse 写的执行提示词）：** 样本 3 + Seep 抽取与运行。Davis 自己直接安排。

**样本分级（每领域）：** 1 个简单（必须过）+ 1 个中等（应该过）+ 最多 1 个难的（流程对、失败原因写清就算过）。难样本永远不许卡住后面；修一次再跑，还不过就记部分通过、往下一个走。

## 9. 长时间无人值守执行（Davis 睡觉时也能往前走）

### 9.1 仓库是唯一真理，聊天不是

聊天会被压缩、被总结，压缩几次就忘了最初的顺序。所以仓库才是真理。任何一个新智能体，只靠仓库就能接手：读本文件 + 审计文件 + MANIFEST + STATE + `check_state.py` 的输出。每阶段交接时另写一页“交接单”（本阶段做了什么、下一步、证据），不许只靠 STATE 一行。

### 9.2 STATE 检查点（D17）

每做完一小步就更新 `lifecycle/STATE.yaml`，每 45 分钟写一次。字段要校验（`check_state.py`，R0 已建），不是自由文本。**提交后立即 `git rev-parse HEAD` 回写 STATE，提交命令和 STATE 回写写成同一条命令链，不许分两步做**——STATE 滞后已经复发两次（Stage 11、Stage 12、R1、R2 都落后一个提交）。STATE 和 `git log` 对不上时，按 `check_state.py` 给的修法命令修，不许猜、不许停下。

### 9.3 不许卡住：往前走的规则

**永远不许停的清单：** 范围冲突；工具返回 `provider_unavailable` / `target_format_unsupported`；某个可选引擎没装；样本第一次失败；一个文件在一个位置找不到（先去镜像位置找）；一段话看起来自相矛盾（先查第 14 节的决议，表里有就按表办）。

**只许停的三种情况（规则 C，一个字不改；D18）：**
1. 同一个步骤、同一个错误，失败两次；
2. 一个样本修两次还是失败；
3. 发现新矛盾，有文件 + 行号证据，计划里又没有解法。

v3.1 的第 4 种“一个能用的引擎都没有”并进第 1 种：如果一个引擎都跑不起来，那是第 0 步环境核对被卡住，修一次环境还卡，就按第 1 种停。其他问题都记成开放事项“以后再说”，继续做下一步，不要停。**“做到 100% 再停”这句话作废（D6）：** 做到 R8/R9，或命中上面三种之一就停。

**备用梯（写在计划里，不许临场发明）：** REA MCP 调用失败 → 改用命令行 `rea …` → 用对应领域命令行工具直接做；REA 分析 ELF 失败 → Ghidra 12.2 无头 → QEMU 跑原版 + gdb 断点 dump；Node 版本被拒 → 用 MANIFEST 里记的 Node 路径（Node 24.22.1）；npm 安装脚本失败 → `npm ci --ignore-scripts` 再单独 `npm run compile`；样本跑不起来（缺 DLL）→ 按样本 1 的做法从 SDK / Build Tools 补 DLL，记下每个 DLL 的来源和哈希；样本跑不起来先查杀毒拦截记录（Windows 杀毒 / SmartScreen 可能拦样本），排除之后再写失败原因。

### 9.4 不许悄悄失败、不许假装做完

每做完一小步就更新 STATE，每做完一个阶段就把全部结果提交到 GitHub 仓库 reverse-fusion-v2 的 main 分支，检查有没有漏文件，核对远程提交，报告提交的哈希值和链接。没有提交、没有核实过的远程提交哈希值和链接，就不算做完，不许回复“做完了”。不要赶时间，不要凭记忆、凭印象做事，不要只看标题就说通过了。每个结论都要有证据：文件 + 行号，或者命令 + 结果。没核实的东西写成“未核实”，永远不要写成“通过”。回复之前自己检查一遍。宁可慢、宁可说没做完，也不要快、不要假装做完了。

**离线后备：** 没网 / 没 GitHub 权限时，写本地待推箱 + STATE 记待推队列，待推箱文件格式是 `cases/_shared/offline-queue/<阶段>.md`（每行：文件名 + 本地哈希 + 应提交的分支）；“做完”改成“本地做完 + 已排队”，永远不许假装已提交。R8 再推一次；没有远程哈希、也没有排队记录的阶段，不算做完。

## 10. 并发硬规则（Claude Code，Davis 定）

Davis 用的是 Claude Code，子智能体 3–5 个同时跑是正常的，工作流也可以同时跑，但**总数不许超过 6 个**。同时最多 5 个子智能体；算上工作流，同时最多 6 个在跑的工人。多出来的排队等着。**单写者规则：** 只有阶段负责人写 STATE/MANIFEST；并行工人只写自己领域的目录。

**测试员接口（D15）：** 测试员（第 12 章的 Pi）不与执行方并行同写。测试员只读仓库、只写自己目录（快照的 `pi-work/`）；测试员启动时执行方停写 STATE；总数仍 ≤6。

## 11. 共享文件夹部署（新电脑从零手册，D1）

**模型（一句话，不改 Davis 的模型）：** 一个公开共享文件夹，拉一次，全在里面。每个智能体只拿三根细指针，不复制、不装三份。路径只写在一个配置文件里，换盘、换文件夹只改那一个文件，再跑一次同步脚本，所有指针跟着变。

### 11.1 文件夹布局

```
D:\reverse-fusion-v2\                  ← 共享文件夹（用户自选盘和文件夹，默认 D 盘新建一个文件夹）
│   .git\                              ← git 仓库
│   .gitmodules                        ← 两个子模块：engine/rea、upstream/reverse-skill
│   .mcp.json                          ← 生成的文件，不要手改（模板是 .mcp.json.template）
│   .mcp.json.template                 ← 新文件：带占位符的模板，进仓库
│   CLAUDE.md                          ← 新文件：细指针（只指路，不写内容）
│   AGENTS.md                          ← 旧文件：顶部加指针，保留原来的 5 条同步约定
│   FUSION-FINAL-v3.2.md               ← v3.2 正文（部署章就是它的一章）
│   README.md                          ← v3.2 要重写：删掉所有 D:\ 写死路径，改成读配置文件
│   .gitignore                         ← 加一行 .mcp.json（生成的文件不入库）
├───core\                             ← reverse-skill 完整版 675 个文件（总控 + 全部技能）
│   ├───skills\SKILL.md               ← 唯一总控 reverse-skill-router（第一入口）
│   ├───skills\reconstruction\SKILL.md← R46 重建（由总控打开，不单独装）
│   ├───skills\config\routing.json    ← 唯一路由表
│   ├───skills\scripts\master-route.ps1 / master-route.sh
│   └───skills\tool-index.md          ← 部署时生成（部署前仓库里没有）
├───engine\rea\                       ← 子模块 REA 6.9.0，锁定 4491c84（只当 MCP 工具调）
│   └───scripts\rea.mjs               ← MCP 服务器入口（子模块不初始化就没有这个文件）
├───upstream\reverse-skill\           ← 子模块 reverse-skill 1.9.0，锁定 ce67509（对照用的上游原件）
├───cases\                            ← 全部案子包
├───lifecycle\                        ← MANIFEST.yaml、STATE.yaml、DECISION-LOG.md 等
│   ├───versions.lock                 ← R0 已建：精确版本号（Node 24.22.1、Ghidra 12.2、JDK 25…）
│   └───check_state.py                ← R0 已建：STATE 校验脚本
└───tools\
    └───fusion-sync.ps1 / fusion-sync.sh   ← 新文件：同步脚本（读配置文件，生成三根指针）
```

共享文件夹**外面**、每个智能体自己家里的东西：

```
%USERPROFILE%\.fusion\                ← 固定位置，不随共享文件夹搬家
│   fusion-home.yaml                 ← 唯一配置文件（§11.3）
└───tools\fusion-sync.ps1            ← 同步脚本的副本
%USERPROFILE%\.claude\skills\reverse-skill-router\SKILL.md   ← Claude Code 全局技能指针
%USERPROFILE%\.codex\skills\reverse-skill-router\SKILL.md    ← Codex 全局技能指针（路径未核实）
%USERPROFILE%\.pi\skills\reverse-skill-router\SKILL.md       ← Pi 全局技能指针（路径未核实）
```

### 11.2 三根细指针的准确内容（占位符是 `<SHARED_FOLDER>`）

**指针 (a) MCP 配置：只配 REA 一个服务器。** 共享文件夹根目录的 `.mcp.json`（由同步脚本从 `.mcp.json.template` 生成，不要手改）：

```json
{
  "mcpServers": {
    "rea": {
      "command": "<NODE_EXE>",
      "args": ["<SHARED_FOLDER>/engine/rea/scripts/rea.mjs", "mcp"],
      "cwd": "<SHARED_FOLDER>",
      "env": { "HUSKY": "0", "GHIDRA_INSTALL_DIR": "<GHIDRA_DIR>", "JAVA_HOME": "<JAVA_HOME>" }
    }
  }
}
```

关键改动（相对现在仓库里的 `.mcp.json`）：`command` 不再写死 `D:\Tools\...`，同步脚本先填配置文件里的 `node_exe`；`args` 改成**绝对路径**，再加 `"cwd": "<SHARED_FOLDER>"`；`GHIDRA_INSTALL_DIR`、`JAVA_HOME` 从配置文件里填；只有 `rea` 一个服务器。reverse-skill 不配 MCP（它是技能文件）；Seep 不进本执行。Codex 的 MCP 配置文件位置和写法要在 Davis 电脑上核实（未核实），不要凭印象写。

**指针 (b) 全局技能指针：只有一个 `reverse-skill-router`，正文只有指路。** 每个智能体的全局技能目录里只放这一个文件：`reverse-skill-router/SKILL.md`。不要复制 `core/skills/` 的内容，不要复制 `reconstruction`，不要复制旧的 Codex 适配器。示例全文：

```markdown
---
name: reverse-skill-router
description: Routes reverse engineering tasks to the right skill. Use when a task is about analyzing, rebuilding, bypassing or extracting an algorithm from a program and the correct entrypoint is unclear.
---
# reverse-skill-router（指针文件，不是总控本身）
这个文件只有指路，不写任何方法。真正的方法全在共享文件夹里，不要在这里加内容。
共享文件夹位置：`<SHARED_FOLDER>`
第一步，先读这一个文件：`<SHARED_FOLDER>/core/skills/SKILL.md`（唯一总控）。
第二步，按总控说的做。路由用 `<SHARED_FOLDER>/core/skills/scripts/master-route.ps1`（Windows）或 `master-route.sh`，路由表只认 `<SHARED_FOLDER>/core/skills/config/routing.json`。工具路径只认 `<SHARED_FOLDER>/core/skills/tool-index.md`。
重建（R46）入口在 `<SHARED_FOLDER>/core/skills/reconstruction/SKILL.md`，由总控打开，不要直接跳过去。
共享文件夹搬家后，这个文件不用手改：改配置文件里的一行，再跑一次同步脚本，它会自动重写。
```

**指针 (c) 根目录 `CLAUDE.md` / `AGENTS.md`：只指路。** 共享文件夹根目录新建 `CLAUDE.md`，全文如下（不要把 `core/CLAUDE.md` 的内容抄进来，那是上游 reverse-skill 自己的文件）：

```markdown
# reverse-fusion-v2（指针文件）
本项目位置：`<SHARED_FOLDER>`（共享文件夹，三个上游、全部技能、全部案子都在里面）。
第一步，先读：`<SHARED_FOLDER>/FUSION-FINAL-v3.2.md` 的“从磁盘恢复清单”那一节，再读 `<SHARED_FOLDER>/lifecycle/STATE.yaml`，看 `current_stage` 和 `next_step`，从那里继续做。
总控是 `<SHARED_FOLDER>/core/skills/SKILL.md`（reverse-skill-router）。分析引擎是 REA，只通过 MCP 调，不加载它的技能文件当总控。Seep 不在这里装（Track B，单独走）。
路径不要写死：共享文件夹位置只记在配置文件里（`%USERPROFILE%\.fusion\fusion-home.yaml` 的 `shared_folder` 这一行）。搬家只改那一行，再跑一次同步脚本。
```

根目录 `AGENTS.md`：**保留现有的 5 条同步约定全文**（GitHub `gthubtom1/reverse-fusion-v2` 的 main 分支、每轮提交核对远程哈希、不夹带凭据、不自动建分支开 PR），只在文件顶部加指针（项目位置、第一步读 v3.2 和 STATE、总控路径、配置文件位置）。

**废止声明：** 旧办法“`.claude/skills/`、`.agents/skills/`、`.pi/skills/` 三个目录都有 `reverse-skill-router/SKILL.md` 和 `reconstruction/SKILL.md`”作废。全局技能只放 router 一个，reconstruction 不单独装，由总控从共享文件夹里打开。旧的三份安装拷贝删掉，只留全局指针（删之前确认全局指针已经生成）。

### 11.3 唯一配置文件

- **名字：** `fusion-home.yaml`；**位置：** `%USERPROFILE%\.fusion\fusion-home.yaml`（Windows 用户家目录下的固定位置）。**不在共享文件夹里面**——如果它在共享文件夹里，文件夹一搬家就找不到它。
- **示例：**

```yaml
# 唯一配置文件。换盘、换文件夹：只改 shared_folder 这一行，再跑一次同步脚本。
shared_folder: D:\reverse-fusion-v2
node_exe: D:\Tools\node-24.22.1\node-v24.22.1-win-x64\node.exe
ghidra_install_dir: D:\Tools\Ghidra-12.2\ghidra_12.2_PUBLIC
java_home: D:\Tools\jdk25
pinned:
  rea: { repo: morluto/rea, version: 6.9.0, commit: 4491c84c82140a43fa12390b727840a433875ba8 }
  reverse-skill: { repo: gthubtom1/reverse-skill, version: 1.9.0, commit: ce675096e6a2cd4789a76f9bd618feddc2b6f333 }
  seep: { repo: angusdevgo/Seep-Reverse-Lab, version: 1.15.0, commit: 1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e, status: track-b-only-not-installed-here }
```

同步脚本 `tools/fusion-sync.ps1`（和 `.sh` 孪生版）只做四件事：读配置文件拿四个值；生成 `.mcp.json`；生成根目录 `CLAUDE.md` 和 `AGENTS.md` 顶部指针；生成每个智能体全局技能目录里的 `reverse-skill-router/SKILL.md`。同步脚本自己留一份副本在 `%USERPROFILE%\.fusion\tools\`，文件夹搬家后不用先找到新文件夹就能跑它。

### 11.4 新电脑部署顺序（一步一步，不许跳步）

| 步 | 做什么 | 命令 / 操作 |
|---|---|---|
| 0 | 选文件夹 + 部署前检查 | 用户定一个文件夹（默认 D 盘新建一个文件夹）；检查磁盘 ≥2G、路径短（建议 `D:\rfv2`，Windows 长路径会坏）、网络通、杀毒不会删样本 |
| 1 | 装前置工具 | Node 24.22.1、Ghidra 12.2、JDK 25、Git、Python 3（版本号以 `lifecycle/versions.lock` 为准） |
| 2 | 拉仓库 | `git clone https://github.com/gthubtom1/reverse-fusion-v2.git D:/reverse-fusion-v2` |
| 3 | 初始化子模块（不许跳过） | `git submodule update --init --recursive`。完后 `engine/rea/scripts/rea.mjs` 必须存在，不存在就停下修。`git submodule status` 两行前面都不许有 `-` 号 |
| 4 | 写唯一配置文件 | 新建 `%USERPROFILE%\.fusion\fusion-home.yaml`，填 4 个路径 + 3 个锁定提交 |
| 5 | 拿同步脚本 | 从共享文件夹复制 `tools/fusion-sync.ps1` 到 `%USERPROFILE%\.fusion\tools\` |
| 6 | 跑同步脚本 | PowerShell 里跑同步脚本，生成 `.mcp.json`、根 `CLAUDE.md`、`AGENTS.md` 指针、三个智能体的全局技能指针 |
| 7 | 生成工具索引 | 跑 `scripts/refresh-tool-index.ps1`，生成 `core/skills/tool-index.md`（仓库里原来没有，部署时必须生成） |
| 8 | 跑核查表 | 按 §11.5 一条一条跑，全过才算部署完 |
| 9 | 删掉旧的三份安装拷贝 | 确认全局指针已生成后，删掉旧办法装的三份拷贝，只留全局指针 |
| 10 | 冒烟：跑样本 1 的第一步 | 按 README 跑样本 1 的对照命令（或只跑 `rea doctor` + 路由回归检查）。过了才算“能用” |

搬家顺序：只改 `fusion-home.yaml` 的 `shared_folder` 这一行 → 把整个共享文件夹搬到新位置 → 跑一次同步脚本 → 重跑核查表。**不要手改 `.mcp.json`、技能指针、`CLAUDE.md` 里任何一处路径**，手改的一律在下次同步时被覆盖掉。

### 11.5 部署核查表（每条都是命令 + 预期结果，不是口头说“通过”；10 条全过才算部署完）

1. `git -C <共享文件夹> rev-parse HEAD` 和 `git log --oneline -3`：HEAD 是 v3.2 冻结的提交号。
2. `git submodule status`：两行前面都没有 `-` 号；`ls <共享文件夹>/engine/rea/scripts/rea.mjs`：文件存在。
3. `cat ~/.fusion/fusion-home.yaml`：`shared_folder` 和第 2 步的文件夹一致。
4. `.mcp.json`：只有一个 rea 服务器；args 是绝对路径；有 `"cwd"`；再跑一次同步脚本，内容不变（同步是等幂的）。
5. `CLAUDE.md` 第一行有共享文件夹路径，第二段写着先读 v3.2 和 STATE；`AGENTS.md` 顶部有指针，下面还保留原来的 5 条同步约定。
6. `ls <共享文件夹>/core/skills/SKILL.md`、`config/routing.json`、`tool-index.md`：三个文件都存在；`master-route.sh --hint "apk" --dry-run` 退出 0 指到 apk-reverse，`--hint "复刻这个APK" --dry-run` 退出 0 指到 reconstruction。
7. 全局技能指针只有 router 一个，不含方法内容；正文里写的共享文件夹路径和配置文件一致。Codex、Pi 的全局技能目录同样各查一次（路径未核实，先在 Davis 电脑上确认）。
8. `python -I cases/stage1/mcp_probe.py <node.exe> engine/rea/scripts/rea.mjs cases/stage1/tools-list-rea.json mcp`：`tool_count=260`；`<node.exe> engine/rea/scripts/rea.mjs doctor`：ghidra 相关是 healthy。
9. `python lifecycle/check_state.py`：退出 0；STATE 的 `last_commit` 和 `git rev-parse HEAD` 一致。没落地之前手跑对一遍。
10. 搬家测试（换过文件夹才跑，没换过写“未做”）：改配置 → 搬文件夹 → 重跑同步脚本 → 重跑第 1–9 条；`grep -r "旧文件夹路径" .mcp.json CLAUDE.md AGENTS.md` 预期 0 个结果。

## 12. 独立测试员 R9（Pi tester，D2；放在 R8 之后、冻结之前）

**核心规则（一条都不能改）：**
1. **建造者 ≠ 测试员。** 建造者是 Claude Code（电脑上的智能体），测试员是 Pi。Pi 永远不在建造者的对话里测，建造者永远不在自己的对话里“自测通过”。
2. **Pi 每次都是全新对话。** 每一轮测试（初测、复测）都是一个新的 Pi 对话，没有上一轮的聊天记录，没有建造者的聊天记录。
3. **Pi 只认仓库 + 共享文件夹 + 自己跑出来的命令结果。** ACCEPTANCE.md 在 Pi 眼里只是“建造者的说法”，不是证据。Pi 必须自己跑一遍，跑出来的才算。
4. **Pi 只测、不修、不提交。** Pi 不改代码、不改仓库、不推 GitHub。修是建造者的事。
5. **Seep / Track B 不进测试执行。** 测试执行提示词里不写 Seep、不写样本 3、不写绕过意图。

### 12.1 R9 的位置和编号

- **编号 R9，放在 R0–R8 之后。** R8 是建造者自己回归；R9 是 Pi 独立重跑。R8 通过 ≠ R9 通过。
- **R9 内部有 3 轮（T1、T2、T3），不是 3 个阶段：** T1 初测（Pi 第一次全新对话）；T2 第一次复测；T3 第二次复测（最后一轮）。
- **入口文件（缺一个就不开 R9）：** `FUSION-FINAL-v3.2.md`；`lifecycle/STATE.yaml`（`current_stage: R9`，`last_commit` 必须等于远程 HEAD——R9 开场先由建造者把 STATE 追平，追不平不许开）；`lifecycle/MANIFEST.yaml`（R1–R8 的完成记录）；`README.md`（能照着跑任一领域的第一个小目标）；共享文件夹快照（见 §12.2）。
- **出口文件：** `cases/final/PI-TEST-REPORT-T1.md`、T2、T3（做了几轮就有几份，每份都是 Pi 的原文，一字不改）；`cases/final/PI-PASS.md`（只有 Pi 通过时才有，见 §12.5）；`cases/final/GAPS.md`（更新）；`lifecycle/STATE.yaml`（`pi_test` 字段 + `last_commit` 追平）。
- **时间上限：** T1 最多 6 小时，T2、T3 各最多 3 小时，R9 总共最多 12 小时。超时就停下这一轮，写“时间到，未测完”，没测的写“未核实”，不许赶时间假装测完。时间是设计值，不是实测值（未核实）。

### 12.2 Pi 怎么搭起来：冻结快照，不是建造者的工作目录

建造者在每一轮测试前，做一个**冻结快照**，放在共享文件夹里。快照就是 Pi 的全部世界，Pi 不碰建造者电脑上的其他东西。快照路径格式（每轮一个新文件夹，旧的只读不动）：`<共享文件夹>/v3.2-R9-T1/`（T2 用 `v3.2-R9-T2`，以此类推）。快照里必须有 6 样东西，缺一样，Pi 在报告开头就写缺了什么、那一部分测不了：

| # | 东西 | 为什么必须有 |
|---|---|---|
| 1 | 仓库的干净克隆，定在某一个提交哈希值上（Pi 第一件事就是核对 `git rev-parse HEAD` 是不是这个值） | 不然 Pi 测的和建造者说的不是同一个东西 |
| 2 | `README.md` + `FUSION-FINAL-v3.2.md` | Pi 照 README 从零部署；v3.2 正文只当“规格书”，不当证据 |
| 3 | 全部 `cases/` 和 `lifecycle/` | Pi 要逐项核对建造者的每个结论 |
| 4 | **原版样本文件**（样本 1 的 `CrackMe.exe`、样本 2 的 ELF、各领域自建目标的原版） | 现在这些文件在仓库外（`D:/tmp/fusion-samples/`），Pi 没有它们就跑不了“原版 vs 复现”的对照。建造者必须把样本拷进快照的 `samples/` 里；拷不进来，Pi 就写“原版缺失，对照未核实”，这一项不许算通过 |
| 5 | 环境清单（一页纸）：Node、Ghidra、JDK、QEMU、jadx/apktool、tshark 各是什么版本，装在哪，`.mcp.json` 怎么配 | Pi 的机器和建造者的机器环境不一样时，先对环境 |
| 6 | Pi 自己的工作目录 `pi-work/`（空的） | Pi 的测试输出、临时文件只写在这里，不写进仓库文件里 |

**不许给 Pi 的东西：** 建造者的聊天记录、建造者的自测对话、建造者本地没提交的文件、建造者电脑上快照之外的东西。Pi 首选在 Davis 电脑上跑（和建造者同一台 Windows 电脑，另一个全新对话），因为 README 全是 Windows 路径；如果 Pi 在别的机器上，Windows 专用的步骤一律写“环境不符，未核实”，不许改命令硬凑通过。

### 12.3 Pi 测哪些样本：每个领域一个，分简单 / 中等 / 难

| 领域 | 样本 | 难度 | 模式 |
|---|---|---|---|
| Windows PE（样本 1） | CrackMe（`mr1337`） | 简单 | 模式 1 全重建 |
| ELF（样本 2） | KeyGen | 中等 | 模式 1（L4 部分通过、L5 未做，Pi 要重验） |
| JS / 网页算法 | `cases/js-1`（sig1/sig2） | 简单 | 模式 3 |
| APK / Android | `cases/apk-1`（licdemo，中等，d8 崩未成 dex，Pi 要重验这点还在不在） | 中等 | 模式 3 |
| 浏览器扩展 | `cases/ext-1` | 简单 | 模式 3 |
| 协议 | `cases/protocol-1` | 简单 | 模式 3 |
| 浏览器自动化 | `cases/automation-1` | 观察支撑（只验“观察能不能录到请求链路”） | 支撑 |
| 验证码 | `cases/captcha-1` | 中等 | 模式 3 |
| R5 新领域（Stage 13–16） | 每个新案子各 1 个样本 | 按 R5 定级 | 按 R5 定级 |

**分级：** 简单必须过；中等应该过；难的流程对、失败原因写清就算过。难样本永远不许卡住后面。如果 R5 没交出某个新领域的样本，Pi 就写那个领域“未做”，不许写“通过”。

### 12.4 Pi 一步一步做什么（T1 初测的操作清单）

**第 0 步：环境核对。** 核对快照提交哈希值和 STATE 的 `last_commit`；跑 `rea doctor`、报各工具版本号，和环境清单一个一个对；检查 `core/skills/tool-index.md` 在不在快照里（R1 的教训：建造者说生成了，仓库里没有——不在就写“C10 未核实”）。

**第 1 步：从零部署，只照 README。** Pi 不看建造者的聊天记录，只照 README 从头装、从头跑。哪一步跑不通（命令报错、路径不对、缺文件），原样记下来：命令、报错、退出码。Pi 不许自己改 README、不许自己绕过去。

**第 2 步：路由回归。** `master-route.sh --hint "apk" --dry-run` 和 `--hint "复刻这个APK" --dry-run`，两个都要退出 0；4 个提示词（“复刻这个APK”“复刻这个 APK”“reconstruct this apk”“rebuild this apk”）都要进 R46。命令 + 输出原样贴进报告。

**第 3 步：逐个领域跑样本。** 每个案子做 5 件事：跑原版 vs 复现的对照（5 个用例 + 边界 + 比较器自检），记 `all_match`；对照 ACCEPTANCE.md 的每一个结论重跑；查证据链（`E-` 号能不能对上 `ev_` 号，有没有 `EVIDENCE-MAP.md`；`check_handoff.py` 对真清单跑一遍，PASS 还是 FAIL）；查复用（真调过上游比对/验证工具没有，工具名 + 证据号写出来；只调了自写脚本就写“只用了自写脚本，上游验证工具未调用”）；难样本只看流程对不对、失败原因写没写清。

**第 4 步：写报告，不修东西。** Pi 写完报告就停。报告只写在快照的 `pi-work/PI-TEST-REPORT-T1.md` 里（T2、T3 同理）。

### 12.5 Pi 的测试报告模板（每份报告必须有这 6 节）

0. 环境核对（每项：建造者说的 / Pi 实测 / 通过 / 不通过 / 未核实）；1. 路由回归（提示词 / 预期 / Pi 实测命令 + 输出原文 / 结果）；2. 逐领域结果（每个领域一张表：建造者结论原文 + 文件路径 + 行号、Pi 重跑命令 + 退出码 + 输出、Pi 结果：通过 / 部分通过 / 不通过 / 未做 / 未核实、证据、没过的项、未核实的项；8 个旧领域 + R5 新领域，一个都不能少，没测的写“未做”）；3. 证据链专项（E-→ev_ 对照表有没有、`check_handoff.py` 真跑结果、REA 验证链真调过没有、样本 1 有没有一次真正的 Codex 往返）；4. 缺口清单（给建造者修的单子：编号、缺口、在哪、Pi 看到的现象、要改成什么样才算修好）；5. 总结论（通过 / 部分通过 / 不通过的领域个数 + 名字、下一步修哪几条）。**硬规矩：** 每个“通过”后面必须跟一条证据（文件 + 行号，或命令 + 结果）；没有证据的写“未核实”，永远不许写成“通过”。

### 12.6 建造者怎么修、怎么复测

1. 建造者读 Pi 的报告文件，不读 Pi 的对话。只照报告第 4 节的缺口清单修，一条一条修。
2. 修完就提交到 GitHub main 分支，核对远程哈希值和链接，更新 STATE（`last_commit` 追平新 HEAD）。没有提交、没有核实过的远程哈希值和链接，就不算修完，不许出新快照。
3. 出新快照，开新 Pi 对话。Pi 只拿到新快照 + 旧报告（当“上轮缺口清单”看，不当证据）。
4. 复测只测三样：上轮没过 / 部分通过的项（全测）；上轮通过的领域，每个抽 1 个样本做回归（防止修 A 坏了 B）；STATE 追平 + 路由回归（每轮必跑）。
5. Pi 的报告原文不许改。建造者把 Pi 的报告文件原样拷进仓库 `cases/final/` 提交，记下文件的 SHA-256。想补充说明，另外写一个文件。

### 12.7 最多测几轮，什么叫“Pi 通过了”

- **最多 3 轮：T1 + T2 + T3。** T3 结束还有没过的项，R9 就到此为止，不许再开 T4。没过的项记进 `cases/final/GAPS.md` 当开放事项，由 Davis 决定是接受、还是以后再开一轮。R9 的 verdict 就是“部分通过”，不许说“通过了”。
- **“Pi 通过了”的定义（7 条全过才算，缺一条都不算）：** (1) 每个领域都有 verdict，没有空着的，没有“未做”的领域；(2) 全部简单样本通过；(3) 全部中等样本通过，或部分通过且没过的项有名有姓有原因；(4) 全部难样本流程对、失败原因写清；(5) 证据链通了：样本 1 上真调过一次 REA 验证链，`check_handoff.py` 对真清单是 PASS，样本 1、2 的 `E-`→`ev_` 对照表齐全；(6) 路由回归 4 个提示词全进 R46，两次 `--dry-run` 都退出 0；(7) STATE 的 `last_commit` 等于远程 HEAD 哈希值，`tool-index.md` 在快照里真实存在，Pi 报告里 0 个没有证据的“通过”。
- **出口文件（通过时才有）：** `cases/final/PI-PASS.md`（一页：通过日期、最后一轮是 T几、提交哈希值 + 链接、逐领域 verdict 表、Pi 报告的文件名 + SHA-256）。没有这份文件，R9 就不算通过，v3.2 不许说冻结。`lifecycle/STATE.yaml` 里写 `pi_test: passed` + 通过的提交哈希值。

### 12.8 给 Pi 的执行提示词（草稿，30 行以内，里面没有 Seep / 样本 3 / 绕过）

```
你是独立测试员 Pi，和建造者不是同一个人，没有建造者的聊天记录。
只测下面共享文件夹里的快照，不改代码、不提交、不推 GitHub。
共享文件夹：<共享文件夹>/v3.2-R9-T__/
仓库提交哈希值：<哈希值>，先跑 git rev-parse HEAD 核对。
只照快照里的 README 从零部署、从零跑样本。
逐个领域核对 cases/*/ACCEPTANCE.md 的每个结论，
每个结论都要自己跑一遍，命令 + 退出码 + 输出都记下来。
没有自己跑过的写“未核实”，永远不要写成“通过”。
路由回归、证据链、复用检查都要做（见快照里的测试清单）。
写完报告就停，报告只写在快照的 pi-work/PI-TEST-REPORT-T__.md 里。
（测试清单和报告模板由 Muse 发给你，见对话里的文件）
```

## 13. v3.2 做完了是什么意思（13 条，一条没过就不许说做完了）

v3.1 的 12 条全保留，按 D6、D7、D8、D9 改过，再加第 13 条：

1. 路由器回归检查每阶段都跑过，退出 0（R1；回归集文件化，中英各 6 句）。
2. 四个提示词都进 R46（R1）。
3. Seep 分支触发条件记在 `lifecycle/V31-C3-SEEP-TRIGGER.md`，v2.1 原文不动（R1）。
4. 样本 1、2 各有一份 JSON 指针清单 + 对照表 + 检查器 PASS 输出；样本 1 的 Codex 往返按两档写：有真回执 = 通过，无真回执 = 未做（R2）。
5. 样本 1 上真调过一次 REA 验证链，结果或确切报错已记录（R3）。
6. 数字全对（675；恢复数按 §2 算法复核），3 个旧修正已重补，MANIFEST 已改对，安装按第 11 章废止旧三份拷贝、只留三个细指针（R4）。
7. 44 个领域每个都有 verdict：有阶段的 10 个各有验收记录；21 个范围外已写明理由；macOS/iOS 写明范围外直到有设备；其余交叉支撑已引用（R5 + §7）。
8. 共用比较器只有一份，8 个旧案子各补了一句复用检查（R6）。
9. 换电脑的 12 条防线每条都有文件或记录；`versions.lock`、`check_state.py` 已在 R0 建好（R7）。
10. 全领域回归重跑过，记录齐全；失败的只追加记录、不改旧结论、不阻塞冻结（R8）。
11. `USED-FUNCTIONS.md` 每领域两栏齐全，本机没跑过的写“本机未调用”（R8）。
12. README 能让一个没看过方案的人照着跑任一领域的第一个小目标；README 里的写死路径已全部改成读配置文件或相对路径（R8）。
13. **没有 `cases/final/PI-PASS.md`，v3.2 不许说完成（R9）。**

## 14. 停点审计（v3 §9 的 9 个点 + v3.1 的 3 个点全保留，再加 C1–C15）

v3 §9.1 的 9 条决议全保留（绕过手册取用冲突、样本登记时间打架、3 个 HEAD 对不上、写事实被当成做实施、样本 2 口径没按范围改、开新版本自相矛盾、接线放第几阶段、Stage 0 停工、旧项目 20 多小时没成），v3.1 的 3 条（Stage 5A 数量检查、STATE 滞后、`check_state.py`、自己造工具）全保留，再加本次的 15 条决议（C1–C15，见改动清单 D3–D17）：469/467 都作废以算法为准；范围外 21 个；v2.1 原文不动；“做到 100%”作废；回归零失败作废；macOS/iOS 范围外；R2 第 4 项改判未做；L5 只写“未做”；v3 错句进附录 A；R0 只打标签不上分支；安装证明改本地证明 + 新克隆重生成 tool-index；Stage 10 门只拦“不通过”；测试员不并行同写；宿主目录四档记录。**每条决议的格式都是：旧写法是什么 → 错在哪 → 新写法是什么。旧写法作废，以新写法为准。**

## 15. 预见问题清单（换电脑部署时，三个角度；触发点 → 早发现 → 规则）

- **P1 /tmp 太小，克隆失败。** 触发：任何写“克隆到 /tmp”的步骤。实测 512M tmpfs 两次克隆都报 `invalid index-pack output`。早发现：克隆前跑 `df -h`。规则：仓库目录禁止放 /tmp，必须放在 ≥2G 磁盘的工作目录，写进部署前检查单第 1 条。
- **P2 新克隆子模块是空的。** 触发：Stage 5A / R1。实测 `git submodule status` 显示 `-4491c84… engine/rea`、`-ce67509… upstream/reverse-skill`（`-` = 未初始化）。早发现：`git submodule status` 必须无 `-`。规则：子模块初始化是硬门，未初始化不许开 R1。
- **P3 宿主目录不存在或宿主不同。** 触发：§3.4/§4.4。规则：按 D16 四档记录；Codex 宿主目录在 v3.2 里补一张对照表（未核实，先在 Davis 电脑上确认）。
- **P4 tool-index.md 新克隆一定没有。** 触发：§3.5。原因：它被 gitignore 了。规则：克隆后必跑 `refresh-tool-index.sh`，STATE 记生成时间 + 大小。
- **P5 版本漂移（Node/Ghidra/JDK）。** 触发：各阶段开头。规则：`versions.lock` 从 R7 提前到 R0，先建锁再动手；不许用“最新版”。
- **P6 没网 / 没 GitHub 权限。** 触发：每阶段提交步。规则：沿用离线待推箱（§9.4），格式 + STATE 待推队里字段 + R8 重推责任写死；没有远程哈希、也没有排队记录的阶段不算做完。
- **P7 样本下载不到 / 被墙。** 触发：各阶段找样本。规则：每个领域简单样本必须进仓库（或本地备用样本），没网也能跑简单样本；下载的样本先过恶意软件门。
- **P8 换英文提示词 / 换模型，路由又翻盘。** 触发：R1 回归检查。规则：回归集扩到中英各 6 句 + 大小写变体，存为 `cases/_shared/routing-regression.txt`，R8 必跑。
- **P9 宿主不支持 `--primary` 开关。** 触发：§3.1。规则：宿主不支持时，改走 routing.json 关键词 + 人工复核记录，不许只写“走过了”。
- **P10 新电脑缺工具链（jadx/apktool/frida/adb/tshark）。** 触发：Stage 6/8 开头。规则：缺失记开放事项 + 走备用梯，但“走了备用梯”必须写进 `USED-FUNCTIONS.md`，自己造的替代品永远不算“工具已验证”。
- **P11 STATE 滞后复发。** 触发：每阶段提交后。规则：`check_state.py` 从 R7 提前到 R0；提交命令和 STATE 回写写成同一条命令链。
- **P12 Windows 杀毒 / SmartScreen 拦样本。** 触发：样本运行、`patched/` 产物。规则：样本跑不起来时，先排除“被杀毒删了/拦了”再写失败原因。
- **P13 Windows 长路径。** 触发：克隆 / 恢复。规则：工作目录用短路径（如 `D:\rfv2`），写进部署前检查单。
- **P14 时间上限是设计值，不是实测。** 触发：R8 冻结。规则：每阶段记实际用时进 STATE；超时走 CHANGE-REQUEST 调上限。
- **P15 Seep 知识库数字 294/199 没法复核。** 触发：R4 Seep 清单。规则：在 Seep 真正签出（Track B）前，数字写“未核实（仓库外）”，不许写进完成标准。
- **P16 测试员与执行方抢 STATE。** 触发：测试阶段。规则：测试员只读 + 只写自己目录；启动测试员时执行方停写。
- **P17 上下文压缩漂移。** 触发：长任务执行中。规则：每阶段交接时另写一页“交接单”，不许只靠 STATE 一行。

## 16. 给 Davis 的执行提示词（30 行以内，复制就能用；续接，不重做）

```
读这个链接里的 FUSION-FINAL-v3.2.md，继续做，不要从头重做。
R1、R2 已经做完了（提交 81fc67e），从 R3 开始，做到 R9。
先把第 11 章的共享文件夹部署做出来，再做 R3–R8，
最后做第 12 章的 R9 独立测试（Pi 全新对话测，最多 3 轮）。
每个阶段做完都提交到 GitHub 仓库 gthubtom1/reverse-fusion-v2 的 main 分支，
核对远程提交号。做到 R9，或命中三种停下条件之一就停。
（链接由 Muse 发给你，见对话里的代码块）
```

注意：这份执行提示词里**没有第三个项目、没有绕过意图**，符合 Track B 的拆分要求。审计文件和 v3.2 正文可以写 Seep，执行提示词里不写。**续接说明：** 电脑上的智能体现在对话里已经在做 v3.1，Davis 把上面这句发到同一个对话里续接就行，不用新开对话，不用重做 R1、R2。

## 17. 冻结声明

- 这份文件就是 v3.2 最终版，版本号 v3.2，日期 2026-11-20。v2.1、v3、v3.1 冻结不动，留着。
- 执行中不许悄悄改顺序、不许加模块、不许开分支、不许开 PR、不许把方案拆成多个版本。
- 想改，先写 `CHANGE-REQUEST.md`，写清“想改什么、为什么、证据是什么”，等 Davis 批了再改。

## 18. 没核实的事（诚实清单，不许当成已证明）

1. Seep 的 MCP 服务器真跑起来是什么样（只数了工具，没跑过）；Seep 知识库 294/199 篇、`check_routing.py` 能不能跑（Seep 不在仓库里）。
2. 电脑上那 3 份安装拷贝是不是恢复后的完整版（不在仓库里，gitignore 也排除了）。
3. `tool-index.md` 有没有在电脑上生成过（只有模板；新克隆里没有）。
4. REA 的 JS/Android 工具在 Windows 上能不能跑（只证明了 PE 能、ELF 不能）。
5. 验证码在三个上游里有没有现成方法（Stage 10 只用了一篇笔记 + 一篇参考）。
6. 各阶段的时间上限是设计值，不是实测值；R9 的时间上限（T1 6 小时、复测各 3 小时）也是设计值。
7. 样本 3 + Seep（Track B）一次都没做过，不在 v3.2 的完成标准里（第 13 条不含 Track B）。
8. Codex / Pi 的全局技能目录和 MCP 配置文件位置（Linux 机器上核实不了，要在 Davis 电脑上确认）。
9. Claude Code 的 `.mcp.json` 支不支持 `"cwd"` 字段（要在 Davis 电脑上实测）。
10. 恢复清单的最终数（469 还是 467，按 §2 算法复核前写“未核实”）。
11. Pi 这个测试员实际能不能用（Davis 电脑上有没有 Pi、Pi 能不能开全新对话、能不能读共享文件夹）——没核实。
12. 原版样本文件能不能拷进快照（样本 1、2 现在不在仓库里，来源和分发限制没核实）。
13. v3.2 本身没有被执行过——它是一份修复计划，修完、跑通、Pi 测通过了才算数。

---

## 附录 A：冻结原文作废句对照表（v3 / v3.1 冻结原文不动，这里逐条作废）

| 位置 | 旧句（作废） | 替换句 |
|---|---|---|
| v3 §13.2 | “`compare_functions` 等在 Stage 1/3 真调过” | “只在工具列表里核实存在，未调用”（以 `USED-FUNCTIONS.md` 为准） |
| v3 §11.1 | “完整版已恢复，671 个文件” | “完整版已恢复，675 个文件”（数字本身仍按 §2 算法复核） |
| v3.1 §3.2 | “加不上 Seep 触发条件，就把 v2.1 §1.4 那句话删掉” | “触发条件只记在 `lifecycle/V31-C3-SEEP-TRIGGER.md`，v2.1 原文不动” |
| v3.1 §9.5 | “一直做到 R8，做到 100% 再停” | “做到 R8/R9，或命中三种停下条件之一就停” |
| v3.1 §10-10 | “全领域回归重跑过，无回归失败” | “回归重跑过，记录齐全；失败只追加记录、不改旧结论、不阻塞冻结” |
| v3.1 §10-7 | “44 个领域每个都有 verdict” | “42 个有 verdict，macOS/iOS 2 个待定（范围外，直到有设备）” |
| v3.1 §8 R0 | “开新分支做 v3.1” | “只打标签，v3.1/v3.2 就在 main 上做” |
| v3.1 §4 / §7.4 | “恢复 469 个”“范围外 19 个” | “恢复数未核实（按 §2 算法）”“范围外 21 个（O1–O21）” |

## 附录 B：部署检查单（可打印一页，见 §11.5）

1. 仓库 HEAD 对不对（`git rev-parse HEAD`）；2. 子模块初始化了没有（`git submodule status` 无 `-`）；3. 配置文件存在且路径一致；4. `.mcp.json` 只有一个 rea、args 绝对路径、有 `cwd`、同步等幂；5. 根指针文件指对了地方；6. 总控 + 路由表 + tool-index 都存在，路由回归两次退出 0；7. 全局技能指针只有 router 一个；8. REA 工具列表 `tool_count=260`，`rea doctor` 的 ghidra 相关 healthy；9. `check_state.py` 退出 0，STATE 的 `last_commit` 等于 HEAD；10. 搬家测试（如换过文件夹）。**10 条全过才算部署完。**

---

*依据：v2.1 全文（835 行）；v3 全文（599 行）；v3.1 全文（312 行）；仓库 gthubtom1/reverse-fusion-v2 提交 `81fc67e`（V3.1 R2，2026-11-20 06:28）；`FUSION-REVIEW-v3-AUDIT.md`（309 行）；部署复核报告（HEAD `81fc67e` 实测：无根 CLAUDE.md、无 .claude/skills/、.mcp.json 写死路径、子模块空、STATE 滞后）；独立测试员设计报告（HEAD `b8ccdcd` 实测：STATE 滞后、tool-index 不在仓库、路由回归无证据）；整合复核报告（C1–C15、P1–P17）。*

*老实说明：没有逐字逐行读完每一个文件。三个项目加起来快一万五千个文件，REA 一个 `src/` 就有 130 多万行。做的是“文件树全清点 + 关键文件全读 + 大文件结构化核对 + 明确列出没读的部分”（见 §18）。没读的部分，各阶段第一步补读。*
