# Read-only discovery. Presence of a command is never evidence of a usable build.
# Deliberately does not execute discovered tools, launch GUI programs, or install anything.
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$commandNames = @('dotnet', 'rustc', 'cargo', 'rustup', 'cmake', 'ninja',
    'qmake6', 'qmake', 'qtpaths6', 'cl', 'clang', 'dumpbin', 'python')
$inventory = foreach ($name in $commandNames) {
    $found = Get-Command -Name $name -CommandType Application -ErrorAction SilentlyContinue
    [ordered]@{ name = $name; available = [bool]$found }
}
$defaultLocations = @()
if ($IsWindows) {
    $defaultLocations = @(
        @{ name = 'dotnet default'; path = "$env:ProgramFiles\dotnet\dotnet.exe" },
        @{ name = 'Rust default'; path = "$env:USERPROFILE\.cargo\bin\rustc.exe" },
        @{ name = 'CMake default'; path = "$env:ProgramFiles\CMake\bin\cmake.exe" },
        @{ name = 'Qt default'; path = 'C:\Qt' },
        @{ name = 'VS locator'; path = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" }
    )
}
$defaults = @(foreach ($entry in $defaultLocations) {
    [ordered]@{ name = $entry.name; present = (Test-Path -LiteralPath $entry.path) }
})
[ordered]@{
    scope = 'read-only discovery; not build or clean-machine evidence'
    verified_utc = [DateTime]::UtcNow.ToString('yyyy-MM-dd')
    powershell_version = $PSVersionTable.PSVersion.ToString()
    windows_host = $IsWindows
    commands = @($inventory)
    default_locations = $defaults
    release_readiness = 'NO-GO'
} | ConvertTo-Json -Depth 4
