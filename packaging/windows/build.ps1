param([Parameter(Mandatory)][string]$ToolchainRoot)
$ErrorActionPreference='Stop'
$repo=(Resolve-Path "$PSScriptRoot/../..").Path
$ToolchainRoot=(Resolve-Path -LiteralPath $ToolchainRoot).Path
. "$repo/spikes/windows/environment.ps1" -ToolchainRoot $ToolchainRoot
$env:CARGO_TARGET_DIR="$ToolchainRoot/alpha-package-target"
$env:RUSTFLAGS=$null
$env:CARGO_ENCODED_RUSTFLAGS=@('-C','link-self-contained=yes',"--remap-path-prefix=$repo=/tessaveil",("--remap-path-prefix="+$repo.Replace('\','/')+'=/tessaveil'),"--remap-path-prefix=$ToolchainRoot=/toolchain",("--remap-path-prefix="+$ToolchainRoot.Replace('\','/')+'=/toolchain')) -join [char]31
$env:RUSTDOCFLAGS='-C link-self-contained=yes'
Push-Location $repo
try{
 cargo build --release --locked -p tessaveil-windows-controller
 if($LASTEXITCODE){throw 'Release Rust build failed'}
 cmake -S apps/tessaveil-windows -B "$ToolchainRoot/build/alpha-package" -G Ninja -DCMAKE_BUILD_TYPE=Release "-DCMAKE_PREFIX_PATH=$ToolchainRoot/qt-6.8.3-static" -DCMAKE_CXX_COMPILER=clang++ "-DCONTROLLER_LIBRARY=$ToolchainRoot/alpha-package-target/release/libtessaveil_windows_controller.a" "-DCMAKE_CXX_FLAGS=-ffile-prefix-map=`"$repo`"=/tessaveil" "-DALPHA_LINK_MAP=$ToolchainRoot/build/alpha-package/Tessaveil.map"
 if($LASTEXITCODE){throw 'Application configure failed'}
 cmake --build "$ToolchainRoot/build/alpha-package" --parallel 4
 if($LASTEXITCODE){throw 'Application build failed'}
 & "$ToolchainRoot/build/alpha-package/alpha_ui_tests.exe"
 if($LASTEXITCODE){throw 'Native headful synthetic E2E failed'}
 python "$PSScriptRoot/build_receipt.py" --toolchain-root $ToolchainRoot
 if($LASTEXITCODE){throw 'Build receipt failed'}
}finally{Pop-Location}
