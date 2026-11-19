# 验收报告：样本 1

日期：2026-11-20（北京时间）。标准按 `FUSION-FINAL-v2.1.md` §5.4、§5.5。

**R6（v3.1）复用检查（2026-11-20）：** 先查工具单（REA 260 工具 `cases/stage1/tools-list-rea.json`）——比对/验证类有 `compare_functions`、`compare_artifacts`、`export_evidence_bundle`（R3 已真调成功）；比较器自检这类「改常量看输出变」没有现成专用工具，故自写（`reimpl/comparator_check.py`），但**只写一份，R6 起统一引 `cases/_shared/comparator_check/compare.py`，不再每案重写**。

**R3（v3.1）REA 验证链真调记录（2026-11-20）：** 在 REA 会话内对样本 1 真调：
- `export_evidence_bundle` → **成功**，导出 `E-010-exported-bundle.json`（含 ev_23cd8d78… 与 ev_646685c7… 两条记录）；
- `compare_functions`（left=ev_261a5d8f…[main]，right=ev_cdf672b5…[check]，同会话 analyze 后 retained）→ **成功**，返回 `ev_9e0b4ab3…`（rea-function-comparison，30KB 比较证据，E-012）；
- `build_reconstruction_obligation_ledger` / `verify_reconstruction` / `evaluate_reconstruction_coverage`：**未成功调用**——参数需本会话现场构造的 bundle/manifest/coverage 结构化对象，无法从外部拼接；已记录原因（工具需店内构造输入，见 E-012 同一会话的输出）。这满足 v3.1 §5.1「结果或确切报错记进验收」。

**复核重跑（2026-11-20 04:49）：** 按 README 复现命令重跑五个核心用例，`all_match: true, original_runnable: true`，判定结果与首次一致（TC1 accepted, TC2–TC5 denied）。本次重跑未改任何实现或样例。既有 `evidence/E-006-differential.json` 已由本次命令重新生成覆盖。

**结论：L4 通过（5/5 核心用例一致）；L5 未声明通过**，原因是只补了部分边界面，且独立实现没有复刻控制台副作用（标题、颜色、等待回车）。按 v2.1，不能把「抓到一个坏变体」或「结构相似」当成 L5。

## 1. 结构比对

- REA/Ghidra 12.2 识别为 `pe`、`x86_64`，函数 701 个（含导入）。证据 `evidence/E-002-procedures.json`（`ev_e4bd46c8…`）。
- 关键函数：`FUN_140017cd0`（main）、`FUN_1400173d0`（校验）。证据 `E-004`、`E-005`。
- 结构比对只说明定位正确，不作为行为等价证据。

## 2. 双侧行为对照（L4 核心）

| 用例 | 输入 | 原版 | 独立实现 | 一致 |
|---|---|---|---|---|
| TC1 | `mr1337` | accepted | accepted | 是 |
| TC2 | `mr1338` | denied | denied | 是 |
| TC3 | `MR1337` | denied | denied | 是 |
| TC4 | `mr133` | denied | denied | 是 |
| TC5 | `mr13377` | denied | denied | 是 |

命令：`python -I cases/sample-1/reimpl/differential_test.py D:/tmp/fusion-samples/s1/CrackMe.exe cases/sample-1/evidence/E-006-differential.json`
输出：`{"all_match": true, "original_runnable": true, ...}`
原始 stdout、退出码：`evidence/E-006-differential.json`。

## 3. 边界 / 错误 / 副作用（L5 面）

| 用例 | 输入 | 原版 | 独立实现 | 一致 |
|---|---|---|---|---|
| B1 | 空输入 | denied | denied | 是 |
| B2 | `m` | denied | denied | 是 |
| B3 | `mr1337 `（尾随空格） | accepted | accepted | 是 |
| B4 | `mr1337x` | denied | denied | 是 |
| B5 | 64 个 `x` | denied | denied | 是 |
| B6 | `mr1337\r` | accepted | accepted | 是 |

第一轮 B3、B6 不一致（独立实现没有模拟 `cin >>` 的空白分词）；补上分词后 6/6 一致。这正是 L5 边界面的价值。证据 `evidence/E-008-boundary.json`。

**副作用面没有复刻**：控制台标题 `CrackMe v1.2`、横幅、颜色、`[*] Press Enter to exit...` 的等待行为，独立实现都不产生。因此 L5 不成立。

## 4. 独立运行

`python -I cases/sample-1/reimpl/validator.py mr1337` 输出 `accepted`；`validator.py nope12` 输出 `denied`。不依赖原程序。

## 5. 比较器自检

把异或键从 `0x55` 改成 `0x54` 得到故意做坏的变体，跑同一组用例：

```
{"detected_difference": true, "mismatches": ["mr1337"]}
```

证据 `evidence/E-007-comparator-selfcheck.json`。这只证明比较器能发现差异，不单独等于 L5。

## 6. 未知项

见 [unknowns.md](unknowns.md)。未把静态结论写成运行时事实。

## 7. 判定

- L4：**通过**。5 个核心用例原版/独立实现一致，证据新鲜，独立实现可单独运行。
- L5：**未通过 / 未声明**。边界与错误面 6/6 一致，但控制台副作用未复刻，且未验证所有残留未知。
- 未使用 Seep；样本 1 没有许可证校验或加壳，按 v2.1 §1.4 跳过。
