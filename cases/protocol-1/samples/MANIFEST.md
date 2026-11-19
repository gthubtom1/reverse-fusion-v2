# Stage 8 协议样本登记

日期：2026-11-20。

| 编号 | 样本 | 难度 | 来源 | 代表什么 |
|---|---|---|---|---|
| protocol-1-simple | 自定义二进制协议（magic+字段+XOR 校验） | 简单 | 本仓库 `cases/protocol-1/target/server.py` + `client.py` | 自定义协议的字段还原与状态机解码；代表「抓包→还原→写 decode→对照」 |

## SHA-256

```bash
sha256sum cases/protocol-1/target/server.py cases/protocol-1/target/client.py
```

记录在 `evidence/E-000-hashes.txt`。

## 说明

- 自建学习协议（非第三方）。真实协议需在公开学习流量/pcap 上重做；本阶段验证流程，抓包（tshark loopback）、还原、decode、对照全为真实执行。