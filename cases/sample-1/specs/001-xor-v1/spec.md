# Spec 001 xor-v1

- FR-001: 输入长度必须为 6
- FR-002: 每个字符异或 KEY[0x55] 后等于常量表 [0x38,0x27,0x64,0x66,0x66,0x62]
- FR-003: 全部匹配时输出 ACCESS GRANTED，否则 ACCESS DENIED
