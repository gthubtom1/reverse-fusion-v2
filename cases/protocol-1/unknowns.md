# unknowns.md — cases/protocol-1

- 协议是**自建学习目标**（`target/server.py`），不是真实第三方商业协议；只验证「抓包→还原→decode→对照」流程。
- 只抓 127.0.0.1 loopback，未测跨网段、TLS 加密、分片重组、超大/畸形帧的鲁棒性。
- 用 tshark 静态导出 payload 做还原；没有用 scapy 做在线流量重组。
- 服务端只处理单帧（`recv(4096)` 一次），未测粘包/拆包的多帧场景——这是真实协议的常见面，记为以后再说。
- 未对 checksum 做多字节/其他校验算法变体；只验证了 XOR 一种。