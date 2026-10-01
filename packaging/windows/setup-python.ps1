param([Parameter(Mandatory)][string]$ToolchainRoot)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
if(Test-Path -LiteralPath "$ToolchainRoot/python"){throw 'Python destination must be new'}
$pins=Get-Content -Raw "$PSScriptRoot/toolchains.json" | ConvertFrom-Json
foreach($pin in $pins.downloads | Where-Object { $_.file -match '^(python-|pip-)' }){
 $destination=Join-Path "$ToolchainRoot/downloads" $pin.file
 if(!(Test-Path -LiteralPath $destination)){Invoke-WebRequest -Uri $pin.url -OutFile $destination}
 if((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLower() -ne $pin.sha256){throw 'Python archive hash mismatch'}
}
Expand-Archive -LiteralPath "$ToolchainRoot/downloads/python-3.12.10-embed-amd64.zip" -DestinationPath "$ToolchainRoot/python"
$repo=(Resolve-Path "$PSScriptRoot/../..").Path
[IO.File]::WriteAllLines("$ToolchainRoot/python/python312._pth",@('python312.zip','.','Lib/site-packages',$repo,"$repo/packaging/windows",'import site'))
New-Item -ItemType Directory -Path "$ToolchainRoot/python/Lib/site-packages" -Force | Out-Null
[IO.Compression.ZipFile]::ExtractToDirectory("$ToolchainRoot/downloads/pip-25.0.1-py3-none-any.whl","$ToolchainRoot/python/Lib/site-packages")
& "$ToolchainRoot/python/python.exe" -m pip install --disable-pip-version-check --only-binary=:all: --require-hashes -r "$PSScriptRoot/requirements.lock"
if($LASTEXITCODE){throw 'Locked Python dependencies failed'}
