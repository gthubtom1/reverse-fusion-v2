# .ps1 / .sh 孪生表（R7 防线 11）

reverse-skill 的脚本有 .ps1 与 .sh 两套，行为须一致。不强制统一成一套——Windows 用 .ps1、Linux/macOS 用 .sh，两套工具清单要一样。

| 能力 | .ps1 | .sh | 本机验证 |
|---|---|---|---|
| master-route | skills/scripts/master-route.ps1 | skills/scripts/master-route.sh | 是（R1 四提示词回归） |
| refresh-tool-index | skills/scripts/refresh-tool-index.ps1 | skills/scripts/refresh-tool-index.sh | 是（R1 C10 生成 tool-index.md） |
| 其余 bootstrap | bootstrap-reverse.ps1 / .sh | 同 | 未逐对 diff（记开放项） |
