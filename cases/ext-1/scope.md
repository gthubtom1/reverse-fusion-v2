# scope.md — cases/ext-1

**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过 / 部分通过 / 不通过」，不适用 L4/L5。**

- 目标：一个 MV3 浏览器扩展的签名算法（`tokenFor(pageUrl)`），解包 → 读 manifest → 定位 background/service_worker → 复现 → 5 用例对照。
- 类型：Chrome MV3 扩展 / background service worker 算法
- 样本：自建学习扩展 `cases/ext-1/target/`（`manifest.json` + `background.js`）；manifest 权限只有 `tabs`，无明显危害。符合「公开学习用、不用真实商业软件」的精神（本机经代理拉第三方扩展不稳，自建样本走通全流程）。
- 要做：解包分析 manifest/background → Node 复现 tokenFor → 5 用例浏览器原版 vs Node 双侧对照 → 比较器自检（改 SECRET）。
- 不做：不进行扩展的权限滥用/供应链调查；不自动安装到浏览器（用 chrome-devtools 在页面上下文执行其逻辑作原版基准）；不写 L4/L5。

## 测试集（事先写明）

| 用例 | 输入 URL | 原版输出 | 预期复现 |
|---|---|---|---|
| TC1 正常 | `https://example.com/x` | `644caad34542ba9011a983cb8a85888dd1c5e612ac232e` | 一致 |
| TC2 正常 | `chrome://settings/` | `723c9a228695309038f1c3e88b079ea851c11822` | 一致 |
| TC3 边界 | ``（空串，无字节） | `0000` | 一致 |
| TC4 无效/边界 | `https://a.b/c?q=1` | `644caad34542ba90011bb3834e2ca0c14373ef` | 一致 |
| TC5 篡改 | 改 SECRET 末字节 | → | 输出必须变（防背答案） |