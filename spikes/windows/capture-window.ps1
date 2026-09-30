param([string]$Executable, [int]$ExistingProcessId, [Parameter(Mandatory)][string]$Output)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System; using System.Runtime.InteropServices;
public static class ProbeCapture {
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [StructLayout(LayoutKind.Sequential)] public struct Rect { public int Left, Top, Right, Bottom; }
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out Rect r);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint flags);
}
'@
[void][ProbeCapture]::SetProcessDPIAware()
$p = if ($ExistingProcessId) { [Diagnostics.Process]::GetProcessById($ExistingProcessId) } else { [Diagnostics.Process]::Start($Executable) }
try {
    $deadline = [DateTime]::UtcNow.AddSeconds(30)
    do { Start-Sleep -Milliseconds 100; $p.Refresh() } until ($p.HasExited -or ($p.MainWindowHandle -ne [IntPtr]::Zero -and $p.MainWindowTitle.StartsWith('Tessaveil synthetic')) -or [DateTime]::UtcNow -gt $deadline)
    if ($p.HasExited -or !$p.MainWindowTitle.StartsWith('Tessaveil synthetic')) { throw 'No live probe window' }
    Start-Sleep -Seconds 3
    $p.Refresh()
    $r = [ProbeCapture+Rect]::new()
    [void][ProbeCapture]::GetWindowRect($p.MainWindowHandle, [ref]$r)
    $bitmap = [Drawing.Bitmap]::new($r.Right-$r.Left, $r.Bottom-$r.Top)
    $graphics = [Drawing.Graphics]::FromImage($bitmap)
    $dc = $graphics.GetHdc()
    try { if (![ProbeCapture]::PrintWindow($p.MainWindowHandle, $dc, 2)) { throw 'PrintWindow failed' } }
    finally { $graphics.ReleaseHdc($dc) }
    $bitmap.Save($Output, [Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose(); $bitmap.Dispose()
} finally {
    if (!$ExistingProcessId -and !$p.HasExited) { [void]$p.CloseMainWindow(); if (!$p.WaitForExit(10000)) { $p.Kill() } }
    $p.Dispose()
}
