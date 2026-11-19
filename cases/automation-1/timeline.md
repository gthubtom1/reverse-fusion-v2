# timeline.md — cases/automation-1

- 2026-11-20 06:4x chrome-devtools 打开 `http://127.0.0.1:8765/index.html`。
- 06:4x 观察页面加载请求（index.html + sig1.js）；填输入并点击 compute → 输出 sig1 token。
- 06:4x fetch `/index2.html` → 200、7ms；网络面板录到 reqid 10/11/12，请求/响应头与 body 齐。
- 结论：观察支撑**通过**。