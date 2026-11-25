$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$RenpyExe = Join-Path $Root "tools\renpy_sdk\renpy-8.5.3-sdk\renpy.exe"
$ProjDir = Join-Path $Root "Tsukihime_HD"

if (-not (Test-Path -LiteralPath $RenpyExe)) {
    Write-Error "Ren'Py 8.5.3 SDK not found at: $RenpyExe"
    exit 1
}

& $RenpyExe $ProjDir
