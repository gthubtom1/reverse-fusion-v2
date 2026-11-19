# 第 0 步样本登记

2026-11-20（北京时间）。按[新版交接第 29–34、49–50 行](https://muse.ai/files/1426037403931614/1650581633186387/hcw2h3tnl63cpgcoej59805i/HANDOFF-long-run-v2.md)登记三份样本。**登记通过，原第 0 步验证报告保留为历史结论。**

| 编号 | 站点名称与难度 | 站点依据 | 公开下载 | 登记的程序文件 |
|---|---|---|---|---|
| 1 | XOR Challenge By 0xbadc0de，1.9 | 原作者说明是单字节 XOR 校验、Windows x86-64。页面无反调试或加壳标签。两者是否完全不存在尚未独立检验。 | [详情](https://crackmes.one/crackme/6a653dd6539826f489a10a27) · [ZIP](https://crackmes.one/download/crackme/6a653dd6539826f489a10a27) | `CrackMe.exe`，111,104 字节 |
| 2 | Not to simple KeyGen V2，3.0 | 原作者说明序列号校验使用自定义哈希。测试范围是无效输入被拒绝。文件头为 ELF。 | [详情](https://crackmes.one/crackme/69a1f44218b5d7ee4709351d) · [ZIP](https://crackmes.one/download/crackme/69a1f44218b5d7ee4709351d) | `howo-not-to-simple-keygen`，819,856 字节 |
| 3 | screwme_2 by dynasty，4.0 | 详情页标注反调试、字符串或数据加密、UPX。标签尚未独立验证。 | [详情](https://crackmes.one/crackme/5ab77f6033c5d40ad448c848) · [ZIP](https://crackmes.one/download/crackme/5ab77f6033c5d40ad448c848) | `ScrewMe2_Dynasty.zip` 内 `ScrewMe #2.exe`，266,752 字节 |

## SHA-256

| 编号 | 下载 ZIP | 程序文件 |
|---|---|---|
| 1 | `982e87e25bfa51d427f8660f46f678716afebcb3fb081c06c8c99b054b23125f` | `945e81e113e09002db42b26f69cd43de564c32a03971fdf335e2f81caca6c67a` |
| 2 | `4ebe026cc7f6f735956969271b59dd758e2facf872424680925884ecd1a3b1c1` | `8b685085320c61337679f34eedc5aa338b5cc38c782ab5034581f33ae6c08804` |
| 3 | `4dec91c189f923ba99f40eb130fbebabf87dca085447e4d8ee6813eff037cc77` | `7a194452ddc21cfdc0a5c6d941546f11c5a4e7069ce93ea80b86c883c139b60c` |

用 `curl.exe` 下载 ZIP 到项目外临时目录，以 Python `zipfile` 在内存读取归档成员，用 `hashlib.sha256` 分别计算 ZIP 与样本文件指纹。样本 3 的归档内还有 `ReadMe.exe`，它与主样本是不同文件。

三个样本均未执行，当前各为 0 个用例。样本 1、2 是第 3 阶段必测项。样本 3 为选测项。此提交只公开名称、来源、指纹和登记依据。
