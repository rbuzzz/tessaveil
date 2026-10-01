param([Parameter(Mandatory)][string]$ToolchainRoot, [switch]$Test)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '../environment.ps1') -ToolchainRoot $ToolchainRoot
$env:CARGO_TARGET_DIR = Join-Path $ToolchainRoot 'build/slint'
$lld = Join-Path $ToolchainRoot 'rustup/toolchains/1.90.0-x86_64-pc-windows-gnu/lib/rustlib/x86_64-pc-windows-gnu/bin/rust-lld.exe'
$arguments = @('rustc', '--locked', '--release', '--manifest-path', (Join-Path $PSScriptRoot 'Cargo.toml'), '--message-format=json')
if ($Test) { $arguments += '--tests' }
$messages = & cargo @arguments -- -C "linker=$lld" -C linker-flavor=ld.lld
if ($LASTEXITCODE -ne 0) { throw 'Slint build failed' }
$artifacts = @($messages | ForEach-Object { $_ | ConvertFrom-Json } | Where-Object { $_.reason -eq 'compiler-artifact' -and $_.target.name -eq 'tessaveil-slint-probe' -and $_.executable })
if ($artifacts.Count -ne 1) { throw 'Expected exactly one probe executable from Cargo' }
if ($Test) {
    & $artifacts[0].executable
    if ($LASTEXITCODE -ne 0) { throw 'Slint native tests failed' }
}
else { Write-Output $artifacts[0].executable }
