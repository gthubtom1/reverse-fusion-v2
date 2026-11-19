# 观察记录 — cases/automation-1（Stage 9 浏览器自动化）

日期：2026-11-20。对象：Stage 5 的 JS 测试页（`cases/js-1/target/index.html`，本地服务器 `http://127.0.0.1:8765`）。

## 做了什么（自动化观察，非独立重做）

1. chrome-devtools 打开 `http://127.0.0.1:8765/index.html`（页面 JS Signature Lab 1）。
2. 观察页面加载的网络请求（静默：无外部依赖）：
   - `GET /index.html` → 200
   - `GET /sig1.js` → 200
3. 页面交互：填 `inp=observe-test` 并点击 `#go` → 输出 `08b4f1b6cb55edfe8f2f81c1`（sig1 算法在浏览器真实运行产生）。
4. 触发一次真实 fetch（`GET /index2.html`）→ 200，len 358，7ms → 录到网络面板 reqid 12，带完整请求/响应头与响应体。

## 录到的请求链路

| reqid | method | url | status | 说明 |
|---|---|---|---|---|
| 10 | GET | `/index.html` | 200 | 页面文档 |
| 11 | GET | `/sig1.js` | 200 | 页面脚本（签名算法） |
| 12 | GET | `/index2.html` | 200 | 交互触发的请求（fetch，同源） |

请求 12 详情（automation 证据）：Referer `http://127.0.0.1:8765/index.html`，`sec-fetch-mode: cors`、`sec-fetch-site: same-origin`，响应 `text/html; charset=utf-8` 200，body 为 index2.html 全文。

## 这个观察手段的价值（对 js-reverse）

- 证明能「打开页面→点击交互→触发网络请求→记录请求链路与 initiator」，正好给 REA/js-reverse 补「运行时看到什么」的证据面。
- 可用于后续验证码/真实站点的签名定位：先观察网络请求，找到承载签名的请求，再定位其触发脚本。

## 结论

观察支撑：**通过**（一次成功的自动化观察录制，请求链路完整）。不写 L4/L5（本阶段是观察手段，不是重做）。