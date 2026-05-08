param()

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$tracker = "_local\validacion\semana-1\01-tracker-contactos.local.md"
$config = "_local\validacion\semana-1\CONFIG.local.md"
$sintesis = "mayo2026\ejecucion\semana-1\04-sintesis-dia-7.md"

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
            Numero = $cells[1].Trim()
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

function Get-ConfigValue {
    param(
        [string[]]$Content,
        [string]$Key
    )

    foreach ($line in $Content) {
        if ($line -match "^\|\s*$([regex]::Escape($Key))\s*\|") {
            $cells = $line -split "\|"
            if ($cells.Count -ge 4) {
                return $cells[2].Trim()
            }
        }
    }

    return ""
}

Write-Output "Checklist de Etapa 1"
Write-Output "===================="

Write-Output ("Config local: {0}" -f ($(if (Test-Path $config) { "OK" } else { "FALTA" })))
Write-Output ("Tracker local: {0}" -f ($(if (Test-Path $tracker) { "OK" } else { "FALTA" })))
Write-Output ("Sintesis versionable: {0}" -f ($(if (Test-Path $sintesis) { "OK" } else { "FALTA" })))

if (Test-Path $config) {
    $configContent = Get-Content $config
    $requiredConfig = @(
        "Nombre firma",
        "LinkedIn URL",
        "Calendly / Cal.com URL",
        "Franja 1 ofrecida",
        "Franja 2 ofrecida",
        "Link capitulo / borrador PDF",
        "Link OWASP MCP Top 10"
    )
    $missingConfig = @()
    foreach ($field in $requiredConfig) {
        if (-not (Get-ConfigValue $configContent $field)) {
            $missingConfig += $field
        }
    }

    Write-Output ("Campos config requeridos pendientes: {0}" -f $missingConfig.Count)
    foreach ($field in $missingConfig) {
        Write-Output ("  - {0}" -f $field)
    }
}

if (Test-Path $tracker) {
    $content = Get-Content $tracker
    $rows = Get-TrackerRows $content
    $filledRows = $rows.Count
    $rowsWithName = ($rows | Where-Object { $_.Nombre } | Measure-Object).Count
    $rowsWithCompany = ($rows | Where-Object { $_.Empresa } | Measure-Object).Count
    $rowsWithRole = ($rows | Where-Object { $_.Rol } | Measure-Object).Count
    $rowsWithProfile = ($rows | Where-Object { $_.Perfil } | Measure-Object).Count
    $rowsWithPersonalization = ($rows | Where-Object { $_.Hueco } | Measure-Object).Count
    $readyRows = ($rows | Where-Object { $_.Nombre -and $_.Empresa -and $_.Rol -and $_.Perfil -and $_.Hueco } | Measure-Object).Count
    $pendingRows = ($rows | Where-Object { $_.Estado -eq "pendiente" } | Measure-Object).Count
    $sentRows = ($rows | Where-Object { $_.Estado -eq "enviado" } | Measure-Object).Count
    $scheduledRows = ($rows | Where-Object { $_.Estado -eq "agendada" } | Measure-Object).Count
    $doneRows = ($rows | Where-Object { $_.Estado -eq "realizada" } | Measure-Object).Count

    Write-Output ("Filas con numero detectadas: {0}" -f $filledRows)
    Write-Output ("Filas con nombre detectado: {0}" -f $rowsWithName)
    Write-Output ("Filas con empresa detectada: {0}" -f $rowsWithCompany)
    Write-Output ("Filas con rol detectado: {0}" -f $rowsWithRole)
    Write-Output ("Filas con perfil detectado: {0}" -f $rowsWithProfile)
    Write-Output ("Filas con personalizacion detectada: {0}" -f $rowsWithPersonalization)
    Write-Output ("Filas listas para mensaje: {0}" -f $readyRows)
    Write-Output ("Filas pendientes detectadas: {0}" -f $pendingRows)
    Write-Output ("Mensajes enviados: {0}" -f $sentRows)
    Write-Output ("Llamadas agendadas: {0}" -f $scheduledRows)
    Write-Output ("Llamadas realizadas: {0}" -f $doneRows)
}

Write-Output ""
Write-Output "Siguiente accion esperada:"
Write-Output "1. Completar config local si hay campos pendientes"
Write-Output "2. Generar y revisar mensajes personalizados"
Write-Output "3. Enviar en lotes de 10 y marcar estado con tools/update-tracker-status.ps1"
Write-Output "4. Guardar notas por entrevista en _local/validacion/semana-1/notas/"
Write-Output "5. Copiar solo resumen agregado a mayo2026/ejecucion/semana-1/04-sintesis-dia-7.md"
