# 各领域回归重跑结果（Stage 11）

日期：2026-11-20。对 Stage 5–10 每个领域重跑一次它的 5 用例（只重跑，不修；失败记「回归失败」不改旧结论）。

| 领域 | 重跑命令 | 结果 | 回归 |
|---|---|---|---|
| JS/网页算法 (js-1) | `node cases/js-1/reimpl/differential_test.mjs` | ok=true，12 行（10 用例 + 2 未见输入探针）全过 | ✅ 无回归 |
| browser 扩展 (ext-1) | `node --input-type=module -e "…tokenFor…"` | 5 URL 输出确定为字符串且与 E-002 基准一致 | ✅ 无回归 |
| 验证码 (captcha-1) | `node --input-type=module "…token…"` | 5 表达式 token 与 E-002 基准逐字一致 | ✅ 无回归 |
| APK (apk-1) | `node cases/apk-1/reimpl/licensecheck.mjs`（validate 5 用例） | 前 3+2 用例与 JVM 原版一致（d8 限制不属回归） | ✅ 无回归（范围同原验收） |
| 协议 (protocol-1) | `cd cases/protocol-1 && node reimpl/decode.mjs`（decode 对照） | 依赖服务抓包；decode 5 帧预测与真实响应一致（证据 E-002） | ✅ 无回归 |
| 浏览器自动化 (automation-1) | chrome-devtools 观察 | 观察支撑（无 5 用例对象） | ✅ 不适用（非重做领域） |

结论：**无回归失败**。所有能重跑的领域重跑结果与各自验收证据一致；老验收结论未改。APK 的 d8 卡点与自动化的「观察支撑」性质在原验收里已如实记录，不构成回归失败。