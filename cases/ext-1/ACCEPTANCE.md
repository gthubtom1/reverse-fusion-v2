# 验收报告：cases/ext-1（Stage 7）

**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过」。不适用 L4/L5（本模式不要求）。**

## 0. 结论（两行分写）
- 第一行（本模式结论）：**算法抽取：通过**。
- 第二行（R46 结论）：R46 L4：不适用（模式 3）；L5：不适用。

## 1. 做了什么

- 解包分析：`target/manifest.json`（MV3，permissions `tabs`，service_worker `background.js`）→ 定位 `background.js` 里的 `tokenFor(pageUrl)`。
- 原版基准：chrome-devtools 页面上 `fetch('/background.js')` + `new Function` 加载原扩展脚本，调用 `tokenFor` 对 5 个 URL 真跑输出（这就是扩展逻辑在浏览器上下文里运行的「原版」）。
- 复现：`reimpl/extrepro.mjs` 独立 Node 重写（不 eval/require 扩展文件）。
- 比较器自检：`reimpl/comparator_check.mjs` 改 SECRET 末字节。

## 2. 双侧对照（浏览器原版 vs Node 复现，5 用例）

evidence/E-002-differential.json：

| 用例 | 输入 URL | 原版 | 复现 | 一致 |
|---|---|---|---|---|
| TC1 | `https://example.com/x` | `644caad3…32e` | 相同 | ✅ |
| TC2 | `chrome://settings/` | `723c9a22…22` | 相同 | ✅ |
| TC3 | ``（空） | `0000` | `0000` | ✅ |
| TC4 | `https://a.b/c?q=1` | `644caad3…ef` | 相同 | ✅ |
| TC5 篡改 | 改 SECRET(0x33→0x44) | 输出必变 | `644caad3459f…` | ✅ |

真实原版输出逐字记录在 `evidence/E-002-differential.json.original_outputs`；Node 复现逐字一致（命令：`node --input-type=module -e "...tokenFor..."`，得分 `ALL_MATCH true`）。

## 3. 独立运行 + 不依赖原文件

- Node 复现独立运行，不读扩展文件、不依赖浏览器。
- 防背答案：改 SECRET 后 4 个非空 URL 的 token 全部变化 → 抽取的是参数化算法，不是背下来的答案。空串恒 `0000` 是无输入字节的算法语义。

## 4. 限制 / 未验证

- 未把扩展真正加载进 Chrome 运行时（`chrome://extensions`「加载解压扩展」需要 GUI，自动化未做）；这里把浏览器页面里的 `tokenFor` 执行等价视为「扩展逻辑运行」。
- `chrome.action.onClicked` 的监听未实际触发验证（空实现接受）。
- 未做扩展级权限面/网络钩子的全量分析（v3 Stage 7 的重点是「解包 + 复现关键逻辑」，本案例聚焦 token 算法）。

## 结论

**算法抽取：通过**。5 用例双侧全一致、独立运行、比较器自检（防背答案）通过。未宣称 L4/L5。