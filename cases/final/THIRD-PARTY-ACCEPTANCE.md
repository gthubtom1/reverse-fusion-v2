# Pi 独立验收单

测试员在全新 Pi 会话和单独检出中记录 `git rev-parse HEAD`。以目标提交的实际文件运行以下五组核对。记录命令、退出码、结果与缺项。样本仅使用仓库里的静态元数据和合成布尔输入。

| 用例 | 操作 | 预期 |
|---|---|---|
| 1. 路由布局 | 从仓库外目录运行 `python -I <仓库>/lifecycle/defenses/unique_router.py` | 退出 0，45 个技能指针来自唯一配置。只读，不加载技能。 |
| 2. 两份真实交接 | 分别以 `core.autocrlf=false`、`true` 建立干净检出。对两个样本使用 `python -I core/skills/reconstruction/scripts/check_handoff.py . cases/sample-N/notes/handoff-manifest.json` | 四次退出 0，分别报告 11/15 个文件。`semantic_verification` 与 `target_execution` 均为 `not_performed`。 |
| 3. 篡改拒绝 | 在可丢弃检出中追加一行到 `cases/sample-1/evidence/E-005.md`，重新核对样本 1 | 退出 1，首条错误为 `sha256.mismatch`。 |
| 4. 共享比较器 | 用四组布尔回调测正常/改后全拒绝、有一项仍通过、空输入、全拒绝基线，再测非布尔回调 | 依次为真、假、假、假与 `TypeError`。 |
| 5. STATE 检查点 | 目标提交跑 `python -I lifecycle/check_state.py`。在可丢弃检出额外造一个空提交后重跑 | 目标提交退出 0 并打印其哈希。无状态更新的子提交退出 1。 |

领域设备实测、客户端配置和第二台机器装机单独记账。五组检查无法替代真实 Codex 往返、独立装机或全领域行为回归，不签发 `PI-PASS.md`。开放事项见 [结论](THIRD-PARTY-REPORT.md)。

## 第 1 轮 Pi 输出

被测版本 `18f260073f709c76fe700084ea18c29152bdbe54`。使用全新 `pi -p` 会话，关闭已有会话、扩展、技能和项目上下文，执行外置检查脚本。Pi 返回以下结果。其工具没有单独返回数值退出码。作者运行同一脚本的退出码为 0。

```text
1: OK one route table under core/, 45 skill pointers checked
2: lf sample-1: PASS 11
2: lf sample-2: PASS 15
2: crlf sample-1: PASS 11
2: crlf sample-2: PASS 15
3: tamper rejected
4: five comparator outcomes matched
5: OK STATE checkpoint 18f260073f709c76fe700084ea18c29152bdbe54
5: stale state rejected
```

负用例拒绝了一个一次性的子提交，这条预期失败不影响正向检查。两次测试均复用真实清单和原检查器。未执行任何原始样本。
