<#
.SYNOPSIS
    BYOA Asset Importer for Blue Glass Engine (Tsukihime 2000 Classic HD).
.EXAMPLE
    pwsh -File import_assets.ps1 -Source "C:\Games\Tsukihime"
    pwsh -File import_assets.ps1 -Source "D:\Tsukibako" -Quality hd
#>
param(
    [Parameter(Mandatory = $false)]
    [string]$Source = "",

    [Parameter(Mandatory = $false)]
    [ValidateSet("fast", "hd")]
    [string]$Quality = "fast",

    [Parameter(Mandatory = $false)]
    [string]$HdPack = "",

    [Parameter(Mandatory = $false)]
    [string]$Target = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrWhiteSpace($Source)) {
    Write-Host "请输入本地原版《月姬 (2000)》目录 / Enter your local Tsukihime (2000) directory (contains arc.nsa & 0.txt/nscript.dat):" -ForegroundColor Cyan
    $Source = (Read-Host "Source Path").Trim().Trim('"')
}

if (-not (Test-Path -LiteralPath $Source)) {
    Write-Error "Directory not found / 找不到目录: $Source"
    exit 1
}

$pyArgs = @(
    (Join-Path $Root "scripts\byoa_import.py"),
    "--source", $Source,
    "--quality", $Quality
)
if (-not [string]::IsNullOrWhiteSpace($HdPack)) {
    $pyArgs += @("--hd-pack", $HdPack)
}
if (-not [string]::IsNullOrWhiteSpace($Target)) {
    $pyArgs += @("--target", $Target)
}

& python @pyArgs
exit $LASTEXITCODE
