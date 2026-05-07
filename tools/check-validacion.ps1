param()

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$tracker = "_local\validacion\semana-1\01-tracker-contactos.local.md"
$config = "_local\validacion\semana-1\CONFIG.local.md"
$sintesis = "mayo2026\ejecucion\semana-1\04-sintesis-dia-7.md"

Write-Output "Checklist de Etapa 1"
Write-Output "===================="

Write-Output ("Config local: {0}" -f ($(if (Test-Path $config) { "OK" } else { "FALTA" })))
Write-Output ("Tracker local: {0}" -f ($(if (Test-Path $tracker) { "OK" } else { "FALTA" })))
Write-Output ("Sintesis versionable: {0}" -f ($(if (Test-Path $sintesis) { "OK" } else { "FALTA" })))

if (Test-Path $tracker) {
    $content = Get-Content $tracker
    $filledRows = ($content | Select-String -Pattern "^\|\s*\d+\s*\|\s*\S" | Measure-Object).Count
    $rowsWithCompany = ($content | Select-String -Pattern "^\|\s*\d+\s*\|\s*[^|]*\|\s*\S" | Measure-Object).Count
    $rowsWithRole = ($content | Select-String -Pattern "^\|\s*\d+\s*\|\s*[^|]*\|\s*[^|]*\|\s*\S" | Measure-Object).Count
    $pendingRows = ($content | Select-String -Pattern "\|\s*pendiente\s*\|" | Measure-Object).Count
    Write-Output ("Filas con numero detectadas: {0}" -f $filledRows)
    Write-Output ("Filas con empresa detectada: {0}" -f $rowsWithCompany)
    Write-Output ("Filas con rol detectado: {0}" -f $rowsWithRole)
    Write-Output ("Filas pendientes detectadas: {0}" -f $pendingRows)
}

Write-Output ""
Write-Output "Siguiente accion esperada:"
Write-Output "1. Completar 30 contactos en _local/validacion/semana-1/01-tracker-contactos.local.md"
Write-Output "2. Enviar mensajes personalizados"
Write-Output "3. Guardar notas por entrevista en _local/validacion/semana-1/notas/"
Write-Output "4. Copiar solo resumen agregado a mayo2026/ejecucion/semana-1/04-sintesis-dia-7.md"
