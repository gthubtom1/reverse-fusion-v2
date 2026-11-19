# JS Signature 复现（Node 独立实现）

对 sig1（简单）和 sig2（中等）的 Node 复现。**这些复现不加载页面文件、不 eval 原脚本、不读浏览器**；算法是静态读页面分析后重写的。原版基准在浏览器里跑过（`E-001`）。

## sig1

```js
// 复现代码：cases/js-1/reimpl/sig1repro.mjs
// 算法：逐字节 b = ((b + i*7) ^ K[i%4]) & 0xff，再左旋 1 位，输出 hex；长度不足 4 用 K 补位
//（K = "k3y!" 的字节 [0x6b,0x33,0x79,0x21]）
```

## sig2

```js
// 复现代码：cases/js-1/reimpl/sig2repro.mjs
// 算法：nonce 派生 256 字节置换表 LUT -> 输入字节按 LUT 散列 -> FNV-1a 折叠成 32 位 -> 异或长度与 nonce 影响
```