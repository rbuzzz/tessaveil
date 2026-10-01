param([Parameter(Mandatory)][string]$ToolchainRoot)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
if(Test-Path -LiteralPath $ToolchainRoot){throw 'Bootstrap requires a NEW external directory'}
if($ToolchainRoot -match '[^\x00-\x7F]'){throw 'Use an ASCII toolchain directory'}
New-Item -ItemType Directory -Path "$ToolchainRoot/downloads" -Force | Out-Null
$pins=Get-Content -Raw "$PSScriptRoot/toolchains.json" | ConvertFrom-Json
foreach($pin in $pins.downloads){
 $destination=Join-Path "$ToolchainRoot/downloads" $pin.file
 Invoke-WebRequest -Uri $pin.url -OutFile $destination
 if((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLower() -ne $pin.sha256){throw "Pinned archive mismatch: $($pin.file)"}
}
foreach($item in @(@('llvm-mingw-20250709.zip',''),@('cmake-3.31.8.zip',''),@('ninja-1.12.1.zip','ninja-1.12.1'),@('qtbase-6.8.3.zip',''))){
 Expand-Archive -LiteralPath "$ToolchainRoot/downloads/$($item[0])" -DestinationPath "$ToolchainRoot/$($item[1])"
}
$repo=(Resolve-Path "$PSScriptRoot/../..").Path
& "$PSScriptRoot/setup-python.ps1" -ToolchainRoot $ToolchainRoot
$env:PATH="$ToolchainRoot/python;$ToolchainRoot/python/Scripts;$env:PATH"
$env:RUSTUP_HOME="$ToolchainRoot/rustup"
$env:CARGO_HOME="$ToolchainRoot/cargo"
& "$ToolchainRoot/downloads/rustup-init.exe" -y --no-modify-path --profile minimal --default-host x86_64-pc-windows-gnu --default-toolchain 1.90.0
if($LASTEXITCODE){throw 'Pinned Rust installation failed'}
& "$ToolchainRoot/cargo/bin/rustup.exe" component add rustfmt clippy rust-src --toolchain $pins.rust
if($LASTEXITCODE){throw 'Pinned Rust components failed'}
python "$PSScriptRoot/verify-rust-manifest.py" "$ToolchainRoot/downloads/channel-rust-1.90.0.toml" "$ToolchainRoot/rustup/toolchains/$($pins.rust)/lib/rustlib/multirust-channel-manifest.toml"
if($LASTEXITCODE){throw 'Installed Rust manifest differs from pinned archive hashes'}
python "$PSScriptRoot/runtime_material.py" --toolchain-root $ToolchainRoot --fetch
if($LASTEXITCODE){throw 'Pinned runtime source/notice material unavailable'}
. "$repo/spikes/windows/environment.ps1" -ToolchainRoot $ToolchainRoot
$options=Get-Content -Raw "$PSScriptRoot/qt-options.json" | ConvertFrom-Json
cmake -S "$ToolchainRoot/qtbase-everywhere-src-6.8.3" -B "$ToolchainRoot/build/qt-static" @options "-DCMAKE_INSTALL_PREFIX=$ToolchainRoot/qt-6.8.3-static"
if($LASTEXITCODE){throw 'Qt configure failed'}
cmake --build "$ToolchainRoot/build/qt-static" --parallel 4
if($LASTEXITCODE){throw 'Qt build failed'}
cmake --install "$ToolchainRoot/build/qt-static"
if($LASTEXITCODE){throw 'Qt install failed'}
