#requires -Version 7.4
[CmdletBinding()]
param(
    [string] $Root,
    [ValidateSet('AfterCreate','AfterWrite','AfterFlush','AfterVerify','BeforeReplace','AfterReplace','None')]
    [string] $FailurePhase = 'None'
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:ProbeDirectory = $PSScriptRoot

# The native calls below only inspect/pin paths. No disk, volume, mount or format API.
if (-not ('TessaveilFsProbe.Paths' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Text;
using System.ComponentModel;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
namespace TessaveilFsProbe {
    public static class Paths {
        [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
        static extern SafeFileHandle CreateFileW(string p, uint a, uint s, IntPtr sa, uint c, uint f, IntPtr t);
        [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
        static extern uint GetFinalPathNameByHandleW(SafeFileHandle h, StringBuilder s, uint n, uint flags);
        [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
        static extern uint QueryDosDeviceW(string name, StringBuilder target, int max);
        [DllImport("cldapi.dll", CharSet=CharSet.Unicode)]
        static extern int CfGetSyncRootInfoByPath(string p, int c, byte[] buffer, uint size, out uint length);
        [StructLayout(LayoutKind.Sequential)]
        struct Info {
            public uint Attributes;
            public System.Runtime.InteropServices.ComTypes.FILETIME Creation, Access, Write;
            public uint Volume, SizeHigh, SizeLow, Links, IndexHigh, IndexLow;
        }
        [DllImport("kernel32.dll", SetLastError=true)]
        static extern bool GetFileInformationByHandle(SafeFileHandle h, out Info i);

        public static SafeFileHandle Pin(string path, bool directory) {
            // READ_ATTRIBUTES, share READ only, OPEN_EXISTING, OPEN_REPARSE_POINT + BACKUP_SEMANTICS.
            var h = CreateFileW(path, 0x80, 1, IntPtr.Zero, 3, 0x02200000, IntPtr.Zero);
            if (h.IsInvalid) { h.Dispose(); throw new Win32Exception(Marshal.GetLastWin32Error()); }
            try {
                Info i;
                if (!GetFileInformationByHandle(h, out i)) throw new Win32Exception(Marshal.GetLastWin32Error());
                // Reject reparse, offline and recall-on-open/data-access attributes.
                if ((i.Attributes & (0x400u | 0x1000u | 0x40000u | 0x400000u)) != 0)
                    throw new IOException("Reparse/offline/cloud attribute refused");
                if (((i.Attributes & 0x10) != 0) != directory || (!directory && i.Links != 1))
                    throw new IOException("Wrong path kind or multiply linked file");
                var b = new StringBuilder(1024);
                uint n = GetFinalPathNameByHandleW(h, b, 1024, 0);
                if (n == 0 || n >= 1024) throw new IOException("Cannot resolve exact path");
                string actual = b.ToString();
                if (!actual.StartsWith(@"\\?\", StringComparison.Ordinal)) throw new IOException("Nonlocal path");
                actual = actual.Substring(4).TrimEnd('\\');
                if (!String.Equals(actual, Path.GetFullPath(path).TrimEnd('\\'), StringComparison.OrdinalIgnoreCase))
                    throw new IOException("Resolved path differs from authorized path");
                return h;
            } catch { h.Dispose(); throw; }
        }
        public static void RequireLocalDrive(string drive) {
            var b = new StringBuilder(1024);
            if (QueryDosDeviceW(drive.TrimEnd('\\'), b, 1024) == 0 ||
                !b.ToString().StartsWith(@"\Device\HarddiskVolume", StringComparison.Ordinal))
                throw new IOException("Mapped, substituted or unknown drive refused");
            var d = new DriveInfo(drive);
            if (d.DriveType != DriveType.Fixed || d.DriveFormat != "NTFS")
                throw new IOException("Only the local fixed NTFS research target is authorized");
        }
        public static void RequireNotCloud(string path) {
            uint length;
            int hr = CfGetSyncRootInfoByPath(path, 0, new byte[1024], 1024, out length);
            // Only ERROR_CLOUD_FILE_NOT_UNDER_SYNC_ROOT clears this gate.
            if (hr != unchecked((int)0x80070186))
                throw new IOException("Cloud/unknown sync-root status refused: " + hr.ToString("X8"));
        }
    }
}
'@
}

function Get-ProbePublicDirectory {
    if (-not $IsWindows) { throw 'Windows is required' }
    $common = [Environment]::GetFolderPath('CommonDocuments')
    $public = [IO.Path]::GetDirectoryName($common)
    $drive = [IO.Path]::GetPathRoot([Environment]::SystemDirectory)
    if ($public -cne (Join-Path $drive 'Users\Public')) { throw 'Redirected Public directory refused' }
    return $public
}

function Open-ProbeRoot {
    param([Parameter(Mandatory)][string] $Path, [switch] $RequireEmpty)
    $public = Get-ProbePublicDirectory
    # Deliberately narrower than arbitrary caller paths: direct GUID child only.
    if ($Path -cnotmatch ('^' + [regex]::Escape($public) + '\\TessaveilReplaceProbe-[0-9a-f]{32}$')) {
        throw 'Only an explicit dedicated Public GUID test directory is authorized'
    }
    if ([IO.Path]::GetFullPath($Path) -cne $Path) { throw 'Noncanonical root refused' }
    foreach ($forbidden in @([Environment]::GetFolderPath('UserProfile'), $HOME,
        (Get-Location).Path, [IO.Path]::GetFullPath((Join-Path $script:ProbeDirectory '..\..')))) {
        if ($forbidden -and ($Path -ieq $forbidden -or $Path.StartsWith($forbidden.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase))) {
            throw 'Workspace/profile target refused'
        }
    }
    [TessaveilFsProbe.Paths]::RequireLocalDrive([IO.Path]::GetPathRoot($Path))
    $pins = [Collections.Generic.List[IDisposable]]::new()
    try {
        $ancestors = [Collections.Generic.List[string]]::new()
        $cursor = $Path
        while ($cursor) {
            $ancestors.Insert(0, $cursor)
            $cursor = [IO.Path]::GetDirectoryName($cursor)
        }
        foreach ($ancestor in $ancestors) {
            $pins.Add([TessaveilFsProbe.Paths]::Pin($ancestor, $true))
        }
        [TessaveilFsProbe.Paths]::RequireNotCloud($Path)
        if ($RequireEmpty -and [IO.Directory]::EnumerateFileSystemEntries($Path).GetEnumerator().MoveNext()) {
            throw 'Nonempty directory refused'
        }
        return ,$pins
    } catch {
        foreach ($pin in $pins) { $pin.Dispose() }
        throw
    }
}

function Assert-ProbeFile {
    param([string] $TestRoot, [string] $Path, [switch] $MustExist)
    if ([IO.Path]::GetDirectoryName($Path) -cne $TestRoot -or
        [IO.Path]::GetFileName($Path) -cnotin @('vault.tessaveil','update.tmp.tessaveil','sentinel.bin')) {
        throw 'File outside exact probe allowlist'
    }
    if ([IO.Path]::GetFullPath($Path) -cne $Path) { throw 'Noncanonical file refused' }
    if ($MustExist) {
        $pin = [TessaveilFsProbe.Paths]::Pin($Path, $false)
        $pin.Dispose()
    } elseif ([IO.File]::Exists($Path) -or [IO.Directory]::Exists($Path)) {
        throw 'Existing path refused'
    }
}

function Get-ProbeKey {
    # Public synthetic fixture key, never a credential or a password/KDF proposal.
    return ,[Security.Cryptography.SHA256]::HashData(
        [Text.Encoding]::UTF8.GetBytes('Tessaveil filesystem probe public synthetic key v1'))
}

function New-ProbeImage {
    $header = [byte[]]::new(28)
    [Text.Encoding]::ASCII.GetBytes('TVFS0001').CopyTo($header, 0)
    $header[10] = 1 # AES-256-GCM; KDF id 0 = synthetic public key, no KDF.
    [BitConverter]::GetBytes([uint32]4096).CopyTo($header, 12)
    $nonce = [Security.Cryptography.RandomNumberGenerator]::GetBytes(12)
    $nonce.CopyTo($header, 16)
    $plain = [Security.Cryptography.RandomNumberGenerator]::GetBytes(4096)
    $cipher = [byte[]]::new(4096)
    $tag = [byte[]]::new(16)
    $aes = [Security.Cryptography.AesGcm]::new((Get-ProbeKey), 16)
    try { $aes.Encrypt($nonce, $plain, $cipher, $tag, $header) }
    finally { [Array]::Clear($plain); $aes.Dispose() }
    return ,[byte[]]($header + $cipher + $tag)
}

function Test-ProbeImage {
    param([byte[]] $Image)
    if ($null -eq $Image -or $Image.Length -ne 4140) { return $false }
    if ([Text.Encoding]::ASCII.GetString($Image, 0, 8) -cne 'TVFS0001' -or
        $Image[8] -ne 0 -or $Image[9] -ne 0 -or $Image[10] -ne 1 -or $Image[11] -ne 0 -or
        [BitConverter]::ToUInt32($Image, 12) -ne 4096) { return $false }
    $plain = [byte[]]::new(4096)
    $aes = [Security.Cryptography.AesGcm]::new((Get-ProbeKey), 16)
    try {
        $aes.Decrypt([byte[]]$Image[16..27], [byte[]]$Image[28..4123], [byte[]]$Image[4124..4139], $plain, [byte[]]$Image[0..27])
        return $true
    } catch [Security.Cryptography.CryptographicException] { return $false }
    finally { [Array]::Clear($plain); $aes.Dispose() }
}

function Invoke-ReplaceProbe {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string] $Root,
        [ValidateSet('AfterCreate','AfterWrite','AfterFlush','AfterVerify','BeforeReplace','AfterReplace','None')]
        [string] $FailurePhase = 'None'
    )
    # This intentionally terminates its process. Always invoke in a dedicated pwsh child.
    $pins = Open-ProbeRoot -Path $Root -RequireEmpty
    $stream = $null
    try {
        $target = Join-Path $Root 'vault.tessaveil'
        $temporary = Join-Path $Root 'update.tmp.tessaveil'
        $fixture = Join-Path $script:ProbeDirectory 'fixtures\header-and-ciphertext.bin'
        if ((Get-Item -LiteralPath $fixture).Length -ne 4140) { throw 'Unbounded fixture refused' }
        $old = [IO.File]::ReadAllBytes($fixture)
        $new = New-ProbeImage
        if (!(Test-ProbeImage $old) -or !(Test-ProbeImage $new)) { throw 'Unauthenticated input refused' }
        Assert-ProbeFile $Root $target
        $stream = [IO.FileStream]::new($target, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        $stream.Write($old, 0, $old.Length)
        $stream.Flush($true)
        $stream.Dispose(); $stream = $null
        Assert-ProbeFile $Root $target -MustExist
        if (!(Test-ProbeImage ([IO.File]::ReadAllBytes($target)))) { throw 'Baseline verification failed' }
        @{
            old_sha256 = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($old)).ToLowerInvariant()
            new_sha256 = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($new)).ToLowerInvariant()
        } | ConvertTo-Json -Compress
        Assert-ProbeFile $Root $temporary
        $stream = [IO.FileStream]::new($temporary, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None, 8192)
        if ($FailurePhase -eq 'AfterCreate') { [Environment]::Exit(86) }
        $stream.Write($new, 0, $new.Length)
        if ($FailurePhase -eq 'AfterWrite') { [Environment]::Exit(86) }
        $stream.Flush($true)
        if ($FailurePhase -eq 'AfterFlush') { [Environment]::Exit(86) }
        $stream.Dispose(); $stream = $null
        Assert-ProbeFile $Root $temporary -MustExist
        if (!(Test-ProbeImage ([IO.File]::ReadAllBytes($temporary)))) { throw 'Reopened image rejected' }
        if ($FailurePhase -eq 'AfterVerify') { [Environment]::Exit(86) }
        # Both exact resolved paths belong to the still-pinned authorized test root.
        Assert-ProbeFile $Root $target -MustExist
        Assert-ProbeFile $Root $temporary -MustExist
        if ($FailurePhase -eq 'BeforeReplace') { [Environment]::Exit(86) }
        [IO.File]::Replace($temporary, $target, [System.Management.Automation.Language.NullString]::Value, $false)
        if ($FailurePhase -eq 'AfterReplace') { [Environment]::Exit(86) }
        Assert-ProbeFile $Root $target -MustExist
        if (!(Test-ProbeImage ([IO.File]::ReadAllBytes($target)))) { throw 'Result authentication failed' }
    } finally {
        if ($null -ne $stream) { $stream.Dispose() }
        foreach ($pin in $pins) { $pin.Dispose() }
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    if (-not $Root) { throw 'Caller-supplied empty Root is required' }
    Invoke-ReplaceProbe -Root $Root -FailurePhase $FailurePhase
}
