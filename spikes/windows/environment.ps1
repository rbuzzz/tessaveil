# Dot-source in a disposable PowerShell process. No registry/user PATH edits.
param([Parameter(Mandatory)][string]$ToolchainRoot)
$ErrorActionPreference = 'Stop'
if ($ToolchainRoot -match '[^\x00-\x7F]') { throw 'Use an ASCII toolchain root' }
$root = (Resolve-Path -LiteralPath $ToolchainRoot).Path
$rust = Join-Path $root 'rustup/toolchains/1.90.0-x86_64-pc-windows-gnu'
$llvm = Join-Path $root 'llvm-mingw-20250709-ucrt-x86_64/bin'
$support = Join-Path $root 'gnu-support'
New-Item -ItemType Directory -Force $support | Out-Null
Copy-Item -LiteralPath (Join-Path $llvm 'llvm-dlltool.exe') -Destination (Join-Path $support 'dlltool.exe')
$env:RUSTUP_HOME = Join-Path $root 'rustup'
$env:CARGO_HOME = Join-Path $root 'cargo'
$env:RUSTFLAGS = '-C link-self-contained=yes'
$env:DOTNET_CLI_HOME = Join-Path $root 'dotnet-home'
$env:NUGET_PACKAGES = Join-Path $root 'nuget'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$env:DOTNET_GENERATE_ASPNET_CERTIFICATE = 'false'
$env:DOTNET_SKIP_FIRST_TIME_EXPERIENCE = 'true'
$env:TEMP = Join-Path $root 'tmp'
$env:TMP = $env:TEMP
New-Item -ItemType Directory -Force $env:TEMP | Out-Null
$env:PATH = @($support, (Join-Path $rust 'bin'), (Join-Path $rust 'lib/rustlib/x86_64-pc-windows-gnu/bin/self-contained'), $llvm,
    (Join-Path $root 'cmake-3.31.8-windows-x86_64/bin'), (Join-Path $root 'ninja-1.12.1'), (Join-Path $root 'dotnet-8.0.414'), $env:PATH) -join ';'
