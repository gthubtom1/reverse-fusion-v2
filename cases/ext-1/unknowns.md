# unknowns.md — cases/ext-1

- 样本为**自建 MV3 扩展**（manifest + background），非第三方 crx/xpi 抓包。真实第三方扩展（如商店里的开源扩展）下载/解包面未测。
- 扩展未实际加载进 Chrome（自动化无法 GUI 操作 `chrome://extensions`）；把浏览器页面里 `tokenFor` 的执行等价视为原版运行。`chrome.action.onClicked` 监听未触发验证。
- 未分析扩展的 storage/IndexedDB 密钥、网络拦截（webRequest）、`<all_urls>` 等高权限路径——本案例只取核心 token 算法。
- 未验证 MV2 扩展或 Firefox xpi 的不同结构。
- 浏览器原版基准依赖本地 HTTP 服务器服务 background.js；改成别的方式加载扩展需另行验证。