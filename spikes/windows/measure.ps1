param(
    [Parameter(Mandatory)][string]$Executable,
    [Parameter(Mandatory)][string]$ReadObj,
    [Parameter(Mandatory)][string]$ObservationRoot,
    [int]$Runs = 10
)
$ErrorActionPreference = 'Stop'
if ($Runs -lt 10) { throw 'At least ten warm launches are required' }
$exe = Get-Item -LiteralPath $Executable
if (Test-Path -LiteralPath $ObservationRoot) { throw 'ObservationRoot must be new' }
New-Item -ItemType Directory -Path $ObservationRoot | Out-Null
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class ProbeObservation {
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll", SetLastError=true)] public static extern IntPtr SendMessageTimeout(IntPtr h, uint m, IntPtr w, IntPtr l, uint flags, uint timeout, out IntPtr result);
 [DllImport("dwmapi.dll")] public static extern int DwmFlush();
}
'@
$timings = @(); $modules = @(); $temporary = @(); $peaks = @()
for ($i = 0; $i -lt $Runs; $i++) {
    $temp = Join-Path $ObservationRoot "run-$i"
    New-Item -ItemType Directory -Path $temp | Out-Null
    $before = @(Get-ChildItem -LiteralPath $temp -File -Recurse -Force -ErrorAction Stop | ForEach-Object { $_.FullName.Substring($temp.Length + 1) })
    $start = [Diagnostics.ProcessStartInfo]::new($exe.FullName)
    $start.UseShellExecute = $false
    $start.WorkingDirectory = $exe.DirectoryName
    $start.Environment['TEMP'] = $temp; $start.Environment['TMP'] = $temp
    # Never permit a developer toolchain PATH to satisfy runtime DLL lookup.
    $start.Environment['PATH'] = "$env:SystemRoot\System32;$env:SystemRoot"
    $clock = [Diagnostics.Stopwatch]::StartNew()
    $process = [Diagnostics.Process]::Start($start)
    try {
        while ($true) {
            $process.Refresh()
            if ($process.HasExited) { throw "Probe exited before ready: $($process.ExitCode)" }
            $window = $process.MainWindowHandle
            $reply = [IntPtr]::Zero
            if ($process.MainWindowTitle.StartsWith('Tessaveil synthetic') -and $window -ne [IntPtr]::Zero -and [ProbeObservation]::IsWindowVisible($window) -and
                [ProbeObservation]::SendMessageTimeout($window, 0, [IntPtr]::Zero, [IntPtr]::Zero, 2, 100, [ref]$reply) -ne [IntPtr]::Zero) { break }
            if ($clock.Elapsed.TotalSeconds -gt 30) { throw 'Window readiness timeout' }
            Start-Sleep -Milliseconds 5
        }
        [void][ProbeObservation]::DwmFlush()
        $timings += [Math]::Round($clock.Elapsed.TotalMilliseconds, 3)
        Start-Sleep -Milliseconds 300
        $process.Refresh()
        $modules += @($process.Modules | ForEach-Object ModuleName)
        $peaks += $process.PeakWorkingSet64
        if (!$process.CloseMainWindow()) { throw 'Could not request normal window close' }
        if (!$process.WaitForExit(10000)) { throw 'Probe did not close normally' }
        if ($process.ExitCode -ne 0) { throw "Probe exit: $($process.ExitCode)" }
    } finally {
        if (!$process.HasExited) { $process.Kill(); $process.WaitForExit() }
        $process.Dispose()
    }
    $after = @(Get-ChildItem -LiteralPath $temp -File -Recurse -Force -ErrorAction Stop | ForEach-Object { $_.FullName.Substring($temp.Length + 1) })
    $temporary += [ordered]@{ run=$i; before=$before; after=$after }
}
$imports = & $ReadObj --coff-imports $exe.FullName
if ($LASTEXITCODE -ne 0) { throw 'PE inspection failed' }
$names = @($imports | Select-String '^  Name: ' | ForEach-Object { $_.Line.Trim().Substring(6) })
[ordered]@{
    scope='development-host; not clean Windows evidence'
    startup_definition='Process.Start to visible top-level HWND answering WM_NULL plus DwmFlush; not instrumented first-content-frame'
    startup_ms=$timings
    artifacts=@([ordered]@{path=$exe.Name; bytes=$exe.Length; sha256=(Get-FileHash -LiteralPath $exe.FullName).Hash.ToLowerInvariant()})
    pe_imports=$names
    loaded_modules=@($modules | Sort-Object -Unique)
    peak_working_set_bytes=$peaks
    temp_before=@($temporary | ForEach-Object { $_.before })
    temp_after=@($temporary | ForEach-Object { $_.after })
    temp_runs=$temporary
    limitations=@('Warm sequential dev-host launches, no cold boots', 'Snapshots cannot detect create-delete extraction; no full process-tree event trace', 'No clean-machine, Narrator, network or scaling certification')
} | ConvertTo-Json -Depth 8
