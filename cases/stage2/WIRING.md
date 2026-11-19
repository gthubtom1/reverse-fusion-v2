# 第 2 阶段：接线报告

日期：2026-11-20（北京时间）。范围：REA MCP + 总控 + 复刻交接单模板。

**结论：接线测试通过。** 总控侧发出 `open_binary`、`binary_overview` 任务，REA 返回两条带证据 ID 的记录，证据包已落到 `cases/sample-1/evidence/`。复刻交接单模板已建立。限制与未核实项在末尾单列。

## 1. REA MCP

- 注册：`claude mcp add -s local rea -e GHIDRA_INSTALL_DIR=... -e JAVA_HOME=... -- <node.exe> engine/rea/scripts/rea.mjs mcp`
- `claude mcp list` 输出：`rea: ... - ✔ Connected`
- 项目级配置在 `.mcp.json`，同一端点；项目级条目在 Claude Code 中仍需用户批准一次。
- 工具目录：第 1 阶段已保存 260 项，见 [../stage1/tools-list-rea.json](../stage1/tools-list-rea.json)。

### 1.1 第一次接线失败与修复

第一次运行（04:09）`open_binary` 成功，`binary_overview` 返回：

```
provider_unavailable: The selected analysis provider is unavailable.
candidate_ids: ["ghidra","hopper","ida","kuna"]
ghidra rejection: unsupported_version (12.1.3; accepted 12.x >= 12.2)
java probe: REA Windows native controls are unavailable: Missing packaged Windows native file native/windows/build/manifest.json
```

两项修复，都按 REA 自己文档的说明做：

| 问题 | 处理 | 依据 |
|---|---|---|
| `native/windows/build/` 缺失 | 从 `npm pack rea-agents@6.9.0` 的 tarball 取出 `manifest.json`、`rea-windows-x64.node` 放入该目录 | `engine/rea/native/windows/README.md` 的 “Restore the artifact in a source checkout” 一节 |
| Ghidra 12.1.3 低于 12.2 | 下载官方 `Ghidra_12.2_build` 发布包，解压到 `D:/Tools/Ghidra-12.2/ghidra_12.2_PUBLIC` | REA `doctor` 的 remediation |
| Ghidra 12.2 要求 JDK 25 | 安装 Temurin JDK 25 到 `D:/Tools/jdk25` | `doctor` 的 `ghidra-java` 检查 |

修复后 `doctor` 里 `ghidra`、`ghidra-version`、`ghidra-java` 均为 healthy（原始输出 [rea-doctor-after.txt](rea-doctor-after.txt)）。`doctor` 总体仍是 `healthy: false`，因为 `hopper`、`ida-registration`、`jadx`、`kuna-installation` 等可选引擎未装；这些不影响 Ghidra 路径。

## 2. 接线测试

脚本：[wiring_test.py](wiring_test.py)。流程：initialize → `open_binary` → `binary_overview` → `get_evidence_bundle`（summary / complete）→ 落盘。

样本：`CrackMe.exe`，SHA-256 `945e81e113e09002db42b26f69cd43de564c32a03971fdf335e2f81caca6c67a`（与登记一致）。

| 调用 | 结果 | 耗时 |
|---|---|---|
| `open_binary` | 成功，`format=pe`、`architecture=x86_64`，返回的 sha256 与登记一致 | 1.7s |
| `binary_overview` | 成功，返回证据 ID `ev_646685c7bd9bc61a2bf30b163bb006bf2693e8e5121ada0f65201d1eea089a90` | 20.7s |
| `get_evidence_bundle` (summary) | 成功，`total_retained_records=2`，`direct_links=1` | 0.009s |
| `get_evidence_bundle` (complete) | 成功，`evidence_format=2`，providers 含 `ghidra 12.2` 与 `rea-workflow 1` | 0.004s |

两条证据 ID：

- `ev_23cd8d78eea2c858ba10f3ce69bfaf4bbe5c664f26f1faa5e0819471aa9ae13f` — `read_binary_inventory_summary`
- `ev_646685c7bd9bc61a2bf30b163bb006bf2693e8e5121ada0f65201d1eea089a90` — `binary_overview`

原始请求/响应：[../sample-1/evidence/wiring-transcript.json](../sample-1/evidence/wiring-transcript.json)；完整证据包：[../sample-1/evidence/E-REA-COMPLETE.json](../sample-1/evidence/E-REA-COMPLETE.json)。

这满足 v2.1 §7 第 2 阶段第 3 条：总控发出任务，REA 返回带证据 ID 的结果，结果存进 `cases/` 的 evidence。

## 3. 复刻交接单模板

已建立 [../templates/reconstruction-handoff.md](../templates/reconstruction-handoff.md)，字段与 v2.1 §5.3 一致：`target`、`key_functions`、`key_algorithms`、`behavior_list`、`test_cases`（≥5）、`unknowns`、`source`，并写明人读 Markdown 与机器 JSON 清单分开、未测输出写「未知、未验证」。

## 4. 未做与未核实

- 没有运行 `check_handoff.py` 校验真实交接单；模板里没有填真实值，等样本 1 有交接单后再跑。
- `doctor` 的 `hopper`、`ida-registration`、`jadx`、`kuna` 未装；本次只用 Ghidra 路径。
- `.mcp.json` 与 local scope 并存，`claude mcp list` 会提示端点不一致；当前两者指向同一程序，仅路径写法不同。
- REA 的 `open_binary` 用的是仓库外样本路径；证据里带本地绝对路径，公开前已确认不含用户名。
