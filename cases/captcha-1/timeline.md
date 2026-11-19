# timeline.md — cases/captcha-1

- 2026-11-20 06:5x 前置门核查：Stage 5–9 状态（JS 通过/APK 部分/扩展通过/协议通过/自动化通过）无「不通过」→ 门通过。
- 06:5x 上游方法核查：`field-journal/2026-07-05_dsl-vm-captcha-reverse.md` + `browser-automation/references/distilled-captcha-evidence.md` 存在。
- 06:5x 自建算术验证码 `target/`；浏览器打开真跑 token 5 用例基准。
- 06:6x Node 复现 `captcharepro.mjs`，对照 `ALL_MATCH true`。
- 06:6x 比较器自检（改 40503→40504）→ ok=true。
- 结论：算法抽取**通过**。清理：从 js-1/target 移除 captcha.html/captcha.js。