# Stage 10 验证码样本登记

日期：2026-11-20。

| 编号 | 样本 | 难度 | 来源 | 代表什么 |
|---|---|---|---|---|
| captcha-1-simple | 自建算术验证码（Canvas + 确定性 token） | 简单 | 本仓库 `cases/captcha-1/target/` | 前端验证码的答案推导（token 算法）；代表「前端验证码的定位与本地复现」的最小场景 |

## SHA-256

```bash
sha256sum cases/captcha-1/target/index.html cases/captcha-1/target/captcha.js
```

记录于 `evidence/E-000-hashes.txt`。

## 说明

- 自建学习样本；未触碰真实验证码服务（v3 §7 Stage 10 明确「只用自己的测试验证码」）。
- 上游方法来源：`core/skills/field-journal/2026-07-05_dsl-vm-captcha-reverse.md`。