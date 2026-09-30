# Invoke the observer's real AST statements without launching a GUI process.
param([ValidateSet('ReadFailure', 'Snapshot')][string]$Case, [string]$FixtureRoot,
      [ValidateSet('Unexpected', 'AccessDenied', 'ElementUnavailable', 'FirstRead', 'Setter')][string]$FaultKind='Unexpected')
$ErrorActionPreference = 'Stop'
$repo = Split-Path (Split-Path $PSScriptRoot)
$support = Join-Path $repo 'spikes/windows/observer-support.ps1'
if (Test-Path $support) { . $support }
function Get-ObserverAst([string]$Name) {
    $tokens=$null; $errors=$null
    $ast = [Management.Automation.Language.Parser]::ParseFile((Join-Path $repo "spikes/windows/$Name"), [ref]$tokens, [ref]$errors)
    if ($errors.Count) { throw 'Observer syntax error' }
    return $ast
}
if ($Case -eq 'Snapshot') {
    $ast = Get-ObserverAst 'measure.ps1'
    $temp = (Get-Item -LiteralPath $FixtureRoot).FullName
    foreach ($variable in @('$before', '$after')) {
        $statement = $ast.Find({ param($n) $n -is [Management.Automation.Language.AssignmentStatementAst] -and $n.Left.Extent.Text -eq $variable }, $true)
        . ([scriptblock]::Create($statement.Extent.Text))
    }
    [ordered]@{ before=@($before); after=@($after) } | ConvertTo-Json -Compress
    exit
}
Add-Type -AssemblyName UIAutomationClient
Add-Type @'
public class FaultingPattern {
 public int Reads;
 public string Fault;
 public FaultingPattern Current { get { return this; } }
 public string Value { get {
  ++Reads;
  if (Reads == 1 && Fault == "FirstRead") throw new System.IO.IOException("synthetic first read failure");
  if (Reads == 2) {
   if (Fault == "AccessDenied") throw new System.Runtime.InteropServices.COMException("synthetic denial", unchecked((int)0x80070005));
   if (Fault == "ElementUnavailable") throw new System.Runtime.InteropServices.COMException("synthetic disappearance", unchecked((int)0x80040201));
   if (Fault == "Unexpected") throw new System.IO.IOException("synthetic read failure");
  }
  return "";
 } }
 public void SetValue(string value) { if (Fault == "Setter") throw new System.IO.IOException("synthetic setter failure"); }
}
public class SyntheticNode {
 public FaultingPattern Pattern = new FaultingPattern();
 public object GetCurrentPattern(object id) { return Pattern; }
}
'@
$node = New-Object SyntheticNode
$node.Pattern.Fault = $FaultKind
$c = [pscustomobject]@{ IsPassword=$true; ControlType=[pscustomobject]@{ProgrammaticName='ControlType.Edit'}; Name='Test input'; IsKeyboardFocusable=$true; IsOffscreen=$false }
$passwordCount=0; $inputSetSucceeded=$false; $exposed=$false; $controls=@()
$ValidatePassword=$true; $invoked=$true; $core=$true
$ast = Get-ObserverAst 'inspect-ui.ps1'
$password = $ast.Find({ param($n) $n -is [Management.Automation.Language.IfStatementAst] -and $n.Clauses[0].Item1.Extent.Text -eq '$c.IsPassword' }, $true)
$record = $ast.Find({ param($n) $n -is [Management.Automation.Language.AssignmentStatementAst] -and $n.Left.Extent.Text -eq '$controls' -and $n.Operator -eq 'PlusEquals' }, $true)
$gate = $ast.Find({ param($n) $n -is [Management.Automation.Language.IfStatementAst] -and $n.Clauses[0].Item1.Extent.Text.StartsWith('$ValidatePassword -and') }, $true)
if (!$password -or !$record -or !$gate) { throw 'Observer behavior entry point missing' }
. ([scriptblock]::Create($password.Extent.Text))
. ([scriptblock]::Create($record.Extent.Text))
$passed=$true
try { . ([scriptblock]::Create($gate.Extent.Text)) } catch { $passed=$false }
[ordered]@{ gate_passed=$passed; reads=$node.Pattern.Reads; input_set_succeeded=$inputSetSucceeded; controls=$controls } | ConvertTo-Json -Depth 10 -Compress
