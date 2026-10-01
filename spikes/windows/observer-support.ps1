# Only sanitized categories are recorded. Exception messages can contain input.
function Get-ProbeObservationError($Failure) {
    $exception = $Failure.Exception
    while ($exception.InnerException) { $exception = $exception.InnerException }
    $code = $exception.HResult.ToString('X8')
    $kind = switch ($code) {
        '80040201' { 'element-unavailable'; break }
        '80070005' { 'access-denied-unverified'; break }
        default { 'unexpected-provider-error' }
    }
    return [ordered]@{ kind=$kind; hresult=$code }
}

function Read-ProbePasswordValue([scriptblock]$ReadValue) {
    try {
        $value = & $ReadValue
        if ($null -eq $value -or $value -isnot [string]) { throw 'Invalid provider response' }
        $exposed = $value -eq 'TEST-INPUT-42!' -or $value -eq 'TEST-EDIT-99!'
        $value = $null
        return [ordered]@{ status='OBSERVED'; synthetic_password_exposed=$exposed; error=$null }
    } catch {
        return [ordered]@{ status='ERROR'; synthetic_password_exposed=$null; error=(Get-ProbeObservationError $_) }
    }
}

function Get-ProbePasswordObservation([scriptblock]$ReadValue, [scriptblock]$SetValue) {
    $before = Read-ProbePasswordValue $ReadValue
    try {
        $null = & $SetValue
        $setter = [ordered]@{ status='SET'; error=$null }
    } catch {
        $setter = [ordered]@{ status='ERROR'; error=(Get-ProbeObservationError $_) }
    }
    $after = Read-ProbePasswordValue $ReadValue
    $complete = $before.status -eq 'OBSERVED' -and $setter.status -eq 'SET' -and $after.status -eq 'OBSERVED'
    $exposed = $before.synthetic_password_exposed -eq $true -or $after.synthetic_password_exposed -eq $true
    # Even access denied is not accepted as password protection without a separately
    # validated provider-specific contract. Disappearance/COM failures stay unknown.
    $security = if ($exposed) { 'FAIL' } elseif ($complete) { 'PASS' } else { 'UNKNOWN' }
    return [ordered]@{ before=$before; setter=$setter; after=$after; security_status=$security; synthetic_password_exposed=$(if ($exposed) { $true } elseif ($complete) { $false } else { $null }) }
}
