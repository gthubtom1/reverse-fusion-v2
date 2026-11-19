# timeline.md — cases/ext-1

- 2026-11-20 05:5x 读 `core/skills/browser-extension-reverse/SKILL.md`（Stage 5A 已恢复），确认流程：解压→manifest→background→复现。
- 06:0x 自建 MV3 扩展样本 `target/`（manifest + background.js tokenFor）。
- 06:0x 写 Node 复现 `extrepro.mjs`；把 background.js 复制到本地服务器目录，浏览器 chrome-devtools fetch+new Function 加载原版 `tokenFor`，5 URL 真跑基准。
- 06:1x Node 复现跑同 5 用例 → `ALL_MATCH true`。
- 06:1x 比较器自检（改 SECRET 末字节）→ 4 非空 URL token 全变，空串恒定 0000（语义）→ ok。
- 结论：算法抽取**通过**。