# 链路归属复核报告：每个测试到底走没走 REA / reverse-skill / Seep

日期：2026-11-20（北京时间，复核）
复核方式：逐案检索本仓库已提交证据，不采信对话自述。
结论先行：**只有样本 1、样本 2 走了 REA**；JS / APK / 扩展 / 协议这四个「模式 3」案例**没有走 REA**，而是自建样本 + 手写脚本 + 双侧对照。reverse-skill 在整个执行期**从未以「路由/总控」身份真实驱动过任何案例**（仅在 Stage 5A 恢复文件，作为手册存在）。**Seep 从未被调用**（样本 1/2 明确记为「未使用，以后再说」）。

下面每条都有证据文件可查。

---

## 0. 本仓库要验证的「链路」是什么

按 `FUSION-FINAL-v2.1.md` §1.2 与 §7：

```
总控(reverse-skill 路由) → REA 分析 → (硬骨头才叫 Seep 提取件) → R46 复刻 → REA 比对验收
```

也就是说，「走了我们的流程」至少须满足三点之一，并留下证据：
1. **REA 真实被调用**（`open_binary`/`analyze_function`/`list_procedures` 等，返回带 `evidence_id` 的记录）；
2. **reverse-skill 真实以总控身份驱动**（`master-route` / `case-init` / `check_handoff` 对真实案子运行）；
3. **Seep 真实被调用**（`exe-reverse`/`apkseep`/`aotopsy` 等抽取件）。

以下逐案核对。

---

## 1. 样本 1（XOR CrackMe）—— ✅ 真正走了 REA

证据（`cases/sample-1/evidence/`）：
- `E-002-procedures.json`：REA `open_binary` + `list_procedures` 返回，含 `evidence_id: ev_e4bd46c8…`、`provider: ghidra 12.2`。
- `E-004-main.json` / `E-005-check.json`：REA `analyze_function`，`normalized_result.pseudocode` 为 Ghidra 反编译，证据 ID `ev_cdf672b5…`。
- `wiring-transcript.json` / `E-REA-COMPLETE.json`：REA MCP `get_evidence_bundle` 完整证据包。
- 复现（`reimpl/validator.py`）与差分/比较器由脚本跑，但**分析来源是 REA**。

判定：分析侧 = REA。逆向链路的「REA」环节真实存在。

## 2. 样本 2（ELF keygen）—— ⚠️ 部分走 REA，分析绕开 REA 的 ELF

证据（`cases/sample-2/evidence/`）：
- `E-002-overview.json`：REA `open_binary` 识别 `format: elf`、`architecture: x86_64` —— REA 有调用。
- 但后续 `binary_overview` 返回 `target_format_unsupported`（Windows Ghidra P0 只收 PE/MZ，`DECISION-LOG.md` D7）。
- 因此分析改成 Ghidra 12.2 headless（`ghidra/dump.txt`）+ gdb 断点 dump（`E-004-*.bin`）；复现用 Unicorn 模拟机器码（`DECISION-LOG.md` D8）。

判定：分析侧 = REA 只做了识别，**主分析是 Ghidra headless + gdb + Unicorn**（非 REA）。这是 REA 的平台限制导致，不是「没走 REA」的偷懒，但事实是 REA 只占了很小一部分。

## 3. JS、APK、扩展、协议（模式 3 案例）—— ❌ 没有走 REA、没有走 reverse-skill、没有走 Seep

逐案核对：

| 案例 | REA 证据 | reverse-skill 路由证据 | Seep 证据 | 实际方法（证据） |
|---|---|---|---|---|
| `js-1` | 无（`evidence/` 无 evidence_id/open_binary） | 无 | 无 | 手写 Node 复现 `sig1repro.mjs`/`sig2repro.mjs` + 双侧差分 `E-002-differential.json` |
| `apk-1` | 无 | 无 | 无 | jadx 反编译 `MainActivity.class` + Node 复现 + JVM 5 用例对照（`timeline.md`） |
| `ext-1` | 无 | 无 | 无 | chrome-devtools `new Function` 加载原版 `background.js` + Node 复现（`timeline.md`） |
| `protocol-1` | 无 | 无 | 无 | tshark 抓 loopback + Node decode.mjs（`timeline.md`） |

