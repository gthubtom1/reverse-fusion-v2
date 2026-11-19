# unknowns.md — cases/js-1

- 样本是自有测试页（v3 §6.3 允许自己的测试页），不是在真实第三方站点上做的签名逆向。公网站点的签名链路、动态脚本加载、反调试尚未实测。
- `js-reverse_*` MCP / `jshookmcp` 未装（`claude mcp list` 无该端）、未注册；本阶段用 Node 本地复现 + 浏览器观察（chrome-devtools），CDP 面未试。
- 本地测试页是可控的；未覆盖：真实页面的异步加载、SourceMap、加密混淆、Obfuscator 级别代码。真实站点签名复现需 jshookmcp，记为「以后再说」。
- 复现代码只验证了 5+2 个输入与浏览器原版的一致；未做海量随机输入的模糊双侧对照（后续可加）。
- Node 24.22.1 的 `-I`/ESM 环境下运行要通过 `node --input-type=module` 或直接 `node reimpl/*.mjs`；Windows cmd 下直接 `node reimpl/comparator_check.mjs` 可跑，路径带中文目录时需从项目根跑。