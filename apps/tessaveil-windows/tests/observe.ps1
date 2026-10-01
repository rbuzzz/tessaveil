# Development-host UIA, not clean Windows or Narrator certification.
param([Parameter(Mandatory)][string]$Executable,[Parameter(Mandatory)][string]$Fixture,[Parameter(Mandatory)][string]$ScreenshotRoot,[ValidateSet('1','1.5','2')][string]$Scale='1',[switch]$LaunchOnly,[ValidatePattern('^[a-f0-9]{40}$')][string]$SourceSha)
$ErrorActionPreference='Stop'
$observedExeHash=(Get-FileHash -LiteralPath $Executable -Algorithm SHA256).Hash.ToLowerInvariant()
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System; using System.Text; using System.Threading; using System.Runtime.InteropServices;
public static class AlphaCapture {
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [StructLayout(LayoutKind.Sequential)] public struct Rect {public int Left,Top,Right,Bottom;}
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out Rect r);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h,IntPtr dc,uint flags);
 [DllImport("user32.dll")] static extern bool ShowWindow(IntPtr h,int command);
 [DllImport("user32.dll")] static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] static extern bool BringWindowToTop(IntPtr h);
 [DllImport("user32.dll")] static extern IntPtr SetFocus(IntPtr h);
 [DllImport("user32.dll")] static extern IntPtr SetActiveWindow(IntPtr h);
 [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] static extern IntPtr GetLastActivePopup(IntPtr h);
 [DllImport("user32.dll")] static extern IntPtr GetWindow(IntPtr h,uint command);
 [DllImport("user32.dll")] static extern bool IsWindow(IntPtr h);
 [DllImport("user32.dll")] static extern bool PostMessage(IntPtr h,uint message,IntPtr wParam,IntPtr lParam);
 [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
 [DllImport("user32.dll")] static extern bool AttachThreadInput(uint from,uint to,bool attach);
 [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc callback,IntPtr data);
 [DllImport("user32.dll")] static extern bool EnumChildWindows(IntPtr parent,EnumProc callback,IntPtr data);
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h,out uint processId);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern int GetClassName(IntPtr h,StringBuilder value,int size);
 [DllImport("user32.dll")] static extern int GetDlgCtrlID(IntPtr h);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern IntPtr SendMessage(IntPtr h,uint message,IntPtr wParam,string value);
 [DllImport("user32.dll")] static extern IntPtr SendMessage(IntPtr h,uint message,IntPtr wParam,IntPtr lParam);
 delegate bool EnumProc(IntPtr h,IntPtr data);
 static bool HasClass(IntPtr h,string expected){var value=new StringBuilder(64);GetClassName(h,value,value.Capacity);return value.ToString()==expected;}
 public static IntPtr FindDialog(int processId){IntPtr result=IntPtr.Zero;EnumWindows((h,data)=>{uint candidate;GetWindowThreadProcessId(h,out candidate);if(candidate==processId&&HasClass(h,"#32770")){result=h;return false;}return true;},IntPtr.Zero);return result;}
 public static IntPtr LastActivePopup(IntPtr h){return GetLastActivePopup(h);}
 public static IntPtr FindChild(IntPtr parent,int id,string className){IntPtr result=IntPtr.Zero;EnumChildWindows(parent,(h,data)=>{if(GetDlgCtrlID(h)==id&&HasClass(h,className)){result=h;return false;}return true;},IntPtr.Zero);return result;}
 public static string ActivationState(IntPtr candidate){uint candidateProcess;uint candidateThread=GetWindowThreadProcessId(candidate,out candidateProcess);IntPtr foreground=GetForegroundWindow();uint foregroundProcess;uint foregroundThread=GetWindowThreadProcessId(foreground,out foregroundProcess);string foregroundName="unavailable";try{foregroundName=System.Diagnostics.Process.GetProcessById((int)foregroundProcess).ProcessName;}catch{}return String.Format("candidate={0} candidateValid={1} candidatePid={2} candidateTid={3} foreground={4} foregroundPid={5} foregroundTid={6} foregroundName={7}",candidate.ToInt64(),IsWindow(candidate),candidateProcess,candidateThread,foreground.ToInt64(),foregroundProcess,foregroundThread,foregroundName);}
 public static void SetText(IntPtr h,string value){SendMessage(h,0x000C,IntPtr.Zero,value);}
 public static bool Activate(IntPtr h){uint processId;uint target=GetWindowThreadProcessId(h,out processId);uint foregroundProcess;uint foreground=GetWindowThreadProcessId(GetForegroundWindow(),out foregroundProcess);uint current=GetCurrentThreadId();bool foregroundAttached=current!=foreground&&AttachThreadInput(current,foreground,true);bool targetAttached=current!=target&&AttachThreadInput(current,target,true);try{ShowWindow(h,9);BringWindowToTop(h);SetActiveWindow(h);SetFocus(h);SetForegroundWindow(h);bool active=GetForegroundWindow()==h;if(active)SendMessage(h,0x0006,(IntPtr)1,IntPtr.Zero);return active;}finally{if(targetAttached)AttachThreadInput(current,target,false);if(foregroundAttached)AttachThreadInput(current,foreground,false);}}
 public static void ClickAndActivateOwner(IntPtr button,IntPtr dialog,IntPtr main){IntPtr target=GetWindow(dialog,4);if(target==IntPtr.Zero)target=main;PostMessage(button,0x00F5,IntPtr.Zero,IntPtr.Zero);new Thread(()=>{DateTime deadline=DateTime.UtcNow.AddSeconds(5);while(IsWindow(dialog)&&DateTime.UtcNow<deadline)Thread.Sleep(1);for(int i=0;i<25;i++){Activate(target);Thread.Sleep(10);}}){IsBackground=true}.Start();}
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
function TryFind([string]$name){
 $node=$script:root.FindFirst([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty,$name))
 if(!$node){
  $windows=[Windows.Automation.AutomationElement]::RootElement.FindAll([Windows.Automation.TreeScope]::Children,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::ProcessIdProperty,$process.Id))
  foreach($window in $windows){$node=$window.FindFirst([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty,$name));if($node){break}}
 }
 return $node
}
function Find([string]$name){$node=TryFind $name;if(!$node){throw "Missing expected control: $name"};return $node}
function FindValue([string]$name){
 $windows=[Windows.Automation.AutomationElement]::RootElement.FindAll([Windows.Automation.TreeScope]::Children,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::ProcessIdProperty,$process.Id))
 foreach($window in $windows){
  $nodes=$window.FindAll([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty,$name))
  foreach($node in $nodes){try{[void]$node.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern);return $node}catch{}}
 }
 throw "Missing value control: $name"
}
function WaitValue([string]$name){
 $deadline=[DateTime]::UtcNow.AddSeconds(10)
 do{
  Start-Sleep -Milliseconds 100
  try{$node=FindValue $name}catch{$node=$null}
 }until($node -or [DateTime]::UtcNow -gt $deadline)
 if(!$node){throw "Missing value control after bounded wait: $name; observed state: $(DiagnosticState)"}
 return $node
}
function FindAutomationIdSuffix([string]$suffix){
 $nodes=$script:root.FindAll([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.Condition]::TrueCondition)
 foreach($node in $nodes){
  $id=$node.Current.AutomationId
  if($id -eq $suffix -or $id.EndsWith(".$suffix")){return $node}
 }
 throw "Missing control with AutomationId suffix: $suffix"
}
function TryFindPassword([string]$name){
 $windows=[Windows.Automation.AutomationElement]::RootElement.FindAll([Windows.Automation.TreeScope]::Children,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::ProcessIdProperty,$process.Id))
 foreach($window in $windows){
  $nodes=$window.FindAll([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty,$name))
  foreach($node in $nodes){if($node.Current.IsPassword -and $node.Current.IsKeyboardFocusable -and !$node.Current.IsOffscreen){return $node}}
 }
 return $null
}
function WaitPassword([string]$name){$deadline=[DateTime]::UtcNow.AddSeconds(10);do{Start-Sleep -Milliseconds 100;$node=TryFindPassword $name}until($node -or [DateTime]::UtcNow -gt $deadline);if(!$node){throw "Missing visible password control after bounded wait: $name"};return $node}
function ActivateApplication(){
 $deadline=[DateTime]::UtcNow.AddSeconds(5)
 $stable=0
 do{
  if([AlphaCapture]::Activate($script:mainWindowHandle)){$stable++}else{$stable=0}
  Start-Sleep -Milliseconds 25
 }until($stable -ge 8 -or [DateTime]::UtcNow -gt $deadline)
 if($stable -lt 8){throw 'Application could not retain foreground through the bounded activation window'}
 $script:root=[Windows.Automation.AutomationElement]::FromHandle($script:mainWindowHandle)
}
function ActivateOwnedDialog(){
 $deadline=[DateTime]::UtcNow.AddSeconds(5)
 $stable=0
 $lastState='no candidate observed'
 do{
  $candidate=[AlphaCapture]::LastActivePopup($script:mainWindowHandle)
  if($candidate -eq [IntPtr]::Zero){$candidate=$script:mainWindowHandle}
  if([AlphaCapture]::Activate($candidate)){$stable++}else{$stable=0}
  $lastState=[AlphaCapture]::ActivationState($candidate)
  Start-Sleep -Milliseconds 25
 }until($stable -ge 4 -or [DateTime]::UtcNow -gt $deadline)
 if($stable -lt 4){throw "The owning application dialog could not retain foreground through the bounded activation window: $lastState"}
 $script:root=[Windows.Automation.AutomationElement]::FromHandle($script:mainWindowHandle)
}
function DiagnosticState(){
 $values=@()
 $nodes=$script:root.FindAll([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.Condition]::TrueCondition)
 foreach($node in $nodes){if($node.Current.AutomationId -match '\.(state|message)$' -or $node.Current.Name -eq 'Tessaveil is covered while inactive'){$values+=$node.Current.Name}}
 if($values.Count -eq 0){
  foreach($node in $nodes){
   if($values.Count -ge 20){break}
   if($node.Current.Name -or $node.Current.AutomationId){$values+=("{0}[{1}]" -f $node.Current.Name,$node.Current.AutomationId)}
  }
 }
 return ($values -join ' | ')
}
function WaitFind([string]$name){$deadline=[DateTime]::UtcNow.AddSeconds(10);do{Start-Sleep -Milliseconds 100;$node=TryFind $name}until($node -or [DateTime]::UtcNow -gt $deadline);if(!$node){throw "Missing expected control after bounded wait: $name; observed state: $(DiagnosticState)"};return $node}
function Invoke([string]$name){(Find $name).GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke();Start-Sleep -Milliseconds 150}
function SetValue([string]$name,[string]$value){(Find $name).GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue($value)}
function ChooseFile([string]$button,[string]$value){
 Invoke $button
 $deadline=[DateTime]::UtcNow.AddSeconds(10)
 $dialog=[IntPtr]::Zero
 $name=[IntPtr]::Zero
 $open=[IntPtr]::Zero
 do{
  Start-Sleep -Milliseconds 100
  $dialog=[AlphaCapture]::FindDialog($process.Id)
  if($dialog -ne [IntPtr]::Zero){
   $name=[AlphaCapture]::FindChild($dialog,1148,'Edit')
   $open=[AlphaCapture]::FindChild($dialog,1,'Button')
  }
 }until(($dialog -ne [IntPtr]::Zero -and $name -ne [IntPtr]::Zero -and $open -ne [IntPtr]::Zero) -or [DateTime]::UtcNow -gt $deadline)
 if($dialog -eq [IntPtr]::Zero){throw 'Native ciphertext picker was not exposed'}
 if($name -eq [IntPtr]::Zero){throw 'Native ciphertext picker did not expose the file-name field'}
 [AlphaCapture]::SetText($name,$value)
 if($open -eq [IntPtr]::Zero){throw 'Native ciphertext picker did not expose its confirmation button'}
 [AlphaCapture]::ClickAndActivateOwner($open,$dialog,$script:mainWindowHandle)
 $process.Refresh()
 ActivateOwnedDialog
}
function Capture([string]$name){
 if($Scale -ne '1' -and $name -ne 'table-36'){return}
 $r=[AlphaCapture+Rect]::new();if(![AlphaCapture]::GetWindowRect($script:mainWindowHandle,[ref]$r)){throw 'Window bounds unavailable'}
 $bitmap=[Drawing.Bitmap]::new($r.Right-$r.Left,$r.Bottom-$r.Top);$graphics=[Drawing.Graphics]::FromImage($bitmap);$dc=$graphics.GetHdc()
 try{if(![AlphaCapture]::PrintWindow($script:mainWindowHandle,$dc,2)){throw 'PrintWindow unavailable'}}finally{$graphics.ReleaseHdc($dc)}
 try{$bitmap.Save((Join-Path $ScreenshotRoot "$name-scale-$Scale.png"),[Drawing.Imaging.ImageFormat]::Png)}finally{$graphics.Dispose();$bitmap.Dispose()}
}
$script:passwordResults=@()
$script:passwordIds=[Collections.Generic.HashSet[string]]::new()
function ObservePassword($element,[string[]]$values){
 if(!$element.Current.IsPassword -or !$element.Current.IsKeyboardFocusable){throw "Password semantics absent for $($element.Current.Name) [$($element.Current.AutomationId)]"}
 [void]$script:passwordIds.Add($element.Current.AutomationId)
 foreach($value in $values){
  $element.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue($value)
  $read=$element.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).get_Current().get_Value()
  if($null -eq $read -or $read -isnot [string] -or $read -notmatch '^[\*\u2022\u25cf]*$'){throw 'Password observation failed closed'}
  $script:passwordResults+=@{getter='OBSERVED_MASKED';setter='SET';password=$true;automation_id=$element.Current.AutomationId}
 }
 $element.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue('')
}
try{
 $deadline=[DateTime]::UtcNow.AddSeconds(20)
 do{Start-Sleep -Milliseconds 100;$process.Refresh()}until($process.HasExited -or ($process.MainWindowHandle -ne [IntPtr]::Zero -and $process.MainWindowTitle.StartsWith('Tessaveil')) -or [DateTime]::UtcNow -gt $deadline)
 if($process.HasExited -or $process.MainWindowHandle -eq [IntPtr]::Zero){throw 'No live alpha window'}
 $script:mainWindowHandle=$process.MainWindowHandle
 $script:root=[Windows.Automation.AutomationElement]::FromHandle($script:mainWindowHandle)
 [void](Find ("I understand " + [char]0x2014 + " use synthetic data only"))
 Start-Sleep -Milliseconds 500
 Capture 'launch'
 if($LaunchOnly){return}
 Invoke ("I understand " + [char]0x2014 + " use synthetic data only")
 Invoke 'Open vault'
 $master=WaitPassword 'Master password'
 ObservePassword $master @('TEST-INPUT-42!','TEST-EDIT-99!')
 $master.SetFocus();$focus=$master.Current.HasKeyboardFocus
 if(!$focus){throw 'Password focus was not observed'}
 ChooseFile ("Browse" + [char]0x2026) $Fixture
 $selectedPath=(WaitValue 'Encrypted vault file').GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).get_Current().get_Value()
 if([IO.Path]::GetFullPath($selectedPath) -ne [IO.Path]::GetFullPath($Fixture)){throw 'Native ciphertext picker selection did not reach the read-only vault path control'}
 SetValue 'Master password' 'synthetic-master-password'
 Invoke 'Continue'
 ActivateApplication
 [void](WaitFind 'State: Open / saved')
 $profileSearch=FindAutomationIdSuffix 'profileFilter'
 $profileValue=$profileSearch.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern)
 if($profileValue.Current.IsReadOnly){throw 'Profile search value is unexpectedly read-only'}
 if([string]::IsNullOrWhiteSpace($profileSearch.Current.Name)){throw 'Profile search accessible name was empty'}
 if(!$profileSearch.Current.IsKeyboardFocusable){throw 'Profile search is not keyboard focusable'}
 $profileSearch.SetFocus()
 if(!$profileSearch.Current.HasKeyboardFocus){throw 'Profile search focus was not observed'}
 $profileValue.SetValue('tonkeeper-multichain')
 $details=FindAutomationIdSuffix 'profileDetails'
 $deadline=[DateTime]::UtcNow.AddSeconds(10)
 do{
  Start-Sleep -Milliseconds 100
  $detailName=$details.Current.Name
}until(($detailName -match 'Keeper / Tonkeeper Multichain' -and
          $detailName -match 'cross-platform' -and
          $detailName -match 'documented' -and
          $detailName -match 'bip39-multichain-generated' -and
          $detailName -match 'documentation-snapshot-2026-09-29-version-unresolved' -and
          $detailName -match 'original wallet') -or [DateTime]::UtcNow -gt $deadline)
 if($detailName -notmatch 'Keeper / Tonkeeper Multichain' -or
    $detailName -notmatch 'cross-platform' -or
    $detailName -notmatch 'documented' -or
    $detailName -notmatch 'bip39-multichain-generated' -or
    $detailName -notmatch 'documentation-snapshot-2026-09-29-version-unresolved' -or
    $detailName -notmatch 'original wallet'){throw "Profile details were not exposed dynamically: $detailName"}
 $profileValue.SetValue('')
 ActivateApplication
 Capture 'table-10'
 ActivateApplication
 (WaitFind 'Next sheet').GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke()
 Start-Sleep -Milliseconds 150
 ActivateApplication
 $combo=Find 'Current sheet'
 if($combo.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).get_Current().get_Value() -ne 'Synthetic 36 columns'){throw 'Sheet selection did not commit'}
 Start-Sleep -Milliseconds 200;Capture 'table-36'
 ActivateApplication
 $protectedInputs=@()
 $allPasswordInputs=$script:root.FindAll([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::IsPasswordProperty,$true))
 foreach($secretElement in $allPasswordInputs){if($secretElement.Current.IsKeyboardFocusable -and !$secretElement.Current.IsOffscreen){$protectedInputs+=$secretElement}}
 if($protectedInputs.Count -lt 4){throw "Expected the open-workspace password-semantic set; observed $($protectedInputs.Count)"}
 foreach($secretElement in $protectedInputs){
  ObservePassword $secretElement @('TEST-EDIT-99!')
 }
 Invoke 'Lock';ActivateApplication;[void](Find ("State: Locked " + [char]0x2014 + " enter master password to reopen"));Capture 'locked';ActivateApplication
 $lockedMaster=WaitPassword 'Master password';ObservePassword $lockedMaster @('TEST-EDIT-99!')
 SetValue 'Master password' 'synthetic-wrong-password';Invoke 'Unlock vault';ActivateApplication
 [void](Find 'The password is incorrect or the vault is damaged.');Capture 'authentication-error';ActivateApplication
 SetValue 'Master password' 'synthetic-master-password';Invoke 'Unlock vault';ActivateApplication;[void](WaitFind 'State: Open / saved')
 Invoke 'Close vault';ActivateApplication;[void](Find 'State: Closed')
 if($script:passwordIds.Count -lt 6){throw "Expected every password role in the exercised open/locked workflow; observed $($script:passwordIds.Count)"}
 if((Get-FileHash -LiteralPath $Executable -Algorithm SHA256).Hash.ToLowerInvariant() -ne $observedExeHash){throw 'Observed executable changed during UIA smoke'}
 [ordered]@{source_sha=$SourceSha;exe_sha256=$observedExeHash;scale=$Scale;password_observations=$script:passwordResults;password_control_count=$script:passwordIds.Count;all_observed_password_controls_masked=$true;keyboard_focus_observed=$focus;profile_search_keyboard_focus_observed=$true;dynamic_profile_details_accessible=$true;native_ciphertext_picker_observed=$true;open_close_reopen_lock=$true;authentication_safe=$true;modules=@($process.Modules|ForEach-Object{$_.ModuleName}|Sort-Object -Unique);scope='Development host UIA only; no clean Windows, Narrator, clipboard contents, network trace or release claim'}|ConvertTo-Json -Depth 5
}finally{
 if(!$process.HasExited){[void]$process.CloseMainWindow();if(!$process.WaitForExit(5000)){$process.Kill()}}
 $process.Dispose()
}
