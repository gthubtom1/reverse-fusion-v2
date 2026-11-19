# reverse-fusion-v2（指针文件）
本项目位置：`<SHARED_FOLDER>`（共享文件夹，三个上游、全部技能、全部案子都在里面）。
第一步，先读：`<SHARED_FOLDER>/FUSION-FINAL-v3.2.md` 的“从磁盘恢复清单”那一节，再读 `<SHARED_FOLDER>/lifecycle/STATE.yaml`，看 `current_stage` 和 `next_step`，从那里继续做。
当前接手先读 `DEPLOYMENT-INVENTORY.md`、`lifecycle/STATE.yaml` 和 `cases/final/THIRD-PARTY-REPORT.md`。历史冻结方案保留作背景资料。

总控是 `<SHARED_FOLDER>/core/skills/SKILL.md`（reverse-skill-router）。分析引擎是 REA，只通过 MCP 调，不加载它的技能文件当总控。Seep 不在这里装（Track B，单独走）。
路径不要写死：共享文件夹位置只记在配置文件里（`%USERPROFILE%\.fusion\fusion-home.yaml` 的 `shared_folder` 这一行）。搬家只改那一行，再跑一次同步脚本。