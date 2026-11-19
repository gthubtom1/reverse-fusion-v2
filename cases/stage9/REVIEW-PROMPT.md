# 复核提示词（给规划智能体 / 放在主对话里用）

> 用法：把下面整段复制到主对话，让智能体.ddi 按它复核。它引用的仓库是 `D:\Project\最终版聚合`（即 gthubtom1/reverse-fusion-v2 的本地签出）。

---

你是一名规划与验收智能体，任务是**独立复核 reverse-fusion-v2 项目「链路是否真的走了 REA / reverse-skill / Seep」**。你只信仓库里的文件与命令输出，不采信对话自述。复核要回答的唯一问题是：

> 今天所有测试（样本 1、样本 2 及 js/apk/扩展/协议等）里，哪些环节真的调用了 REA、reverse-skill 或 Seep？哪些没有？没有的环节对「链路成立」意味着什么？

## 一、你要核对的仓库证据（先读，再判）

1. `FUSION-FINAL-v2.1.md` §1.2、§7：把「应该走什么链路」定下来（总控→REA→(Seep)→R46→REA 比对）。
2. 每一份案例时间线：`cases/<case>/timeline.md`（看有没有写 REA / Seep / router）。
3. 每一份案例证据目录：`cases/<case>/evidence/`（判断证据是 REA 返回的 JSON，还是自写脚本产物）。
4. `lifecycle/DECISION-LOG.md`：为什么样本 2 绕开 REA、为什么 JS 等用自建。
5. `cases/stage9/LINKAGE-AUDIT.md`：这是我方已写的归属结论，你要**独立复核它是否属实**，不要直接抄。

## 二、可复跑的命令（在你本机执行）

```bash
# 1) REA 真正产出了 evidence 的文件（应只有 sample-1，加 sample-2 的 overview）
grep -rlE '"evidence_id"|"open_binary"' cases/*/evidence/

# 2) 含 reverse-skill 总控驱动痕迹（应只有安装文档，没有任何真实案例）
grep -rliE 'master-route|case-init' cases/ lifecycle/

# 3) check_handoff 是否对真实案子跑过（应只有对上游示例 synthetic-project 的记录）
grep -rli 'check_handoff.py' cases/ lifecycle/

# 4) 每个案例时间线里 REA/Seep/router 是否被提及
for c in sample-1 sample-2 js-1 apk-1 ext-1 protocol-1; do
  echo "== $c"; grep -iE 'rea|seep|router|master-route' cases/$c/timeline.md 2>/dev/null
done

# 5) 每个案例的 reimpl 是否引用了 engine/rea 或上游包（js/ext 那些应是纯本地脚本）
grep -rliE 'engine/rea|require\(.rea' cases/*/reimpl/ 2>/dev/null
```

对每一条命令的**实际输出**，逐条标注：`真实证据` / `未发现` / `只出现在文档而非运行`。

## 三、必须回答的 5 个判定

1. **样本 1**：REA 是否真被调用？（看 `E-002~E-005` 有没有 `evidence_id` 和 provider=ghidra）
2. **样本 2**：REA 做到了哪一步？绕开后的 Ghidra headless + gdb + Unicorn 是不是「没走 REA 但合理」？
3. **js/apk/扩展/协议**：这几个的 `evidence/` 里有没有任何 REA 返回？如果没有，它用的是不是纯自建脚本？
4. **reverse-skill 总控**：有没有任何一个案例是被 `master-route`/`case-init` 驱动的？还是它只是躺在 `core/` 当手册？
5. **Seep**：有没有任何一次真实抽取调用？还是全部是「以后再说、未使用」的静态登记？

## 四、输出格式（写进新文件 `cases/audit-<日期>.md`，并更新 `VALIDATION-REPORT.md` 或你的复核报告）

- 一张表：案例 × {REA真实调用 / reverse-skill总控驱动 / Seep抽取}，三列各自 ✅/⚠️/❌。
- 一句结论：「原生链路是否成立」，「成立」的定义是：**至少一个案例里 REA 真产出 evidence、总控真驱动过、Seep 按需触发过**。请按这个定义给「成立 / 不成立 / 部分成立」，并给出证据行号。
- 再用一句话回答：**如果 JS/APK/etc 全没走 REA，那它们算不算「走通了我们的流程」？** 请从「模式 3 验收口径 vs 原生 R46 链路」两个角度分别说明。

以本提示词为任务，以仓库和命令输出为唯一事实来源。