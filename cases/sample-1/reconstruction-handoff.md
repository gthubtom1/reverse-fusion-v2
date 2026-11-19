# 复刻交接单 — CrackMe.exe (XOR Challenge By 0xbadc0de)

target: CrackMe.exe, sha256: 945e81e113e09002db42b26f69cd43de564c32a03971fdf335e2f81caca6c67a
source: 证据 E-002（函数清单）、E-003（invoke_main）、E-004（main）、E-005（校验函数）、E-006（差分）、E-008（边界）
case: cases/sample-1
auth.status: granted

## 关键函数
| 函数名 | 地址 | 输入 | 输出 | 干什么用 |
|---|---|---|---|---|
| FUN_140017cd0（main） | 0x140017cd0 | 无 | int | 打印横幅、提示输入、调用校验、按结果打印 ACCESS GRANTED / DENIED。证据 E-004。 |
| FUN_1400173d0（校验） | 0x1400173d0 | 输入字符串指针 | bool（0/1） | `strlen==6` 时逐字节比较 `input[i] == const[i] ^ 0x55`。证据 E-005。 |
| thunk_FUN_140017820（strlen） | — | 字符串 | 长度 | 长度判断。证据 E-005。 |
| thunk_FUN_140015e90（operator[]） | — | 字符串、下标 | 字符指针 | 取第 i 个字符。证据 E-005。 |

## 关键算法
- 长度：`strlen(input) == 6`，否则返回 0。证据 E-005。
- 常量数组：`[0x38, 0x27, 0x64, 0x66, 0x66, 0x62]`，位于校验函数栈上的 `local_154`。证据 E-005。
- 校验：对 i=0..5，`input[i] == const[i] ^ 0x55`；全部相等返回 1，否则返回 0。证据 E-005。
- 反推密码：`0x38^0x55='m'`、`0x27^0x55='r'`、`0x64^0x55='1'`、`0x66^0x55='3'`、`0x66^0x55='3'`、`0x62^0x55='7'` → `mr1337`。证据 E-005、E-006。
- 输入读取：C++ `cin >> std::string`，按空白分词；行尾空格和 CR 不进入字符串。证据 E-008（B3、B6）。

## 行为清单
1. 启动 → 设置控制台标题 `CrackMe v1.2` → 打印横幅 `SIMPLE+ XOR CRACKME`。证据 E-004。
2. 提示 `[+] Enter password: ` → 读入一个空白分隔的字符串。证据 E-004、E-008。
3. 调用校验函数 → 长度或字节不匹配则打印 `[-] ACCESS DENIED!` 与 `[-] Wrong password!`。证据 E-004、E-006。
4. 匹配则打印 `[+] ACCESS GRANTED!`、`[+] Password is correct!`、`FLAG: CRACKME{X0R_CR4CK3D}`。证据 E-006（TC1）。
5. 最后打印 `[*] Press Enter to exit...` 并等待回车后退出，退出码 0。证据 E-006。

## 测试用例
| 编号 | 输入 | 原版输出 | 证据 |
|---|---|---|---|
| TC1 | `mr1337` | ACCESS GRANTED! / Password is correct! / FLAG: CRACKME{X0R_CR4CK3D} | E-006 |
| TC2 | `mr1338` | ACCESS DENIED! / Wrong password! | E-006 |
| TC3 | `MR1337` | ACCESS DENIED! / Wrong password! | E-006 |
| TC4 | `mr133` | ACCESS DENIED! / Wrong password! | E-006 |
| TC5 | `mr13377` | ACCESS DENIED! / Wrong password! | E-006 |

全部 5 条由 `differential_test.py` 真跑原版得到，stdout 原文保存在 `evidence/E-006-differential.json`，不是猜的。

## 未知清单
- 未做动态调试，未观察运行时内存；结论全部来自 Ghidra 静态反编译和原版黑盒运行。
- 未复刻控制台颜色、标题、等待回车等外围副作用；独立实现只复刻“接受/拒绝”判断。
- 只测了空白分词的空格、CR 和长输入；Tab、全角空格等未测。
- 原版依赖调试版 CRT（`ucrtbased.dll`、`msvcp140d.dll` 等）；本机是从 Windows SDK 与 VS Build Tools 的调试运行库目录取得，未记录这些运行库的哈希。

## 机械交接与证据来源

`E-005` 的完整 REA 证据号为 `ev_cdf672b5dd0d2716c7857ad5def2f11104109341458c8f504f9824a459389a0d`，来自 [E-005 原始答复](evidence/E-005-check.json)。更多对应关系见 [证据映射](EVIDENCE-MAP.md)。 使用 [机器清单](notes/handoff-manifest.json)核对文件与引用。真实 Codex 往返未取得回执。
