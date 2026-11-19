# 复刻交接单 — JS 签名算法（sig1 / sig2）

target: JS 签名算法（自托管学习页）sig1 + sig2
source: 证据 E-000（样本哈希）、E-001（浏览器原版基准）、E-002（双侧对照）
case: cases/js-1
模式: 算法抽取（模式 3），不适用 L4/L5

## 关键算法（抽的是哪一段）

### sig1（简单）
- 输入：字符串；输出：hex（长度 = max(len, 4)*2 字符）
- 逐字节变换：`b = ((byte + i*7) ^ K[i%4]) & 0xff`，再左旋 1 位：`b = ((b<<1)|(b>>7))&0xff`
- 常数 K = `[0x6b,0x33,0x79,0x21]`（"k3y!"）
- 长度不足 4 时用 K 补位：`b = K[i%4] + 0x11`
- 定位：E-001 里 `sig1` 函数。复现：`reimpl/sig1repro.mjs`

### sig2（中等）
- 输入：message + nonce；输出：8 位 hex
- 第一步 nonce 派生 256 字节置换表 LUT（Fisher–Yates 变体）：`j=(j+lut[i]+((nonce*31+i*17)&0xff))&0xff`
- 第二步散列：`sc[i]=lut[(msg[i]+i)&0xff]`
- 第三步折叠：FNV-1a 变体（`h^=b; h=(h+(((h<<1)+(h<<4)+(h<<7)+(h<<8)+(h<<24))))>>>0`）
- 第四步混合：`h2=(h ^ (len*2654435761) ^ (nonce*40503))>>>0`
- 复现：`reimpl/sig2repro.mjs`

## 行为清单（算法语义）
1. sig1：读输入 → 每字节变换 → 左旋 → hex 拼接。
2. sig2：读 msg、nonce → 生成 LUT → 散列 → FNV 折叠 → 混合长度与 nonce → hex。

## 测试用例（见 `evidence/E-002-differential.json`，双侧对照全过）
- sig1 TC1–TC5 全过；sig2 TC1–TC5 全过；破坏 K/LUT 后输出必变；新输入探针确定性 + 非背答案。

## 未知清单
- 见 `unknowns.md`。

## 证据指针
- 本 Markdown 与 `evidence/` 指向同一份原始运行记录（E-001 浏览器基准、E-002 对照 JSON）。