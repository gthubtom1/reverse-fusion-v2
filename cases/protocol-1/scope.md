# scope.md — cases/protocol-1

**本案模式是 算法抽取（模式 3），验收词是「算法抽取：通过 / 部分通过 / 不通过」，不适用 L4/L5。**

- 目标：对一个自定义二进制协议，抓包、还原字段与状态机、写出可复现的解码脚本、5 报文双侧对照。
- 类型：自定义 TCP 二进制协议（帧头 magic + 字段 + XOR 校验）
- 样本：自建协议服务 `target/server.py`（学习目标）；客户端 `target/client.py` 发报文。协议定义见下方。
- 要做：本地起服务 → tshark 抓 loopback → 导出 TCP payload → Node decode 脚本解析字段 + 校验 → 解码预测与真实抓包响应对照。
- 不做：不做模糊测试、不攻击第三方服务；不写 L4/L5。

## 协议定义（从 wire 还原）

```
byte0-1: magic 0xC0 0xD0
byte2: version (1)
byte3: type (1)
byte4-5: payload length (LE, 2 bytes)
byte6..6+len-1: payload
last: checksum = XOR of all payload bytes
```

服务器响应：校验通过 `OK:<ver>:<type>`；magic 错 `ERR:magic`；校验错 `ERR:checksum`；过短 `ERR:short`。

## 测试集（5 报文，事先写明）

| 用例 | 帧 | 类型 | 预期服务端响应 |
|---|---|---|---|
| TC1 正常 | `c0d001050500 68656c6c6f 62` (ver1,type5,"hello") | good | `OK:1:5` |
| TC2 正常 | ver2,type9,"world!" | good | `OK:2:9` |
| TC3 边界 | 空 payload (ver1,type0,len0) | good(+空) | `OK:1:0` |
| TC4 无效 | 校验字节改 0x00 | bad checksum | `ERR:checksum` |
| TC5 无效 | magic 改 0x00 0x00 | bad magic | `ERR:magic` |