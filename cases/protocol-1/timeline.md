# timeline.md — cases/protocol-1

- 2026-11-20 06:1x 核实抓包工具：tshark/wireshark 4.6.8 在 `/d/Tools/Wireshark`，scapy 2.8.0 可用，Npcap loopback 接口存在。
- 06:1x 自建协议：`server.py`（magic+ver+type+len+payload+XOR checksum）、`client.py`（5 报文）。
- 06:1x `tshark -i NPF_Loopback` 首次失败（设备名写法），用完整路径 `\Device\NPF_Loopback` 成功；`-w` 写 pcapng。
- 06:2x 跑客户端 5 报文，服务端响应存 `/tmp/proto-results.txt`；倒出 pcap 中 TCP payload（`evidence/E-002-payload-export.txt`）。
- 06:2x Node write `decode.mjs`；对照 5 报文 → `ALL_MATCH true`。
- 06:3x 比较器自检（改字段/校验字节）→ ok=true。
- 结论：算法抽取**通过**。