# Pi 测试清单（R9 T1，v3.2 §12.4）

你是独立测试员 Pi，全新对话，只读仓库+共享文件夹快照。详见 FUSION-FINAL-v3.2.md 第 12 章。

0. 环境核对：核对 SNAPSHOT-COMMIT.txt 与 `git rev-parse HEAD`；跑 `rea doctor` / 报工具版本；检查 `core/skills/tool-index.md` 在快照里存在（C10 未核实点）。
1. 从零部署：只照 README 从头部署（不看我聊天记录）；每步命令+报错记录。
2. 路由回归：`master-route.sh --hint "apk" --dry-run` 与 `--hint "复刻这个APK" --dry-run` 退出 0；4 提示词进 R46。
3. 逐领域跑样本：对照 cases/*/ACCEPTANCE.md 每个结论重跑（原版 vs 复现 5 用例+边界+比较器）；证据链（E-↔ev_、check_handoff PASS、REA 验证链）；复用检查；难样本看流程。
   - 样本 1/2 原版在 `samples/`（sample1-CrackMe.exe / sample2-keygen.elf）。
4. 写报告 pi-work/PI-TEST-REPORT-T1.md（§12.5 的 6 节），不改代码不提交。

报告模板（6 节）：0 环境核对 / 1 路由回归 / 2 逐领域结果 / 3 证据链专项 / 4 缺口清单 / 5 总结论。
