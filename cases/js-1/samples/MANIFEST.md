# Stage 5 JS 样本登记

日期：2026-11-20。来源：自己的测试页（v3 §6.3 允许「自己的测试页」；不碰真实商业软件）。

| 编号 | 样本 | 难度 | 文件 | SHA-256 | 为什么代表这个领域 |
|---|---|---|---|---|---|
| js-1-simple | 签名算法 sig1 | 简单 | `cases/js-1/target/sig1.js` | 见下文 | 单层签名链路：输入→逐字节变换→十六进制输出。定位 + Node 复现的典型轻量算法 |
| js-1-medium | 签名算法 sig2 | 中等 | `cases/js-1/target/sig2.js` | 见下文 | 多层：nonce 派生置换表（LUT）→散列折叠（FNV-1a 变体）→长度/nonce 混合。代表网页里常见的“多步变换”签名 |

## SHA-256

```bash
sha256sum cases/js-1/target/sig1.js cases/js-1/target/sig2.js
```

结果见 `cases/js-1/evidence/E-000-samples-hash.txt`。

## 理由

- sig1：教学页常见风格，一段独立闭包函数，便于验证“定位 → 复现 → 对照”全流程。
- sig2：带 nonce、置换表、多次折叠，需要逆向多步状态才能复现；对应 v3 §2.1「JS/网页算法主模式」里中等的表单签名。
- 两者都有确定输出（无随机），可以做严格的 5 用例双侧对照。