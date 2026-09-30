# Run with Windows PowerShell 5.1 (UIAutomationClient is the Windows framework assembly).
param([Parameter(Mandatory)][string]$Executable, [switch]$ValidatePassword, [string]$InputScreenshot)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$process = Start-Process -FilePath $Executable -PassThru
try {
    $deadline = [DateTime]::UtcNow.AddSeconds(30)
    do {
        Start-Sleep -Milliseconds 100
        $process.Refresh()
        if ($process.HasExited) { throw 'Probe exited' }
    } until (($process.MainWindowHandle -ne [IntPtr]::Zero -and $process.MainWindowTitle.StartsWith('Tessaveil synthetic')) -or [DateTime]::UtcNow -gt $deadline)
    if (!$process.MainWindowTitle.StartsWith('Tessaveil synthetic')) { throw 'No probe window' }
    $root = [System.Windows.Automation.AutomationElement]::FromHandle($process.MainWindowHandle)
    Start-Sleep -Milliseconds 2000
    $queue = New-Object 'System.Collections.Generic.Queue[System.Windows.Automation.AutomationElement]'
    $queue.Enqueue($root)
    $walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
    $observed = 0
    $passwordCount = 0
    $inputSetSucceeded = $false
    $controls = @()
    while ($queue.Count -gt 0 -and $observed -lt 300) {
        $node = $queue.Dequeue(); $observed++
        $c = $node.Current
        if ($c.ControlType.ProgrammaticName -in @('ControlType.Edit', 'ControlType.Button', 'ControlType.Table', 'ControlType.DataGrid')) {
            $exposed = $false
            if ($c.IsPassword) {
                $passwordCount++
                try {
                    $valuePattern = $node.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
                    $value = $valuePattern.Current.Value; $exposed = ($value -eq 'TEST-INPUT-42!'); $value = $null
                    $valuePattern.SetValue('TEST-EDIT-99!'); $inputSetSucceeded = $true
                    $value = $valuePattern.Current.Value; $exposed = $exposed -or ($value -eq 'TEST-EDIT-99!'); $value = $null
                } catch { }
            }
            $controls += [ordered]@{ role=$c.ControlType.ProgrammaticName; name=$c.Name; password=$c.IsPassword; synthetic_password_exposed=$exposed; keyboard_focusable=$c.IsKeyboardFocusable; offscreen=$c.IsOffscreen }
        }
        if ($c.ControlType.ProgrammaticName -in @('ControlType.Table', 'ControlType.DataGrid', 'ControlType.List')) { continue }
        $child = $walker.GetFirstChild($node)
        while ($child -and $queue.Count -lt 300) { $queue.Enqueue($child); $child = $walker.GetNextSibling($child) }
    }
    if ($InputScreenshot) {
        & (Join-Path $PSScriptRoot 'capture-window.ps1') -ExistingProcessId $process.Id -Output $InputScreenshot
    }
    $invoke = $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants,
        [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty, 'Invoke core'))
    $invoked = $false
    if ($invoke) {
        $pattern = $invoke.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
        $pattern.Invoke(); $invoked = $true
    }
    Start-Sleep -Milliseconds 200
    $core = $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants,
        [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty, 'Core: 1'))
    [ordered]@{ observer='Windows PowerShell 5.1 / UIAutomationClient'; observed_nodes=$observed; controls=$controls; input_set_succeeded=$inputSetSucceeded; invoke_pattern_called=$invoked; core_one_visible=($null -ne $core); limitation='Bounded UIA smoke observation excluding table descendants; not Narrator or keyboard/scaling certification' } | ConvertTo-Json -Depth 6
    if ($ValidatePassword -and ($passwordCount -ne 1 -or @($controls | Where-Object synthetic_password_exposed).Count -ne 0 -or !$inputSetSucceeded -or !$invoked -or !$core)) { throw 'Password/core UIA contract failed' }
} finally {
    if (!$process.HasExited) {
        [void]$process.CloseMainWindow()
        if (!$process.WaitForExit(10000)) { $process.Kill() }
    }
    $process.Dispose()
}
