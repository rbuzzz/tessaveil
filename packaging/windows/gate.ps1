param(
 [Parameter(Mandatory)][string]$ToolchainRoot,
 [Parameter(Mandatory)][string]$SourceSha,
 [Parameter(Mandatory)][string]$OutputRoot
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$repo=(Resolve-Path "$PSScriptRoot/../..").Path
. "$repo/spikes/windows/environment.ps1" -ToolchainRoot $ToolchainRoot
if(Test-Path "$ToolchainRoot/python/python.exe"){$env:PATH="$ToolchainRoot/python;$ToolchainRoot/python/Scripts;$env:PATH"}
$env:CARGO_TARGET_DIR="$ToolchainRoot/alpha-package-target"
Push-Location $repo
try{
 if((git rev-parse HEAD).Trim() -ne $SourceSha -or (git status --porcelain)){throw 'Exact clean checkout required'}
 if(Test-Path -LiteralPath $OutputRoot){throw 'Output directory must be new'}
 $scratch=Join-Path $ToolchainRoot ('tmp/alpha-gate-'+[Guid]::NewGuid().ToString('N'))
 New-Item -ItemType Directory -Path $scratch | Out-Null
 $fixture=Join-Path $scratch 'observation.tessaveil-alpha'
 try{
  cargo run --locked -p tessaveil-windows-controller --example synthetic_fixture -- $fixture
  if($LASTEXITCODE){throw 'Synthetic fixture creation failed'}
  $observation=& powershell -NoProfile -File "$repo/apps/tessaveil-windows/tests/observe.ps1" -Executable "$ToolchainRoot/build/alpha-package/Tessaveil.exe" -Fixture $fixture -ScreenshotRoot "$scratch/captures" -SourceSha $SourceSha
  if($LASTEXITCODE){throw 'Live headful smoke unavailable or failed; no upload permitted'}
  [IO.File]::WriteAllText("$scratch/observation.json",($observation -join "`n"),[Text.UTF8Encoding]::new($false))
  python "$PSScriptRoot/prepare.py" --toolchain-root $ToolchainRoot --build "$ToolchainRoot/build/alpha-package" --rust-library "$ToolchainRoot/alpha-package-target/release/libtessaveil_windows_controller.a" --output $OutputRoot --observation "$scratch/observation.json" --source-sha $SourceSha --analysis-only
  if($LASTEXITCODE){throw 'Local compliance staging failed'}
  & "$PSScriptRoot/relink.ps1" -Bundle "$OutputRoot/compliance" -ToolchainRoot $ToolchainRoot -WorkRoot "$scratch/relink" -MarkerExercise
  $original=(Get-FileHash -LiteralPath "$OutputRoot/runtime/Tessaveil.exe" -Algorithm SHA256).Hash
  $modified=(Get-FileHash -LiteralPath "$scratch/relink/app/Tessaveil.exe" -Algorithm SHA256).Hash
  if($original -eq $modified){throw 'Same-input relink is not a modified Qt exercise'}
  python -c "from pathlib import Path; import sys; assert b'6.8.3-tessaveil-relink-test' in Path(sys.argv[1]).read_bytes()" "$scratch/relink/app/Tessaveil.exe"
  if($LASTEXITCODE){throw 'Modified Qt marker missing from relinked application'}
  $relinkObservation=& powershell -NoProfile -File "$repo/apps/tessaveil-windows/tests/observe.ps1" -Executable "$scratch/relink/app/Tessaveil.exe" -Fixture $fixture -ScreenshotRoot "$scratch/relink-captures" -SourceSha $SourceSha
  if($LASTEXITCODE){throw 'Relinked application synthetic smoke failed'}
  [IO.File]::WriteAllText("$scratch/relink-observation.json",($relinkObservation -join "`n"),[Text.UTF8Encoding]::new($false))
  python "$PSScriptRoot/finish.py" --output $OutputRoot --relink "$scratch/relink" --smoke "$scratch/relink-observation.json" --source-sha $SourceSha
  if($LASTEXITCODE){throw 'Distribution BLOCKED: independent finalization failed; no upload permitted'}
  if(!(Test-Path -LiteralPath "$OutputRoot/GATE-PASS.json")){throw 'Final gate receipt missing'}
 }finally{
  # Only explicit task-created synthetic fixture/capture paths are removed.
  if(Test-Path -LiteralPath $fixture){Remove-Item -LiteralPath $fixture}
  foreach($captureName in @('captures','relink-captures')){
   $capture=Join-Path $scratch $captureName
   if(Test-Path -LiteralPath $capture){
    $resolved=(Resolve-Path -LiteralPath $capture).Path
    if(!$resolved.StartsWith((Resolve-Path -LiteralPath $scratch).Path+[IO.Path]::DirectorySeparatorChar)){throw 'Unsafe cleanup target'}
    Remove-Item -LiteralPath $resolved -Recurse -Force
   }
  }
 }
}finally{Pop-Location}
