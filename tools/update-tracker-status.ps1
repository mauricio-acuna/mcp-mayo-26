param(
    [Parameter(Mandatory = $true)]
    [string]$Ids,

    [Parameter(Mandatory = $true)]
    [ValidateSet("pendiente", "enviado", "aceptado", "respondido", "agendada", "realizada", "archivado")]
    [string]$Estado,

    [string]$TrackerPath = "_local\validacion\semana-1\01-tracker-contactos.local.md",
    [string]$Fecha = (Get-Date -Format "yyyy-MM-dd"),
    [string]$ProximoToque = "",
    [switch]$DryRun
)

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not (Test-Path $TrackerPath)) {
    throw "No existe el tracker: $TrackerPath"
}

$parsedIds = $Ids -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ } | ForEach-Object { [int]$_ }

$content = Get-Content $TrackerPath
$updated = @()
$changed = 0

foreach ($line in $content) {
    if ($line -notmatch "^\|\s*\d+\s*\|") {
        $updated += $line
        continue
    }

    $cells = $line -split "\|"
    if ($cells.Count -lt 12) {
        $updated += $line
        continue
    }

    $id = [int]$cells[1].Trim()
    if ($parsedIds -notcontains $id) {
        $updated += $line
        continue
    }

    $cells[8] = " $Estado "
    if ($Estado -eq "enviado" -and -not $cells[9].Trim()) {
        $cells[9] = " $Fecha "
    }
    if ($ProximoToque) {
        $cells[11] = " $ProximoToque "
    }

    $updated += ($cells -join "|")
    $changed += 1
}

if ($DryRun) {
    Write-Output ("Dry run: se actualizarian {0} filas a estado '{1}'." -f $changed, $Estado)
    return
}

Set-Content -Path $TrackerPath -Value $updated
Write-Output ("Actualizadas {0} filas a estado '{1}'." -f $changed, $Estado)
