# 案子范围：样本 1（XOR Challenge By 0xbadc0de）

- 案子编号：sample-1
- 目标文件：`CrackMe.exe`，111,104 字节
- SHA-256：`945e81e113e09002db42b26f69cd43de564c32a03971fdf335e2f81caca6c67a`
- 来源：crackmes.one，公开练习样本（见 `cases/samples/MANIFEST.md` 第 7 行）
- 类型：Windows x86-64 原生 PE，控制台输入校验
- 要复刻的功能：读取用户输入，按程序自己的规则校验，输出成功或失败
- 不做：不改原程序、不做补丁、不绕过任何真实商业授权；只用于公开练习样本的行为复现
- 成功标准：独立实现能运行；至少 5 个用例原版/新版输出一致；故意做坏的变体被检查器发现；未知项写进 `unknowns.md`
- 授权状态：`auth.status = granted`（用户 2026-11-20 指令明确要求跑样本 1 和样本 2）
- 样本文件位置：仓库外临时目录 `D:/tmp/fusion-samples/s1/CrackMe.exe`，不随仓库分发
