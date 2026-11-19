# E-001 原版浏览器基准（sig1、sig2）

来源：自己的测试页 `cases/js-1/target/index.html` / `index2.html`，经 chrome-devtools 在本地服务器 `http://127.0.0.1:8765` 实跑。

## sig1（简单）

| 输入 | 原版（浏览器）输出 |
|---|---|
| `alice` | `14801cb2d5` |
| `` | `f8881564` |
| `abc` | `14b41064` |
| `hello world` | `06be0641c1e0b1038331a7` |
| `k3y!_x` | `0012fd2e2051` |

获取命令：`chrome-devtools_evaluate_script`（page `http://127.0.0.1:8765/index.html`），循环 `inp.value = v; go.click(); out.textContent`。

## sig2（中等）

| message | nonce | 原版（浏览器）输出 |
|---|---|---|
| `hello` | 42 | `8698c417` |
| `` | 0 | `811c9dc5` |
| `x` | 7 | `783f0662` |
| `hello` | 43 | `55fdcd57` |
| `hello world` | 0 | `ac6e90b2` |

获取命令：同上（`index2.html`，`msg`/`nonce`/`go`）。