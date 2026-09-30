# Development-host UIA, not clean Windows or Narrator certification.
param([Parameter(Mandatory)][string]$Executable,[Parameter(Mandatory)][string]$Fixture,[Parameter(Mandatory)][string]$ScreenshotRoot,[ValidateSet('1','1.5','2')][string]$Scale='1',[switch]$LaunchOnly,[ValidatePattern('^[a-f0-9]{40}$')][string]$SourceSha)
$ErrorActionPreference='Stop'
$observedExeHash=(Get-FileHash -LiteralPath $Executable -Algorithm SHA256).Hash.ToLowerInvariant()
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System; using System.Runtime.InteropServices;
public static class AlphaCapture {
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [StructLayout(LayoutKind.Sequential)] public struct Rect {public int Left,Top,Right,Bottom;}
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out Rect r);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h,IntPtr dc,uint flags);
}
'@
[void][AlphaCapture]::SetProcessDPIAware()
$env:QT_ENABLE_HIGHDPI_SCALING='0'
$env:QT_SCALE_FACTOR=$Scale
New-Item -ItemType Directory -Force $ScreenshotRoot | Out-Null
# This is the requested visible application under test, not a background helper.
$start=[Diagnostics.ProcessStartInfo]::new($Executable)
$start.UseShellExecute=$false
$start.WorkingDirectory=Split-Path $Fixture
$start.EnvironmentVariables['QT_ENABLE_HIGHDPI_SCALING']='0'
$start.EnvironmentVariables['QT_SCALE_FACTOR']=$Scale
$process=[Diagnostics.Process]::Start($start)
function Find([string]$name){
 $node=$script:root.FindFirst([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty,$name))
 if(!$node){
  $windows=[Windows.Automation.AutomationElement]::RootElement.FindAll([Windows.Automation.TreeScope]::Children,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::ProcessIdProperty,$process.Id))
  foreach($window in $windows){$node=$window.FindFirst([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty,$name));if($node){break}}
 }
 if(!$node){throw "Missing expected control: $name"};return $node
}
function Invoke([string]$name){(Find $name).GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke();Start-Sleep -Milliseconds 150}
function SetValue([string]$name,[string]$value){(Find $name).GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue($value)}
function Capture([string]$name){
 if($Scale -ne '1' -and $name -ne 'table-36'){return}
 $r=[AlphaCapture+Rect]::new();if(![AlphaCapture]::GetWindowRect($process.MainWindowHandle,[ref]$r)){throw 'Window bounds unavailable'}
 $bitmap=[Drawing.Bitmap]::new($r.Right-$r.Left,$r.Bottom-$r.Top);$graphics=[Drawing.Graphics]::FromImage($bitmap);$dc=$graphics.GetHdc()
 try{if(![AlphaCapture]::PrintWindow($process.MainWindowHandle,$dc,2)){throw 'PrintWindow unavailable'}}finally{$graphics.ReleaseHdc($dc)}
 try{$bitmap.Save((Join-Path $ScreenshotRoot "$name-scale-$Scale.png"),[Drawing.Imaging.ImageFormat]::Png)}finally{$graphics.Dispose();$bitmap.Dispose()}
}
try{
 $deadline=[DateTime]::UtcNow.AddSeconds(20)
 do{Start-Sleep -Milliseconds 100;$process.Refresh()}until($process.HasExited -or ($process.MainWindowHandle -ne [IntPtr]::Zero -and $process.MainWindowTitle.StartsWith('Tessaveil')) -or [DateTime]::UtcNow -gt $deadline)
 if($process.HasExited -or $process.MainWindowHandle -eq [IntPtr]::Zero){throw 'No live alpha window'}
 $script:root=[Windows.Automation.AutomationElement]::FromHandle($process.MainWindowHandle)
 [void](Find ("I understand " + [char]0x2014 + " use synthetic data only"))
 Start-Sleep -Milliseconds 500
 Capture 'launch'
 if($LaunchOnly){return}
 Invoke ("I understand " + [char]0x2014 + " use synthetic data only")
 $master=Find 'Master password';if(!$master.Current.IsPassword -or !$master.Current.IsKeyboardFocusable){throw 'Password semantics absent'}
 $passwordResults=@()
 foreach($value in @('TEST-INPUT-42!','TEST-EDIT-99!')){
  $master.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue($value)
  $read=$master.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).get_Current().get_Value()
  if($null -eq $read -or $read -isnot [string] -or $read -notmatch '^[\*\u2022\u25cf]*$'){throw 'Password observation failed closed'}
  $passwordResults+=@{getter='OBSERVED_MASKED';setter='SET';password=$true}
 }
 $master.SetFocus();$focus=$master.Current.HasKeyboardFocus
 if(!$focus){throw 'Password focus was not observed'}
 SetValue 'Vault path on development local NTFS' (Split-Path $Fixture -Leaf)
 SetValue 'Master password' 'synthetic-master-password'
 Invoke 'Open vault'
 [void](Find 'Open / saved')
 Capture 'table-10'
 Invoke 'Next sheet'
 $combo=Find 'Current sheet'
 if($combo.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).get_Current().get_Value() -ne 'Synthetic 36 columns'){throw 'Sheet selection did not commit'}
 Start-Sleep -Milliseconds 200;Capture 'table-36'
 $protectedInputs=$script:root.FindAll([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::IsPasswordProperty,$true))
 if($protectedInputs.Count -ne 5){throw 'Expected five password-semantic inputs'}
 foreach($input in $protectedInputs){
  $input.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue('TEST-EDIT-99!')
  $read=$input.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).get_Current().get_Value()
  if($null -eq $read -or $read -isnot [string] -or $read -notmatch '^[\*\u2022\u25cf]*$'){throw 'Secret control exposed value'}
  $input.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue('')
 }
 Invoke 'Lock';[void](Find ("Locked " + [char]0x2014 + " enter master password to reopen"));Capture 'locked'
 SetValue 'Master password' 'synthetic-wrong-password';Invoke 'Unlock vault'
 [void](Find 'The password is incorrect or the vault is damaged.');Capture 'authentication-error'
 SetValue 'Master password' 'synthetic-master-password';Invoke 'Unlock vault';[void](Find 'Open / saved')
 Invoke 'Close vault';[void](Find 'Closed')
 if((Get-FileHash -LiteralPath $Executable -Algorithm SHA256).Hash.ToLowerInvariant() -ne $observedExeHash){throw 'Observed executable changed during UIA smoke'}
 [ordered]@{source_sha=$SourceSha;exe_sha256=$observedExeHash;scale=$Scale;password_observations=$passwordResults;all_five_password_controls_masked=$true;keyboard_focus_observed=$focus;open_close_reopen_lock=$true;authentication_safe=$true;modules=@($process.Modules|ForEach-Object{$_.ModuleName}|Sort-Object -Unique);scope='Development host UIA only; no clean Windows, Narrator, clipboard contents, network trace or release claim'}|ConvertTo-Json -Depth 5
}finally{
 if(!$process.HasExited){[void]$process.CloseMainWindow();if(!$process.WaitForExit(5000)){$process.Kill()}}
 $process.Dispose()
}
