param([Parameter(Mandatory)][string]$ToolchainRoot,[switch]$Test)
$ErrorActionPreference='Stop'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
. (Join-Path $repo 'spikes/windows/environment.ps1') -ToolchainRoot $ToolchainRoot
$env:CARGO_TARGET_DIR=Join-Path $ToolchainRoot 'alpha-target'
$env:RUSTDOCFLAGS='-C link-self-contained=yes'
Push-Location $repo
try {
 cargo build --release --locked -p tessaveil-windows-controller
 if($LASTEXITCODE){throw 'Rust build failed'}
 $build=Join-Path $ToolchainRoot 'build/windows-alpha'
 $lib=Join-Path $env:CARGO_TARGET_DIR 'release/libtessaveil_windows_controller.a'
 cmake -S $PSScriptRoot -B $build -G Ninja -DCMAKE_BUILD_TYPE=Release "-DCMAKE_PREFIX_PATH=$ToolchainRoot/qt-6.8.3-static" -DCMAKE_CXX_COMPILER=clang++ "-DCONTROLLER_LIBRARY=$lib"
 if($LASTEXITCODE){throw 'CMake configure failed'}
 cmake --build $build --parallel 4
 if($LASTEXITCODE){throw 'Native build failed'}
 if($Test){ & (Join-Path $build 'alpha_ui_tests.exe');if($LASTEXITCODE){throw 'Native tests failed'} }
}finally{Pop-Location}
