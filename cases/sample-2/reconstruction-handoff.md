# 复刻交接单 — howo-not-to-simple-keygen (Not to simple KeyGen V2)

target: howo-not-to-simple-keygen, sha256: 8b685085320c61337679f34eedc5aa338b5cc38c782ab5034581f33ae6c08804
source: 证据 E-002（REA 平台限制）、E-003（main 反编译）、E-004（运行时表 dump）、E-005（五用例）、E-006（表一致性验证）
case: cases/sample-2
auth.status: granted

## 关键函数
| 函数名 | 地址 | 输入 | 输出 | 干什么用 |
|---|---|---|---|---|
| main | 0x401640（Ghidra 显示为 FUN_0040158a） | 无 | int 退出码 | 打印提示、读姓名/邮箱/序列号、调用哈希与校验。证据 E-003。 |
| 哈希 FUN_00401d80 | 0x401d80 | 字节指针 + 长度 | 256 字节表 | 自定义哈希，返回 256 字节状态表。证据 E-003、E-004。 |
| 校验循环 | 0x4019ab–0x401aa4 | 序列号、表指针 | 成功/失败 | 长度必须 16；按步长 3 检查三元组。证据 E-003 的汇编与反编译。 |

## 关键算法
- 读入：`fgets` 读姓名、邮箱、序列号，用 `strcspn(...,"\r\n")` 去掉行尾。证据 E-003。
- 表：`table = H(H(name) || H(email))`，H 为 0x401d80，返回 256 字节。证据 E-003、E-006（模拟表与运行时 dump 逐字节一致）。
- 序列号必须 16 字节；`n = 17`（长度 + 1）。对 i = 0,3,6,9,12,15：
  - 若 `serial[(i+1)%17] + serial[i] == serial[(i+2)%17] * 8`，跳过；
  - 否则若 `serial[(i+3)%17] == (signed char)table[i] * 4`（32 位有符号相等），判定成功。
- 由 `table[i]` 的符号扩展乘 4 得到序列号字节，只有结果落在 `-128..127` 的 i 可用。证据 E-004、E-005、E-006。

## 行为清单
1. 打印欢迎语与 `Welcome back to the NTSK Hotel!`。证据 E-003。
2. 依次提示 `Please insert your full name:`、`Please insert your best email:`、`Please insert your serial:`。证据 E-003、E-005。
3. 校验失败：打印 `POLICE, THIS GUY IS A ROBBER BUT HE DON'T HAVE A VALID SERIAL KEY LOL!`，退出码 1。证据 E-005（TC3–TC5）。
4. 校验成功：打印 `Very nice work man!!!` 与 `Get your flag: CTF{Giant-binary!=Secure-binary---Look-to-validation-and-boom}`，退出码 0。证据 E-005（TC1、TC2）。

## 测试用例
| 编号 | 输入（姓名 / 邮箱 / 序列号） | 原版输出 | 证据 |
|---|---|---|---|
| TC1 | alice / bob@example.com / `4142434445464748494a4b4cec4e4f50` | accepted，退出码 0，打印 flag | E-005 |
| TC2 | davis / davis@test.com / `4142434445460448494a4b4c4d4e4f50` | accepted，退出码 0，打印 flag | E-005 |
| TC3 | alice / bob@example.com / `AAAAAAAAAAAAAAAA` | denied，退出码 1 | E-005 |
| TC4 | alice / bob@example.com / `ABC` | denied，退出码 1 | E-005 |
| TC5 | alice / bob@example.com / 64 个 `A` | denied，退出码 1 | E-005 |

TC1、TC2 的序列号由 `reimpl/keygen.py` 生成，生成后交给原版真跑，不是抄原版输出。

## 未知清单
- H（0x401d80）没有用高级语言重写；当前用 Unicorn 模拟原版机器码生成表（`reimpl/emulate_hash.py`），与运行时 dump 逐字节一致（E-006）。这是机器码级复现，不是从反编译 C 重新实现的源码。
- 没有动态调试内存以外的运行状态；没有测 locale、TTY、超长行截断等其他环境差异。
- 校验只验证 6 个三元组位置；R46 的 L5 副作用面（提示文字、退出行为）没有由 keygen 复刻。
