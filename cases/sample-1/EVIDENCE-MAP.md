# 样本 1 证据对应表（E- → ev_）

一个 E 号只指一个文件；多文件已拆分。

| E 号 | 指的文件 | 对应 REA ev_ 号 | 说明 |
|---|---|---|---|
| E-002 | `evidence/E-002-procedures.json` | `ev_e4bd46c88af56ab734e2c053dbac0f4f17875514d804a4b0de24a1c48969e0bb` | REA `list_procedures` 输出（证据自带 ev_） |
| E-003 | `evidence/E-003-invoke-main.json` | `ev_b1f691139a05a2777d9a1f9d8ec95c5eceade85655e2cf06989ba3eb956178a8` | REA `analyze_function`（invoke_main） |
| E-004 | `evidence/E-004-main.json` | `ev_261a5d8f79cd02621c553f22a940e04e31f15f7ee8cca1f9d2ab545bbf96d416` | REA `analyze_function`（main） |
| E-005 | `evidence/E-005-check.json` | `ev_cdf672b5dd0d2716c7857ad5def2f11104109341458c8f504f9824a459389a0d` | REA `analyze_function`（校验函数） |
| E-006 | `evidence/E-006-differential.json` | 无（本机脚本差分） | 5 用例双侧对照 |
| E-007 | `evidence/E-007-comparator-selfcheck.json` | 无（本机脚本） | 比较器自检 |
| E-008 | `evidence/E-008-boundary.json` | 无（本机脚本） | 边界用例 |
| E-REA-COMPLETE | `evidence/E-REA-COMPLETE.json` | `ev_646685c7bd9bc61a2bf30b163bb006bf2693e8e5121ada0f65201d1eea089a90` | REA 完整证据包 |

说明：无 REA 证据号的条目（E-006/007/008）是电脑智能体写的差分/自检脚本输出，不是 REA 工具调用，故没有 `ev_`，这是本机流程设计（模式 3 双侧对照由脚本承担）；每个证据文件的 `content_hash` 见其同名 `.md` 记录。