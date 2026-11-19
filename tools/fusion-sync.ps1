# fusion-sync.ps1 — read 唯一配置文件, generate 3 thin pointers (v3.2 §11).
# Usage: powershell -File tools/fusion-sync.ps1
# Twin of tools/fusion-sync.sh. Only generates pointers; never edits repo logic.

$ErrorActionPreference = "Stop"
$homeConf = Join-Path $HOME ".fusion\fusion-home.yaml"
if (-not (Test-Path $homeConf)) { Write-Error "FAIL config missing: $homeConf"; exit 1 }

function Get-ConfVal([string]$key) {
  $line = (Get-Content $homeConf | Where-Object { $_ -match "^$key:" } | Select-Object -First 1)
  if ($null -eq $line) { return "" }
  return ($line -replace "^$key:\s*", "").Trim()
}
$shared = Get-ConfVal "shared_folder"
$node   = Get-ConfVal "node_exe"
$ghidra = Get-ConfVal "ghidra_install_dir"
$jdk    = Get-ConfVal "java_home"
if (-not $shared -or -not $node) { Write-Error "FAIL config missing shared_folder/node_exe"; exit 1 }

$sharedJson = $shared -replace '\\', '/'
$sharedPs   = $shared

# 1) .mcp.json from template (JSON-safe via ConvertTo-Json)
$tplPath = Join-Path $shared ".mcp.json.template"
if (-not (Test-Path $tplPath)) { Write-Error "FAIL missing .mcp.json.template"; exit 1 }
$raw = (Get-Content $tplPath -Raw) `
    -replace '<NODE_EXE>', $node `
    -replace '<SHARED_FOLDER>', $sharedJson `
    -replace '<GHIDRA_DIR>', $ghidra `
    -replace '<JAVA_HOME>', $jdk
$json = $raw | ConvertFrom-Json
$json | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $shared ".mcp.json") -Encoding UTF8
Write-Output "OK  .mcp.json generated"

# 2) root CLAUDE.md pointer
@"
# reverse-fusion-v2（指针文件）
本项目位置：``$sharedPs``（共享文件夹，三个上游、全部技能、全部案子都在里面）。
第一步，先读：``$sharedPs\FUSION-FINAL-v3.2.md`` 的“从磁盘恢复清单”那一节，再读 ``$sharedPs\lifecycle\STATE.yaml``，看 ``current_stage`` 和 ``next_step``，从那里继续做。
总控是 ``$sharedPs\core\skills\SKILL.md``（reverse-skill-router）。分析引擎是 REA，只通过 MCP 调，不加载它的技能文件当总控。Seep 不在这里装（Track B，单独走）。
路径不要写死：共享文件夹位置只记在配置文件里（%USERPROFILE%\.fusion\fusion-home.yaml 的 shared_folder 这一行）。搬家只改那一行，再跑一次同步脚本。
"@ | Set-Content (Join-Path $shared "CLAUDE.md") -Encoding UTF8
Write-Output "OK  root CLAUDE.md"

# 3) AGENTS.md top pointer (keep existing 5 sync rules)
$agents = Join-Path $shared "AGENTS.md"
if (Test-Path $agents) {
  $head = Get-Content $agents -TotalCount 3 -ErrorAction SilentlyContinue
  if (-not ($head) -or -not ($head -match "本项目位置")) {
    $prefix = @("# reverse-fusion-v2（指针文件）",
                "本项目位置：$sharedPs。第一步读 `$sharedPs\FUSION-FINAL-v3.2.md` 与 `$sharedPs\lifecycle\STATE.yaml`；总控 `$sharedPs\core\skills\SKILL.md`；配置文件 %USERPROFILE%/.fusion/fusion-home.yaml。",
                "下面 5 条同步约定全文保留：", "")
    $content = Get-Content $agents -Raw
    ($prefix -join "`n") + "`n" + $content | Set-Content $agents -Encoding UTF8
  }
  Write-Output "OK  AGENTS.md pointer added"
} else { Write-Output "WARN AGENTS.md missing (open item)" }

# 4) global skill router pointer (3 hosts)
foreach ($base in @((Join-Path $HOME ".claude"), (Join-Path $HOME ".codex"), (Join-Path $HOME ".pi"))) {
  $dir = Join-Path (Join-Path $base "skills") "reverse-skill-router"
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
@"
---
name: reverse-skill-router
description: Routes reverse engineering tasks to the right skill. Use when a task is about analyzing, rebuilding, bypassing or extracting an algorithm from a program and the correct entrypoint is unclear.
---
# reverse-skill-router（指针文件，不是总控本身）
这个文件只有指路，不写任何方法。真正的方法全在共享文件夹里，不要在这里加内容。
共享文件夹位置：``$sharedPs``
第一步，先读这一个文件：``$sharedPs\core\skills\SKILL.md``（唯一总控）。
第二步，按总控说的做。路由用 ``$sharedPs\core\skills\scripts\master-route.ps1``（Windows）或 ``master-route.sh``，路由表只认 ``$sharedPs\core\skills\config\routing.json``。工具路径只认 ``$sharedPs\core\skills\tool-index.md``。
重建（R46）入口在 ``$sharedPs\core\skills\reconstruction\SKILL.md``，由总控打开，不要直接跳过去。
共享文件夹搬家后，这个文件不用手改：改配置文件里的一行，再跑一次同步脚本，它会自动重写。
"@ | Set-Content (Join-Path $dir "SKILL.md") -Encoding UTF8
  Write-Output "OK  $dir\SKILL.md"
}
Write-Output "Sync done."