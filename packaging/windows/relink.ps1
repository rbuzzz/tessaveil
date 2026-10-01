param(
 [Parameter(Mandatory)][string]$Bundle,
 [Parameter(Mandatory)][string]$ToolchainRoot,
 [Parameter(Mandatory)][string]$WorkRoot,
 [switch]$MarkerExercise
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$bundlePath=(Resolve-Path -LiteralPath $Bundle).Path
if(Test-Path -LiteralPath $WorkRoot){throw 'Relink work directory must be new'}
if($WorkRoot -match '[^\x00-\x7F]'){throw 'Relink work directory must be ASCII'}
$archive=Join-Path $bundlePath 'qtbase-6.8.3.zip'
if((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLower() -ne '992bf7766e214a341ef793eb3665fb784787d2fd666955f5f507f4c6f1f770dd'){throw 'Qt source hash mismatch'}
New-Item -ItemType Directory -Path $WorkRoot | Out-Null
$work=(Resolve-Path -LiteralPath $WorkRoot).Path
$env:PATH="$ToolchainRoot/llvm-mingw-20250709-ucrt-x86_64/bin;$ToolchainRoot/cmake-3.31.8-windows-x86_64/bin;$ToolchainRoot/ninja-1.12.1;$env:PATH"
Expand-Archive -LiteralPath $archive -DestinationPath $work
$source=Join-Path $work 'qtbase-everywhere-src-6.8.3'
if($MarkerExercise){
 $file=Join-Path $source 'src/corelib/global/qlibraryinfo.cpp'
 $body=[IO.File]::ReadAllText($file)
 if(([regex]::Matches($body,'return QT_VERSION_STR;')).Count -ne 1){throw 'Marker site changed'}
 [IO.File]::WriteAllText($file,$body.Replace('return QT_VERSION_STR;','return "6.8.3-tessaveil-relink-test"; // Modified by Tessaveil, 2026-09-30, synthetic relink exercise'),[Text.UTF8Encoding]::new($false))
 # qVersion alone is dead-stripped from the real application. Reference it from
 # the actual QApplication constructor so the modified library is exercised.
 $widgetFile=Join-Path $source 'src/widgets/kernel/qapplication.cpp'
 $widgetBody=[IO.File]::ReadAllText($widgetFile)
 $site='    : QGuiApplication(*new QApplicationPrivate(argc, argv))'
 if(([regex]::Matches($widgetBody,[regex]::Escape($site))).Count -ne 1){throw 'Application marker site changed'}
 $widgetBody=[regex]::Replace($widgetBody,([regex]::Escape($site)+'\r?\n\{'),"$site`n{`n    qInfo(`"%s`", qVersion()); // Modified by Tessaveil, 2026-09-30, synthetic relink exercise")
 if(!$widgetBody.Contains('qInfo("%s", qVersion());')){throw 'Application marker insertion failed'}
 [IO.File]::WriteAllText($widgetFile,$widgetBody,[Text.UTF8Encoding]::new($false))
}
$options=Get-Content -Raw (Join-Path $bundlePath 'qt-options.json') | ConvertFrom-Json
$prefix=Join-Path $work 'qt'
cmake -S $source -B "$work/qt-build" @options "-DCMAKE_INSTALL_PREFIX=$prefix"
if($LASTEXITCODE){throw 'Qt relink configure failed'}
cmake --build "$work/qt-build" --parallel 4
if($LASTEXITCODE){throw 'Qt relink build failed'}
cmake --install "$work/qt-build"
if($LASTEXITCODE){throw 'Qt relink install failed'}
cmake -S "$bundlePath/relink" -B "$work/app" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++ "-DCMAKE_PREFIX_PATH=$prefix"
if($LASTEXITCODE){throw 'Application relink configure failed'}
cmake --build "$work/app" --parallel 4
if($LASTEXITCODE){throw 'Application relink failed'}
if($MarkerExercise){
 & "$work/app/qt_marker.exe"
 if($LASTEXITCODE){throw 'Modified Qt was not observed'}
}
Write-Output 'Relink built from bundled application objects and bundled Qt source. Smoke/audit still required.'
