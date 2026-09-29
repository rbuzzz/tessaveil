#requires -Version 7.4
# Explicit opt-in harness: creates small synthetic tests only in dedicated Public roots.
[CmdletBinding()]
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'ReplaceProbe.ps1')

function New-TestRoot {
    $public = Get-ProbePublicDirectory
    [TessaveilFsProbe.Paths]::RequireLocalDrive([IO.Path]::GetPathRoot($public))
    [TessaveilFsProbe.Paths]::RequireNotCloud($public)
    $pin = [TessaveilFsProbe.Paths]::Pin($public, $true)
    try {
        $path = Join-Path $public ('TessaveilReplaceProbe-' + [guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $path -ErrorAction Stop | Out-Null
        $pins = Open-ProbeRoot -Path $path -RequireEmpty
        foreach ($handle in $pins) { $handle.Dispose() }
        return $path
    } finally { $pin.Dispose() }
}

function Remove-TestRoot {
    param([string] $Path)
    $pins = Open-ProbeRoot -Path $Path
    try {
        # No recursive removal, wildcards, or user-provided file names.
        $files = @([IO.Directory]::EnumerateFileSystemEntries($Path))
        foreach ($file in $files) { Assert-ProbeFile $Path $file -MustExist }
        foreach ($file in $files) {
            Assert-ProbeFile $Path $file -MustExist
            [IO.File]::Delete($file)
        }
    } finally { foreach ($handle in $pins) { $handle.Dispose() } }
    $emptyPins = Open-ProbeRoot -Path $Path -RequireEmpty
    foreach ($handle in $emptyPins) { $handle.Dispose() }
    [IO.Directory]::Delete($Path, $false)
}

$matrix = @()
foreach ($phase in @('AfterCreate','AfterWrite','AfterFlush','AfterVerify','BeforeReplace','AfterReplace','None')) {
    $testRoot = New-TestRoot
    try {
        $start = [Diagnostics.ProcessStartInfo]::new((Get-Process -Id $PID).Path)
        $start.UseShellExecute = $false
        $start.CreateNoWindow = $true
        $start.RedirectStandardOutput = $true
        $start.RedirectStandardError = $true
        foreach ($argument in @('-NoProfile','-NonInteractive','-File', (Join-Path $PSScriptRoot 'ReplaceProbe.ps1'), '-Root', $testRoot, '-FailurePhase', $phase)) {
            $start.ArgumentList.Add($argument)
        }
        $child = [Diagnostics.Process]::Start($start)
        try {
            $stdoutTask = $child.StandardOutput.ReadToEndAsync()
            $stderrTask = $child.StandardError.ReadToEndAsync()
            if (!$child.WaitForExit(20000)) { $child.Kill(); $child.WaitForExit(); throw 'Probe exceeded 20-second bound' }
            $stdout = $stdoutTask.GetAwaiter().GetResult()
            $stderr = $stderrTask.GetAwaiter().GetResult()
            $expectedExit = if ($phase -eq 'None') { 0 } else { 86 }
            if ($child.ExitCode -ne $expectedExit -or $stderr) { throw "Probe $phase failed: $stderr" }
            $hashes = $stdout | ConvertFrom-Json
            $pins = Open-ProbeRoot -Path $testRoot
            try {
                $target = Join-Path $testRoot 'vault.tessaveil'
                Assert-ProbeFile $testRoot $target -MustExist
                if ((Get-Item -LiteralPath $target).Length -ne 4140) { throw 'Incomplete result' }
                $image = [IO.File]::ReadAllBytes($target)
                $authenticated = Test-ProbeImage $image
                if (!$authenticated) { throw 'Unauthenticated result' }
                $actualHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($image)).ToLowerInvariant()
                $expected = if ($phase -in @('AfterReplace','None')) { 'new' } else { 'old' }
                $expectedHash = if ($expected -eq 'new') { $hashes.new_sha256 } else { $hashes.old_sha256 }
                if ($actualHash -cne $expectedHash -or $hashes.old_sha256 -ceq $hashes.new_sha256) { throw 'Wrong complete image survived' }
                $temporary = Join-Path $testRoot 'update.tmp.tessaveil'
                $tempLength = $null
                $tempAuthenticated = $null
                if ([IO.File]::Exists($temporary)) {
                    Assert-ProbeFile $testRoot $temporary -MustExist
                    $tempLength = (Get-Item -LiteralPath $temporary).Length
                    if ($tempLength -gt 4140) { throw 'Unbounded temporary image' }
                    $tempAuthenticated = Test-ProbeImage ([IO.File]::ReadAllBytes($temporary))
                }
                $matrix += [ordered]@{
                    phase = $phase; exit_code = $child.ExitCode; observed = $expected
                    authenticated = $authenticated; target_length = $image.Length
                    temporary_length = $tempLength; temporary_authenticated = $tempAuthenticated
                    old_sha256 = $hashes.old_sha256; new_sha256 = $hashes.new_sha256
                    actual_sha256 = $actualHash
                }
            } finally { foreach ($handle in $pins) { $handle.Dispose() } }
        } finally { $child.Dispose() }
    } finally { Remove-TestRoot $testRoot }
}

$nonempty = New-TestRoot
try {
    $pins = Open-ProbeRoot -Path $nonempty -RequireEmpty
    try {
        $sentinel = Join-Path $nonempty 'sentinel.bin'
        Assert-ProbeFile $nonempty $sentinel
        $stream = [IO.FileStream]::new($sentinel, [IO.FileMode]::CreateNew)
        try { $stream.Write([byte[]]@(1,2,3), 0, 3) } finally { $stream.Dispose() }
        $rejected = $false
        try { Invoke-ReplaceProbe -Root $nonempty }
        catch { if ($_.Exception.Message -notlike '*Nonempty directory refused*') { throw }; $rejected = $true }
        if (!$rejected -or [Convert]::ToHexString([IO.File]::ReadAllBytes($sentinel)) -cne '010203') { throw 'Nonempty target damaged or accepted' }
    } finally { foreach ($handle in $pins) { $handle.Dispose() } }
} finally { Remove-TestRoot $nonempty }

$junctionTarget = New-TestRoot
$junctionPath = Join-Path (Get-ProbePublicDirectory) ('TessaveilReplaceProbe-' + [guid]::NewGuid().ToString('N'))
try {
    New-Item -ItemType Junction -Path $junctionPath -Target $junctionTarget -ErrorAction Stop | Out-Null
    $rejected = $false
    try { Invoke-ReplaceProbe -Root $junctionPath }
    catch { if ($_.Exception.Message -notlike '*Reparse/offline/cloud attribute refused*') { throw }; $rejected = $true }
    if (!$rejected -or @([IO.Directory]::EnumerateFileSystemEntries($junctionTarget)).Count -ne 0) { throw 'Junction target damaged or accepted' }
} finally {
    # This one known synthetic junction is removed as a link, never recursively.
    $link = Get-Item -LiteralPath $junctionPath -ErrorAction Stop
    if ($link.Parent.FullName -cne (Get-ProbePublicDirectory) -or $link.FullName -cne $junctionPath -or
        $link.LinkType -ne 'Junction' -or $link.Target -cne $junctionTarget) { throw 'Unexpected junction cleanup target' }
    [IO.Directory]::Delete($junctionPath, $false)
    Remove-TestRoot $junctionTarget
}

$os = Get-CimInstance Win32_OperatingSystem
$version = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
[ordered]@{
    verified_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    os = $os.Caption; os_version = $os.Version; os_build = "$($version.CurrentBuild).$($version.UBR)"
    os_architecture = $os.OSArchitecture; display_version = $version.DisplayVersion
    powershell = $PSVersionTable.PSVersion.ToString()
    dotnet = [Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
    filesystem = 'NTFS'; device_class = 'local fixed development volume'
    scope = 'process interruption at named boundaries only'; release_readiness = 'NO-GO'
    api = 'FileStream.CreateNew -> Write -> Flush(true) -> close/reopen -> AES-GCM verify -> File.Replace(no backup, ignoreMetadataErrors=false)'
    fixture_sha256 = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'fixtures/header-and-ciphertext.bin')).Hash.ToLowerInvariant()
    nonempty_rejected = $true; junction_rejected = $true; matrix = $matrix
} | ConvertTo-Json -Depth 6
