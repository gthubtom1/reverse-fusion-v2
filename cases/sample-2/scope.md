# 案子范围：样本 2（Not to simple KeyGen V2）

- 案子编号：sample-2
- 目标文件：`howo-not-to-simple-keygen`，819,856 字节
- SHA-256：`8b685085320c61337679f34eedc5aa338b5cc38c782ab5034581f33ae6c08804`
- 来源：crackmes.one，公开练习样本（`cases/samples/MANIFEST.md` 第 8 行）
- 类型：ELF 64-bit x86-64，静态链接，stripped；控制台程序，依次读姓名、邮箱、序列号
- 要复刻的功能：判断序列号是否有效；把验证算法在本地复现
- 本轮验收口径（用户 2026-11-20 指令）：按前两个项目测；无效输入拒绝、验证算法复现；第三个项目相关部分记为「以后再说」
- 不做：不改原程序、不做补丁、不绕过真实商业授权
- 成功标准：原版在 Linux 环境真跑；5 个用例结论一致；验证算法可用独立脚本复现
- 授权状态：`auth.status = granted`
- 样本位置：仓库外 `D:/tmp/fusion-samples/s2/howo-not-to-simple-keygen`，不随仓库分发
