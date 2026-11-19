# 第 1 阶段：本地签出核对

日期：2026-11-20（北京时间）。范围：只核对并签出前两个项目——REA 和 reverse-skill。第三个项目（Seep）按本轮指令记为「以后再说」，未签出、未核对。

结论：**两个本地 HEAD 都和锁定表一致，可以进入安装。** 下表每条都附了执行命令和实际输出。

## 1. 仓库与固定提交（来自 `FUSION-FINAL-v2.1.md` §2）

| 项目 | 仓库 | 锁定提交 | 签出位置 |
|---|---|---|---|
| REA | `https://github.com/morluto/rea` | `4491c84c82140a43fa12390b727840a433875ba8` | `engine/rea` |
| reverse-skill | `https://github.com/gthubtom1/reverse-skill` | `ce675096e6a2cd4789a76f9bd618feddc2b6f333` | `upstream/reverse-skill` |

## 2. 实际操作

```bash
cd "D:/Project/最终版聚合"
git submodule add https://github.com/morluto/rea engine/rea
git submodule add https://github.com/gthubtom1/reverse-skill upstream/reverse-skill

cd engine/rea && git checkout 4491c84c82140a43fa12390b727840a433875ba8
cd ../.. && cd upstream/reverse-skill && git checkout ce675096e6a2cd4789a76f9bd618feddc2b6f333
```

两次 `git submodule add` 都只输出 `Cloning into ...`，没有报错。

## 3. 核对结果

`git submodule status` 输出：

```
+4491c84c82140a43fa12390b727840a433875ba8 engine/rea (rea-agents-6.9.0-1344-g4491c84c8)
 ce675096e6a2cd4789a76f9bd618feddc2b6f333 upstream/reverse-skill (v1.9.0-5-gce67509)
```

| 检查项 | 结果 | 判定 |
|---|---|---|
| `engine/rea` 的 `git rev-parse HEAD` | `4491c84c82140a43fa12390b727840a433875ba8` | 与锁定表一致 |
| `upstream/reverse-skill` 的 `git rev-parse HEAD` | `ce675096e6a2cd4789a76f9bd618feddc2b6f333` | 与锁定表一致 |
| REA `git describe` | `rea-agents-6.9.0-1344-g4491c84c8` | 提交在 `6.9.0` 标签之后 1344 个提交，锁定的是提交号，不是标签 |
| reverse-skill `git describe` | `v1.9.0-5-gce67509` | 提交在 `v1.9.0` 标签之后 5 个提交；与 v2.1 §2 第 1 条“正式 tag 指向 `7cc3109…`、项目仍锁 `ce67509…`”一致 |
| REA 文件数 | 9,358（`find engine/rea -type f \| wc -l`） | 记录备查 |
| reverse-skill 文件数 | 676（`find upstream/reverse-skill -type f \| wc -l`） | 记录备查 |
| reverse-skill `skills/` 目录数 | 57（`ls upstream/reverse-skill/skills \| wc -l`） | 记录备查；瘦身时按 v2.1 §4.1 只留 15 个 |

提交元数据（`git log -1 --format='%H %ad %s' --date=iso`）：

- REA：`4491c84c82140a43fa12390b727840a433875ba8 2026-11-20 00:25:23 +0800 fix(node-sea): bound duplicate blob verification work (#11736)`
- reverse-skill：`ce675096e6a2cd4789a76f9bd618feddc2b6f333 2026-11-14 19:14:44 +0800 Define Codex execution profile in the original R46 workflow (#22)`

## 4. 环境差异与处理

REA 的 `package.json` 声明 `engines.node = "^22.23.4 || ^24.22.1 || >=26.12.1"`，仓库 `.npmrc` 写 `engine-strict=true`。本机原有 Node 为 `v24.20.0`，第一次 `npm ci` 被拒绝：

```
npm error code EBADENGINE
npm error notsup Required: {"node":"^22.23.4 || ^24.22.1 || >=26.12.1"}
npm error notsup Actual:   {"node":"v24.20.0","npm":"11.19.0"}
```

处理：从 `https://nodejs.org/dist/v24.22.1/node-v24.22.1-win-x64.zip` 下载官方 Node `v24.22.1`，解压到 `D:/Tools/node-24.22.1/node-v24.22.1-win-x64`，只在 REA 的安装与构建命令里把该目录放到 `PATH` 前面，不改系统全局 Node。`node -v` 在该环境返回 `v24.22.1`。

## 5. 未做与未核实

- Seep 未签出、未核对（以后再说）。
- 两个仓库都未修改源码；`core/` 的瘦身复制在第 1 阶段安装步骤中另记。
- 本地网络克隆成功，但未验证子模块在别的机器上能否以同样方式拉取。
