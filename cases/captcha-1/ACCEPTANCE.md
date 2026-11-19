# 验收报告：cases/captcha-1（Stage 10）

**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过」。不适用 L4/L5（本模式不要求）。**

## 0. 结论（两行分写）
- 第一行（本模式结论）：**算法抽取：通过**。
- 第二行（R46 结论）：R46 L4：不适用（模式 3）；L5：不适用。

## 1. 前置门与上游方法

- 前置门：Stage 5–9 无「不通过」项（列表见 MANIFEST）——**门通过**。
- 上游方法：确认存在 `field-journal/2026-07-05_dsl-vm-captcha-reverse.md`（DSL VM 逆向模式）+ `browser-automation/references/distilled-captcha-evidence.md`。本案例用其「常量表 + 函数追踪 + 导出」思路在自有测试验证码上实践。

## 2. 做了什么

- 自建学习验证码（`captcha-1/target/`）：Canvas 画算术题，`compute()/token()` 确定性生成答案 token。
- 原版基准：chrome-devtools 打开页面，取 `token()` 对 5 组 (a,op,b) 真跑。
- 复现：`reimpl/captcharepro.mjs` 独立 Node 重写（不 eval 页面脚本）。
- 对照：5 用例双侧全一致（`ALL_MATCH true`）。

## 3. 双侧对照（evidence/E-002-differential.json）

| 用例 | 表达式 | 答案 | 原版 token | 复现 token | 一致 |
|---|---|---|---|---|---|
| TC1 | `8+5` | 13 | `08d5dd28` | 相同 | ✅ |
| TC2 | `3*7` | 21 | `fa8d20df` | 相同 | ✅ |
| TC3 | `10-4` | 6 | `b54af524` | 相同 | ✅ |
| TC4 | `7%3` | 1 | `9e332aeb` | 相同 | ✅ |
| TC5 | `0+0` | 0 | `00000000` | 相同 | ✅ |

## 4. 独立运行 + 比较器自检

- Node 复现独立运行，不依赖页面文件。
- 比较器（改 `40503→40504`）：4 组非零输入 token 全变化；`0+0` 恒 `00000000` 为全零输入语义（a,b,ans 全 0 时混合项为 0）。判定 `ok=true`，非背答案。

## 5. 未验证 / 未知

见 `unknowns.md`。

## 结论

**算法抽取：通过**。前置门与上游方法都过核查；5 用例双侧全一致、独立运行、比较器自检通过。未宣称 L4/L5。