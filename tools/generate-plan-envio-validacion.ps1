param(
    [string]$TrackerPath = "_local\validacion\semana-1\01-tracker-contactos.local.md",
    [string]$OutputPath = "_local\validacion\semana-1\plan-envio.local.md",
    [int]$BatchSize = 10
)

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Get-TrackerRows {
    param([string[]]$Content)

    $rows = @()
    foreach ($line in $Content) {
        if ($line -notmatch "^\|\s*\d+\s*\|") {
            continue
        }

        $cells = $line -split "\|"
        if ($cells.Count -lt 12) {
            continue
        }

        $rows += [PSCustomObject]@{
            Numero = [int]$cells[1].Trim()
            Nombre = $cells[2].Trim()
            Empresa = $cells[3].Trim()
            Rol = $cells[4].Trim()
            Perfil = $cells[5].Trim()
            Hueco = $cells[6].Trim()
            Canal = $cells[7].Trim()
            Estado = $cells[8].Trim()
            FechaEnvio = $cells[9].Trim()
            Respuesta = $cells[10].Trim()
            ProximoToque = $cells[11].Trim()
        }
    }

    return $rows
}

if (-not (Test-Path $TrackerPath)) {
    throw "No existe el tracker: $TrackerPath"
}

$rows = Get-TrackerRows (Get-Content $TrackerPath)
$ready = $rows | Where-Object {
    $_.Nombre -and $_.Empresa -and $_.Rol -and $_.Perfil -and $_.Hueco -and $_.Estado -eq "pendiente"
} | Sort-Object Numero

$lines = @()
$lines += "# Plan de envio - Semana 1"
$lines += ""
$lines += "> Archivo local. Usar despues de revisar `mensajes-generados.local.md`."
$lines += ""
$lines += ("Generado: {0}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"))
$lines += ("Contactos pendientes listos: {0}" -f (($ready | Measure-Object).Count))
$lines += ""
$lines += "## Regla"
$lines += ""
$lines += "- Enviar en bloques de 10."
$lines += "- Descansar 5-10 min entre bloques."
$lines += "- Si un mensaje parece generico, corregir o saltar."
$lines += "- Tras cada bloque, marcar estado como `enviado`."
$lines += ""

$batchNumber = 1
for ($i = 0; $i -lt $ready.Count; $i += $BatchSize) {
    $batch = $ready | Select-Object -Skip $i -First $BatchSize
    $ids = ($batch | ForEach-Object { $_.Numero }) -join ","

    $lines += ("## Lote {0}" -f $batchNumber)
    $lines += ""
    $lines += ("IDs: {0}" -f $ids)
    $lines += ""
    $lines += "| # | Nombre | Empresa | Perfil |"
    $lines += "|---|---|---|---|"
    foreach ($row in $batch) {
        $lines += ("| {0} | {1} | {2} | {3} |" -f $row.Numero, $row.Nombre, $row.Empresa, $row.Perfil)
    }
    $lines += ""
    $lines += "Despues de enviar este lote:"
    $lines += ""
    $lines += '```powershell'
    $lines += ("powershell -ExecutionPolicy Bypass -File .\tools\update-tracker-status.ps1 -Ids {0} -Estado enviado" -f $ids)
    $lines += '```'
    $lines += ""

    $batchNumber += 1
}

$outputDir = Split-Path -Parent $OutputPath
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

Set-Content -Path $OutputPath -Value $lines
Write-Output ("Plan generado: {0}" -f $OutputPath)
Write-Output ("Contactos pendientes listos: {0}" -f (($ready | Measure-Object).Count))

