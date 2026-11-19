# reverse-fusion-v2：第 0 步验证报告

日期：2026-11-20（北京时间）  
第 0 步结论：**不通过**。已停止在第 0 步，未开始第 1 阶段。

## 冻结文件与取证范围

下载的 `FUSION-FINAL-v2.md`：798 行，62,569 字节，头部标明 v2.0；SHA-256 `ec552239b3f3d1ec31e78fa341d00c870bf7492df82a2607bb422c44d6e90320`。这是本轮实测文件指纹，未与发布方另行签名比对。冻结文件未编辑。

| 项目 | 固定提交 | 实际核验 |
|---|---|---|
| reverse-skill | [`ce675096e6a2cd4789a76f9bd618feddc2b6f333`](https://github.com/gthubtom1/reverse-skill/commit/ce675096e6a2cd4789a76f9bd618feddc2b6f333) | 上游提交、未截断的文件树、两份 SKILL 全文及关键支撑文件已查。本地 HEAD 未建立。 |
| REA | [`4491c84c82140a43fa12390b727840a433875ba8`](https://github.com/morluto/rea/commit/4491c84c82140a43fa12390b727840a433875ba8) | 上游提交和文件树已查；`package.json` 与 `server.json` 都确认 `rea-agents` 6.9.0。本地 HEAD 未建立。 |
| Seep | [`1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e`](https://github.com/angusdevgo/Seep-Reverse-Lab/commit/1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e) | 上游提交、未截断的文件树、`VERSION` 1.15.0 及相关文档已查。本地 HEAD 未建立。 |

本轮只读取固定提交的资料和文件树，未完整拉下或签出三仓、未安装、未接线、未运行上游脚本或样本。可以核查普通软件的功能证据与对照验收；本轮不搭建、验证许可证绕过、密钥生成或自动规避保护的链路，也未为该链路选取可执行测试样本。

## §6.2：15 项逐项复核

`[x]` 仅表示这一项在标注的证据层面已核实，不表示运行成功。下表的路径行号以各项目固定提交为准，除明确注明的发布记录外不使用分支最新版作依据。

| # | 勾核 | 结果与证据 |
|---|---|---|
| 1 | `[x]` | **通过（文档）**。Seep [`CHANGELOG.md:13–26`](https://github.com/angusdevgo/Seep-Reverse-Lab/blob/1ea9399ccb4dd8db5849a5ff62d963bf4abbe35e/CHANGELOG.md#L13) 明确移出 Codex、Claude Code、OpenCode 的受支持客户端清单，只支持 Pi Agent 和 DeepSeek Harness。此结论限客户端支持口径，非兼容性实测。 |
| 2 | `[x]` | **通过（文档）**。Seep `AGENTS.md:18` 记载会话门，`Tool/skill/softseep/SKILL.md:46` 另立 G-Auth；reverse-skill `skills/ops/scope-contract.md:53–56,89` 记录自己的 `auth.status`。这是两套不同机制，未将其中任何一套用作放行。 |
| 3 | `[x]` | **通过（文档）**。reverse-skill `skills/SKILL.md:28–36` 声明唯一总控；Seep `Tool/skill/softseep/SKILL.md:2–3,75` 同样自称唯一入口。把两者同时作为首入口会产生职责重叠；未进行双入口运行。 |
| 4 | `[ ]` | **未核实**。首次拆解报告未随冻结文件提供，缺“正文”的路径、排除项和去重口径。不能确认 195 篇，也不把 294 等数字换成另一个未审定的数。 |
| 5 | `[x]` | **通过（快照不同步）**。按相对路径比较非截断 Git 树的 blob ID：Seep 两个子树分别 691、682 个 blob，同路径 596 个，其中 19 个内容不同。证明两份快照不等同；哪份被工作台运行读取未实测。 |
| 6 | `[ ]` | **未核实**。Seep `Tool/cases/` 的树有 248 个 blob，能定位多个 `build.ps1`；存在性不证明可构建，也不证明“多处报错”。未运行许可证相关案例脚本，拆解报告的失败记录亦未提供。 |
| 7 | `[x]` | **通过（静态差异）**。reverse-skill `skills/scripts/bootstrap-manifest.json` 登记 26 项；与 `bootstrap-reverse.sh:1215–1241` 的显式分发对照，差 `binaryninja`、`bkcrack`。前者在清单中是纯手动，后者的资产规则面向 Windows，不能把两项都当成应补的 Unix 自动安装。未运行任何启动脚本。 |
| 8 | `[ ]` | **不通过（复合断言有误）**。`README_zh.md:236` 为 175，`skills/tests/routing-benchmark.json` 的 `cases` 实数为 192；`docs/RELEASE-CHECKLIST.md:16` 为 25，清单实数为 26。`skills/routing_zh.md:261` 的 63 已核，78 的计数口径未核。`skills/config/routing.json:215,341` 明列 R44，路由优先级 45 项，R0–R46 实际缺 R42、R43。 |
| 9 | `[ ]` | **未核实**。缺 C 路原始文件与纳入标准；本轮未重做 27 份参考资料的逐条分母和状态统计。任何方法说明都未当成实测回执。 |
| 10 | `[ ]` | **部分通过**。REA `.agents/skills/reverse-engineer-anything/SKILL.md` 与 `.cursor-plugin` 的对应文件均为 674 行。未核 241 历史统计的原始来源，未取得固定版本在当前宿主的 `tools/list`，不声称存在或不存在仓内精确总数。 |
| 11 | `[x]` | **通过（文档）**。REA `docs/providers/windows-ghidra-p0.md:9–23` 写明 Windows x64 的实验性只读 P0、27 个操作。`docs/getting-started/installation.md` 的 Hopper 支持范围不包含 Windows 原生自动安装。未在本机启动任一引擎。 |
| 12 | `[x]` | **通过（术语不同）**。REA 的 SKILL 文档区分 Evidence、推断、局限及未知；reverse-skill `skills/SKILL.md:22,30–36` 用 Evidence→Finding→Path。可以用冻结版三档作摘要；三档不能取代原证据 ID、来源和原生状态。 |
| 13 | `[ ]` | **不通过**。锁定提交的 `CHANGELOG.md:9–11` 使用候选版措辞，但上游有[正式 `v1.9.0` Release](https://github.com/gthubtom1/reverse-skill/releases/tag/v1.9.0)（`prerelease: false`）。解析附注 tag 后指向 `7cc3109bf14a570c9c852dc76cce05fff424e88c`，不是冻结表的 `ce675096…`。正式发布存在和冻结提交未等同发布 tag 两件事同时成立；未改锁定提交。 |
| 14 | `[x]` | **通过（文档）**。Seep `Tool/aotopsy/README.md:23,318–330` 记录 Dart 2.10–3.13、实例字段名约 97–99% 缺失、局部及捕获变量名缺失。Flutter/AOT 输出不等于原源码；未运行该工具。 |
| 15 | `[ ]` | **部分通过**。Seep `Tool/scripts/master-route.ps1:16–26,160` 与文件树确认：脚本所求 `Tool/config/routing.json` 不存在，唯一 `routing.json` 在 `Tool/scripts/`；文中三个辅助脚本及 `MASTER-ROUTING.md` 未在树内找到。`check_routing.py` 并非整仓不存在：两个 `Tool/upstream/` 镜像各有一份；所抽的 `Tool/skill/apkseep` / `exe-reverse` 子树未见同名脚本。未跑路由或证明镜像脚本可替代。 |

汇总：8 项勾选（静态或文档层），2 项部分通过，2 项不通过，3 项未核实。未勾选是有意保留，不按失败或成功混算。

## 衔接与验收判断

- **对的部分**：单一总控在前、REA 是分析委派、原案返回 R46；总控 L28–36、L207 与 R46 L25、L41、L124–128 互相支持。安装顺序和执行顺序分写、检验独立运行、保留未知，都是有用的约束。本轮没有依据将 REA 或 Seep 前移。
- **错的部分**：§5.3 的 Markdown 不是原版检查器的输入；§5.4 的 L5 还需要所选边界、错误、状态或副作用的新鲜对照证据，抓到坏变体不足以独自达到 L5。L6 已有明确定义。§10.2 记错检查器路径；§4.5 与 §6.2 的 R44 和 §2 与 §6.2 的发布状态有实证反例。
- **REA 接口静态核验**：同提交 [`docs/getting-started/cli.md:925–955`](https://github.com/morluto/rea/blob/4491c84c82140a43fa12390b727840a433875ba8/docs/getting-started/cli.md#L925) 记有导入、规范化导出和证据比对；规范化是处理已存在的包，不等于从活动会话导出。 [`docs/reference/mcp-contracts.md`](https://github.com/morluto/rea/blob/4491c84c82140a43fa12390b727840a433875ba8/docs/reference/mcp-contracts.md#L28) 在 L28–29、L323、L981 分别记录 `compare_functions`、`compare_artifacts`、`export_evidence_bundle`、`compare_managed_members`。冻结版的两个“待核实”名字在固定提交文档中找得到；当前宿主是否真实发布这些工具、输入格式和返回值均未实测。
- **不同意的部分**：不能把 Markdown 表格完整、产物清单相似、五条只覆盖正常输入的用例当成完整行为验收。也不认同用本轮文档核对结果背书许可证绕过或自动规避保护流程。各项修订见 `REVIEW-2.md`；没有改原方案或更换样本。

## 阶段出口

两份全文笔记、独立复核和逐项记录已交。本地三仓 HEAD、真实运行接口、保护相关样本以及第 3 阶段的对照测试未验证。样本核验状态单列于 `cases/samples/MANIFEST.md`。第 9 节 10 条是最终验收项，本轮不提前签字。未安装、未生成融合代码、未开分支或 PR，停在第 0 步。
