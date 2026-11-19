# 验收报告：cases/protocol-1（Stage 8）

**R6 复用检查：工具单查询——抓包用 tshark/Wireshark（系统工具）；解码比对自建（decode.mjs 一次性）；比较器自检统一引共享，不再重写。**


**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过」。不适用 L4/L5（本模式不要求）。**

## 0. 结论（两行分写）
- 第一行（本模式结论）：**算法抽取：通过**。
- 第二行（R46 结论）：R46 L4：不适用（模式 3）；L5：不适用。

## 1. 做了什么

- 自建自定义二进制协议服务（`target/server.py`）+ 客户端（`target/client.py`），TCP 127.0.0.1:6553。
- 抓包：tshark 4.6.8 抓 `\Device\NPF_Loopback`，`tcp port 6553`，得到 `evidence/E-001-loopback.pcapng`。
- 还原：tshark `-Y "tcp.payload"` 导出客户端帧与服务端响应 hex（5 组）。
- 复现：`reimpl/decode.mjs` Node 解码器（解析字段 + XOR 校验 + 预测服务端响应），独立实现，不读/不 eval 服务端代码。
- 对照：decode 预测 vs 真实抓包响应。

## 2. 双侧对照（5 报文）

命令输出（`cases/protocol-1` 下 `node --input-type=module`）：

```
T1 ... pred OK:1:5 real OK:1:5 MATCH
T2 ... pred OK:2:9 real OK:2:9 MATCH
T3 ... pred OK:1:0 real OK:1:0 MATCH
T4 ... pred ERR:checksum real ERR:checksum MATCH
T5 ... pred ERR:magic real ERR:magic MATCH
ALL_MATCH true
```

覆盖 TC1/TC2 正常、TC3 边界（空 payload）、TC4/TC5 无效（校验/magic 错），符合模式 3 测试集要求。

## 3. 独立运行 + 不依赖原文件

- `reimpl/decode.mjs` 可独立跑（纯解析 hex），不依赖服务器、不读服务端源码。
- 比较器自检（`reimpl/comparator_check.mjs`，`ok=true`）：好帧→`OK:1:5`；改 payload 字节→`ERR:checksum`；改校验字节→`ERR:checksum`；改 type 且 checksum 未变仍有效→照常 OK。证明解码器依赖真实字节（防背答案）。

## 4. 未验证 / 未知

- 只抓了本机 loopback；未测 TLS/加密字段、跨网段抓包、`<all_urls>` 之类的复杂协议面。
- 协议是自建的（非真实第三方），目的在走通「抓包→还原→decode→对照」流程。
- 未用 scapy 做在线重组（用 tshark 静态导出），未验证边界帧（长度溢出、超大 payload）——TC3 空 payload 已覆盖最小边界。

## 结论

**算法抽取：通过**。5 报文从 pcap 还原、decode 预测与真实响应全一致，独立运行、比较器自检通过。未宣称 L4/L5。