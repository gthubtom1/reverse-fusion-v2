# 复刻交接单 — 自定义协议解码器（protocol-1）

target: 自定义 TCP 二进制协议 decode（自建学习目标）
source: evidence E-001（抓包 pcap）、E-002（tshark 导出 payload + 对照）
case: cases/protocol-1
模式: 算法抽取（模式 3），不适用 L4/L5

## 抽的是哪一段

- 协议帧：`magic(2) | ver(1) | type(1) | len(2,LE) | payload | checksum(1, XOR)`
- 服务器状态机：magic 错→`ERR:magic`；校验错→`ERR:checksum`；过短→`ERR:short`；通→`OK:<ver>:<type>`
- 复现：`reimpl/decode.mjs`（`decodeFrame` + `serverReplyFor`）

## 测试用例（5 报文双侧对照，真实抓包响应 vs decode 预测）

见 `evidence/E-002-differential.json` / 下方命令行输出（`ALL_MATCH true`）：

| 用例 | 帧 hex | 抓包真实响应 | decode 预测 | 一致 |
|---|---|---|---|---|
| TC1 | `c0d00105050068656c6c6f62` | `OK:1:5` | `OK:1:5` | ✅ |
| TC2 | `c0d002090600776f726c642143` | `OK:2:9` | `OK:2:9` | ✅ |
| TC3 | `c0d00100000000` | `OK:1:0` | `OK:1:0` | ✅ |
| TC4 | `c0d00105050068656c6c6f00` | `ERR:checksum` | `ERR:checksum` | ✅ |
| TC5 | `00000105060068656c6c6f00` | `ERR:magic` | `ERR:magic` | ✅ |

## 未知清单

见 `unknowns.md`。