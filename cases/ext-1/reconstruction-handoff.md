# 复刻交接单 — 浏览器扩展 token 签名算法（ext-1）

target: MV3 扩展 token 签名算法（自建学习扩展）
source: evidence E-002（对照 JSON）
case: cases/ext-1
模式: 算法抽取（模式 3），不适用 L4/L5

## 抽的是哪一段算法

- 入口：扩展 `background/service_worker`（`background.js`）里的 `tokenFor(pageUrl)`
- manifest：`manifest_version 3`、`permissions: ["tabs"]`、`background.service_worker: background.js`
- 算法：
  - 对每个字节：`b = rotl8((byte ^ SECRET[i%6]), (i%7)+1)`；`acc = (acc + b) & 0xff`
  - 末尾补 2 字节：`rotl8(acc, 3)`、`rotl8((acc ^ len) & 0xff, 5)`
  - 输出：每字节转 2 位 hex 拼接
  - SECRET = [0x5a,0x67,0x21,0x4d,0x59,0x33]（"Zg!MY3"）

## 复现

- `reimpl/extrepro.mjs`：独立 Node 复现（不读/不 eval background.js）。
- `reimpl/comparator_check.mjs`：改 SECRET 末字节后 token 变；空串恒定 0000 为语义。

## 测试用例（见 evidence/E-002-differential.json，双侧对照全过）

| 用例 | 输入 | 原版 | 复现 | 一致 |
|---|---|---|---|---|
| TC1 | `https://example.com/x` | ✓ | ✓ | ✅ |
| TC2 | `chrome://settings/` | ✓ | ✓ | ✅ |
| TC3 | ``（空） | `0000` | `0000` | ✅ |
| TC4 | `https://a.b/c?q=1` | ✓ | ✓ | ✅ |
| TC5 | 改 SECRET | 必变 | 变 | ✅ |

## 未知清单

见 `unknowns.md`。