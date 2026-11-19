# scope.md — cases/captcha-1

**第一行（C4）：模式 3 算法抽取（自有验证码）；第一个工具：`js-reverse_list_scripts` 先试（js-reverse_* MCP）；装不上走浏览器观察 + Node 复现。**

**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过 / 部分通过 / 不通过」，不适用 L4/L5。**

- 前置门：Stage 5–9 无「不通过」（JS通过/APK部分/扩展通过/协议通过/自动化通过）——**门通过**。
- 上游方法核查：三个上游里有现成验证码方法——`field-journal/2026-07-05_dsl-vm-captcha-reverse.md`（DSL VM 逆向模式：case 提取→opcode 分类→常量表→函数追踪）和 `browser-automation/references/distilled-captcha-evidence.md`。**方法存在**。
- 目标：自有测试验证码（Canvas 算术 + 确定性 token），用上面方法定位答案推导算法并在 Node 复现。
- 类型：前端验证码（算术 = 简单图形验证码模拟）
- 要做：浏览器真跑原版 token → Node 复现 → 5 用例对照 → 比较器自检。
- 不做：不攻击任何真实验证码服务；不写 L4/L5。

## 测试集（5 用例）

| 用例 | 表达式 | 答案 | token 基准 |
|---|---|---|---|
| TC1 正常 | `8+5` | 13 | `08d5dd28` |
| TC2 正常 | `3*7` | 21 | `fa8d20df` |
| TC3 正常 | `10-4` | 6 | `b54af524` |
| TC4 边界 | `7%3` | 1 | `9e332aeb` |
| TC5 无效/边界 | `0+0` | 0 | `00000000` |

修改 40503→40504 后 token 必须变（防背答案）。