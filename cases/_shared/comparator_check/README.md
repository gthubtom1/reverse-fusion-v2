# 共享比较器（v3.1 R6：先找工具再写脚本）

把各领域唯一的「改一个常量、看输出变不变」检查收敛到一份。每领域只需一个适配参数文件，不再每案重写。

用法：
- 每个领域的 `reimpl/comparator_check.<ext>` 改为 `import` 这里的共享入口，传入本领域的 `normal_fn`/`tampered_fn` 和输入集。
- 判定规则统一：正常通过的候选在 tampered 后必须变（防背答案）；本来就失败的输入保持失败属正确语义。

各领域曾经的 7 份单独比较器（sample-1/js-1/apk-1/ext-1/protocol-1/captcha-1/netwin-1）由 R6 合入后保留原文件（历史证据），但新案验收统一引用本目录，不许再新写一份。

## 工具单先行（第 6 条）

写任何新比较器前，先查 REA 260 工具（cases/stage1/tools-list-rea.json）、reverse-skill 技能方法、Seep 工具单。有现成比对工具（compare_functions 等）优先用；没有才自写，自写前在验收里写“查过了，没有这个工具，因为……”。
