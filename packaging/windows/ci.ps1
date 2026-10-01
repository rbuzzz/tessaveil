param([Parameter(Mandatory)][string]$ToolchainRoot,[Parameter(Mandatory)][string]$SourceSha)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$repo=(Resolve-Path "$PSScriptRoot/../..").Path
. "$repo/spikes/windows/environment.ps1" -ToolchainRoot $ToolchainRoot
$env:PATH="$ToolchainRoot/python;$ToolchainRoot/python/Scripts;$env:PATH"
$env:CARGO_TARGET_DIR="$ToolchainRoot/alpha-package-target"
$env:RUSTDOCFLAGS='-C link-self-contained=yes'
Push-Location $repo
try{
 if((git rev-parse HEAD).Trim() -ne $SourceSha -or (git status --porcelain)){throw 'Exact clean checkout required'}
 # SBOM metadata includes all locked platforms, not only the Windows build graph.
 cargo fetch --locked
 if($LASTEXITCODE){throw 'Complete locked Cargo fetch failed'}
 cargo fmt --check
 if($LASTEXITCODE){throw 'Rust format failed'}
 cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
 if($LASTEXITCODE){throw 'Rust clippy failed'}
 cargo test --workspace --all-targets --locked
 if($LASTEXITCODE){throw 'Rust workspace tests failed'}
 cargo test --workspace --doc --locked
 if($LASTEXITCODE){throw 'Rust doctests failed'}
 python tools/run_tests.py
 if($LASTEXITCODE){throw 'Full discovered Python suite failed'}
 python -m check_jsonschema --builtin-schema vendor.github-workflows .github/workflows/windows-alpha.yml
 if($LASTEXITCODE){throw 'Windows workflow schema invalid'}
 python tools/alpha_catalog.py --check
 if($LASTEXITCODE){throw 'Alpha generator drift'}
 python -m tools.catalog.cli generate --root . --check
 if($LASTEXITCODE){throw 'Catalog generator drift'}
 python -m tools.notices --check
 if($LASTEXITCODE){throw 'Notices drift'}
 python -m tools.sensitive_material
 if($LASTEXITCODE){throw 'Sensitive material gate failed'}
 python -m tools.history_sensitive_material --root .
 if($LASTEXITCODE){throw 'History gate failed'}
 & "$PSScriptRoot/build.ps1" -ToolchainRoot $ToolchainRoot
 & "$PSScriptRoot/gate.ps1" -ToolchainRoot $ToolchainRoot -SourceSha $SourceSha -OutputRoot "$ToolchainRoot/alpha-output"
}finally{Pop-Location}
