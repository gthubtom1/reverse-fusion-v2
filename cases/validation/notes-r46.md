# 第 0 步逐条笔记：R46 独立复刻

来源：[锁定提交的 R46 文档](https://github.com/gthubtom1/reverse-skill/blob/ce675096e6a2cd4789a76f9bd618feddc2b6f333/skills/reconstruction/SKILL.md)。全文读取，有内容的最后一行为 L144。交接检查器仅静态核对，未运行。

## L0–L6 定义原文（L29–37）

| Level | Claim | Minimum evidence |
|---|---|---|
| 0 | target/protection triage | exact identity, format/protection observations and unknowns |
| 1 | readable decompilation/pseudocode | reproducible analysis output with addresses and limitations |
| 2 | key calls/data flow | Evidence-linked calls, data transformations and hypotheses |
| 3 | selected behavior model | observed inputs/outputs, states, error and boundary requirements |
| 4 | independent implementation passes core differential tests | frozen core scenarios executed against original and independent implementation |
| 5 | selected boundary/error/side-effect differential tests pass | required edge/state/regression surfaces pass with fresh proof |
| 6 | near-original source recovery | source/symbol/build inputs and provenance support the claim |

L39–41：L0–L3 是分析进度，L4/L5 是有限范围交付，L6 要原生来源与构建证据，不能只从反编译推断。错误变体是 L90 的比较器检查，不是 L5 的定义。冻结版 §5.4 的等级简写不能替代上游定义或扩大等价范围。

## 各节笔记

| 原文位置 | 要点及对冻结版的影响 |
|---|---|
| L1–9，定位 | 复刻、验收与追版；修改原件不属于独立实现。符合 §1.1。 |
| L11–21，前置 | 复用原案，先分已有成果验证、独立实现、材料评估；只有独立实现走完整规格链。机器检查与语义审查分开。 |
| L23–41，交接和等级 | 原案须有目标身份、范围、有证据的行为模型、未知及成功标准。专业 PRIMARY 先分析，同一案子进入 R46；不反对 §1.2。 |
| L43–53，工具 | Python 支持机械审查；REA、规格工具及运行环境各有资格要求；资料中的能力不是本机回执。 |
| L55–61，冻结输入 | 工具源码与成果分开；原案记录目标、我方产物、环境和版本化规格指针；追版按 O/C/N 工作。 |
| L63–76，证据 | 保留原始完整证据和引用；区分观测、推断、未知、设计；机械校验通过后仍要确认材料支持需求。 |
| L78–86，规格和实现 | 独立实现走上游指定的实际命令链；每批只保留一个写入方；候选结果和进程成功退出不是交付证据。 |
| L88–94，差分 | 固定输入、环境、比较规则，真实双侧采集并检查错误变体；变化可使旧证明失效。函数或产物结构比对不替代运行行为。 |
| L96–100，交付 | 规格符合、行为对照和独立运行分别出证据。上游还提及 `diagram-generator` 作为适用收尾，冻结版 §4.2 删除了它，后续不能默认仍可用。 |
| L102–114，自举 | R46 自身不注册宿主、不安装工具、不改配置；缺口如实记录。 |
| L116–120，语言 | 用户可见报告默认中文。 |
| L122–132，路由和分岔 | 取证后经原总控进入复刻；证据不足回专业模块，不建第二分类器。 |
| L134–144，自检 | 可追溯、机器检查、真实对照、独立运行和回滚各凭自己的证据，本轮未测者保持未测。 |

## Spec Kit 来源

- [上游工作流 L43](https://github.com/gthubtom1/reverse-skill/blob/ce675096e6a2cd4789a76f9bd618feddc2b6f333/skills/reconstruction/references/spec-kit-workflow.md#L43) 以官方 Spec Kit `v1.3.0` 为文档/源码核对基线。L7 写明 `integration`、`script` 按安装版官方帮助选择，本技能不硬编码宿主适配命令。因此冻结版 §5.4 的固定调用不是上游原文。
- [官方 `v1.3.0` 的 `pyproject.toml` L2–3、L22](https://github.com/github/spec-kit/blob/v1.3.0/pyproject.toml#L2) 定义包 `specify-cli`、包版本 `1.3.0`、命令入口 `specify`。仅核源码对应关系，未安装或验证 Codex/Pi 集成。
- R46 L80 的链路是 `constitution → specify → clarify → plan → tasks → analyze → implement → converge`。冻结版五步概要不是该流程的完整清单。

## `check_handoff.py` 的实际边界

[检查器 L219–260](https://github.com/gthubtom1/reverse-skill/blob/ce675096e6a2cd4789a76f9bd618feddc2b6f333/skills/reconstruction/scripts/check_handoff.py#L219) 与[交接格式 L21–70](https://github.com/gthubtom1/reverse-skill/blob/ce675096e6a2cd4789a76f9bd618feddc2b6f333/skills/reconstruction/references/handoff-manifest.md#L21) 显示：

- 实际路径为 `skills/reconstruction/scripts/check_handoff.py`，不是冻结版 §10.2 的 `tools/check_handoff.py`。它读项目内 JSON 指针清单，不读冻结版 §5.3 的 Markdown 表格。
- 查相对路径范围、原案上下文指针、同一规格功能项目录、文件 SHA-256、FR 映射唯一性及覆盖、证据/义务/未知项指针；显式关键未知可导致 `FAIL`。
- 不认证 REA 包的语义，不运行目标、复现命令或验证器，不核准授权、事实真伪或当前证明的新鲜度。结果仅为 `machine_check_only`，`semantic_verification` 和 `target_execution` 均为 `not_performed`，`authorization` 为 `not_assessed`。
