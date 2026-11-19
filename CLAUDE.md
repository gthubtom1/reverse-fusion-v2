# reverse-fusion-v2（指针文件）
本项目位置为 `<SHARED_FOLDER>`。当前接手先读 `DEPLOYMENT-INVENTORY.md`、`lifecycle/STATE.yaml` 和 `cases/final/THIRD-PARTY-REPORT.md`。从状态文件的 `next_step` 继续。历史冻结方案 `FUSION-FINAL-v3.2.md` 保留作背景资料。

总控是 `<SHARED_FOLDER>/core/skills/SKILL.md`（reverse-skill-router）。分析引擎是 REA，只通过 MCP 调，不加载它的技能文件当总控。Seep 不在这里装（Track B，单独走）。
路径不要写死：共享文件夹位置只记在配置文件里（`%USERPROFILE%\.fusion\fusion-home.yaml` 的 `shared_folder` 这一行）。搬家只改那一行，再跑一次同步脚本。