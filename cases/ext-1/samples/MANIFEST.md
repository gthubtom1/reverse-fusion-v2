# Stage 7 扩展样本登记

日期：2026-11-20。

| 编号 | 样本 | 难度 | 来源 | 代表什么 |
|---|---|---|---|---|
| ext-1-simple | 自建 MV3 浏览器扩展（token 签名） | 简单 | 本仓库 `cases/ext-1/target/` | MV3 extension `background/service_worker` 里的一段签名算法；代表「解包扩展→读 manifest→定位服务 worker 逻辑→复现」 |

## SHA-256

```bash
sha256sum cases/ext-1/target/manifest.json cases/ext-1/target/background.js
```

（记录在 evidence/E-001。）

## 说明

- 自建学习样本；真实第三方扩展（商店 crx）的自动化下载/加载链路本机未打通，先在自建样本走通 Stage 7 全流程。
- 原版基准 = 浏览器上下文执行原 `background.js` 的 `tokenFor`，5 用例逐字记录。