# unknowns.md — cases/automation-1

- 未在真实第三方站点上观察（只对自己的本地测试页）。真实站点可能依赖登录态、CORS、动态脚本注入，未测。
- 用 chrome-devtools MCP 完成；Playwright CLI 那条路（`npx playwright`）在本机命令缺失报错，未用。
- 未做「观察→自动定位签名调用→取参」的闭环（自动化观察本身证明能用，闭环留给后续真实目标时接续）。
- 未测多标签/跨域/Service Worker 等复杂页面场景。