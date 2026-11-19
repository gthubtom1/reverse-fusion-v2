# Codex 往返回执 — 样本 1（v3.1 §5.1 第 4 条）

日期：2026-11-20。

## 输入给 Codex 的

- `cases/sample-1/reconstruction-handoff.md`（交接单，含关键算法、行为清单、5 用例、证据 E-005/E-006）
- `cases/sample-1/notes/handoff-manifest.json`（机器清单，PASS）
- 规格链 `specs/001-xor-v1/`（spec/plan/tasks，FR-001..003）

## Codex 写实现（独立实现）

`cases/sample-1/reimpl/validator.py` — 从交接单算法独立实现：

- `validate(raw)`: 按空白分词 → 长度==6 → 每字节 `== [0x38,0x27,0x64,0x66,0x66,0x62][i] ^ 0x55`。
- `differential_test.py`: 5 用例（TC1..TC5）原版 CrackMe.exe vs 该实现，双侧对照。
- 边界：`cin >>` 分词语义（B3/B6 通过）。

（注：本项目无真实 Codex 会话历史，回执以「电脑智能体按交接单实现的交付物 + 对照记录」为准，如实不冒充 Codex CLI 会话。）

## 对照结果（回执内容）

`python -I cases/sample-1/reimpl/differential_test.py D:/tmp/fusion-samples/s1/CrackMe.exe cases/sample-1/evidence/E-006-differential.json`

```
{"all_match": true, "original_runnable": true,
 "decisions": [["TC1","accepted","accepted"],["TC2","denied","denied"],
               ["TC3","denied","denied"],["TC4","denied","denied"],
               ["TC5","denied","denied"]]}
```

边界：`boundary_test.py` → 6/6 all_match（E-008）。
比较器：`comparator_check.py` → detected_difference=true（E-007）。

## 结论

实现按交接单产出，5 用例原版/新版全一致；E 号引用（E-005/E-006）真实存在且经检查器 PASS。L4 通过、L5 未声明（控制台副作用未复刻）——按 v3.1 四档写「未做」。