这些案例用了「scope / 差分 / 比较器」这套**验收剧本**（模式 3 的口径），但**分析引擎不是 REA，路由不是 reverse-skill，也没有叫 Seep**。它们是「自建学习目标 + 手写脚本 + 双侧对照」，正确但**不是** v2.1 §1.2 那条「总控→REA→（Seep）→R46→REA 比对」的原生链路。

## 4. reverse-skill：从未以总控身份驱动过案子

- 全仓库没有 `master-route` / `case-init` 对你真实案子的运行记录（搜 `cases/*/`、`lifecycle/` 的 `master-route`、`router` 调用，只有 `cases/stage1/STAGE1-REPORT.md` 提到「总控模型」但这只是安装报告文档）。
- `check_handoff.py` 只在 Stage 3 对 `core/skills/reconstruction/examples/synthetic-project`（上游自带的示例）跑过一次（`cases/stage3/checker-example.txt`），**从未对真实案子运行**。
- Stage 5A 把 `core/` 恢复成 reverse-skill 完整版（675 文件），但它是**当手册/静态文件**放着的，没有作为路由执行器被调用。

判定：reverse-skill 作为「总控/R46 手册」存在于仓库，**真实执行路径里没有它驱动的环节**。

## 5. Seep：从未被调用（合理，但事实是没有）

- 样本 1/2 的 ACCEPTANCE 都写明「未使用 Seep」（`cases/sample-1/ACCEPTANCE.md:66`、`cases/sample-2/ACCEPTANCE.md:55`）。
- `lifecycle/MANIFEST.yaml` 里 Seep 只是**静态登记**（版本、提交号、`do_not_use` 项），没有任何抽取件运行记录。
- 按 D2，Seep「以后再说」，所以没调用是**决定而非事故**；但确凿地讲：**整条链路里 Seep 从未发生过**。

---

## 6. 结论

| 环节 | 样本 1 | 样本 2 | js/apk/ext/protocol |
|---|---|---|---|
| 建案/scope | ✅ 有 | ✅ 有 | ✅ 有（模式 3） |
| REA 分析 | ✅ 真走 | ⚠️ 仅识别，主分析绕开 | ❌ 无 |
| reverse-skill 总控驱动 | ❌ 无 | ❌ 无 | ❌ 无 |
| Seep 提取件 | ❌ 无（合理跳过） | ❌ 无（合理跳过） | ❌ 无 |
| 复现/差分/比较器 | ✅ | ✅ | ✅（手写脚本） |

**一句话：**「REA 分析 → 复现 → 差分 → 比较器」这条**验收意义上的链路**在样本 1 完整成立、在样本 2 部分成立；但「reverse-skill 当总控驱动、REA 当引擎、Seep 兜底」这条**执行意义上的原生链路**，在全部 6 个案例里都**没有真正跑完整过**——JS/APK/ext/protocol 全凭手写脚本，REA 只服务了样本 1（和样本 2 的识别）。

这不是「全部都没走」，也不是「全部走了」。是**一半真、一半自建**。复核者请以此为准，不要再从对话自述推断。

---

## 7. 复核者请自行验证的操作

```bash
# REA 真正产出了 evidence 文件的，只有这些：
grep -rlE '"evidence_id"|"open_binary"' cases/*/evidence/

# 含 REA provider 返回的 JSON：
cat cases/sample-1/evidence/E-004-main.json | head -40

# reverse-skill 总控驱动 = 全仓库搜索，仅安装报告里出现：
grep -rliE 'master-route|case-init' cases/ lifecycle/

# check_handoff 只对上游示例跑过（非真实案子）：
cat cases/stage3/checker-example.txt

# 六个案例的时间线，核对有没有写「REA」：
for c in sample-1 sample-2 js-1 apk-1 ext-1 protocol-1; do echo "== $c"; grep -iE 'rea|seep|router' cases/$c/timeline.md 2>/dev/null; done
```

复核提示词由规划智能体执行；本报告作为第一批证据。