# 离线待推箱（R7 防线 8 + v3.1 9.4）

没网 / 没 GitHub 权限时：
- 提交写在本地 `lifecycle/defenses/OFFLINE-QUEUE.md`（追加：日期+阶段+本地 commit sha）。
- STATE 的 next_step 记 `待推送：<阶段>`。
- 「做完」= 本地做完 + 已排队；不假装已推送到远端。
- R8 时把排队的一并推送并核算远程 sha。
