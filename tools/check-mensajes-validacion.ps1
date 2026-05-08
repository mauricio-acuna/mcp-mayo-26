param(
    [string]$MessagesPath = "_local\validacion\semana-1\mensajes-generados.local.md",
    [switch]$FailOnWarnings
)

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not (Test-Path $MessagesPath)) {
    throw "No existe el archivo de mensajes: $MessagesPath"
}

$content = Get-Content $MessagesPath
$text = $content -join "`n"

$contactCount = ($content | Select-String -Pattern "^## \d+\. " | Measure-Object).Count
$placeholderMatches = $content | Select-String -Pattern "\[PENDIENTE:"
$genericPatterns = @(
    "vi tu perfil",
    "me parecio interesante",
    "trabajais con tecnologia",
    "interesante perfil",
    "como sabes"
)

$genericMatches = @()
foreach ($pattern in $genericPatterns) {
    $genericMatches += $content | Select-String -Pattern ([regex]::Escape($pattern)) -CaseSensitive:$false
}

$doublePunctuation = $content | Select-String -Pattern "\.\."
$emptyLinkIndicators = $content | Select-String -Pattern " -\s*$|:\s*$"

Write-Output "Revision de mensajes de validacion"
Write-Output "=================================="
Write-Output ("Archivo: {0}" -f $MessagesPath)
Write-Output ("Contactos detectados: {0}" -f $contactCount)
Write-Output ("Placeholders pendientes: {0}" -f (($placeholderMatches | Measure-Object).Count))
Write-Output ("Frases genericas detectadas: {0}" -f (($genericMatches | Measure-Object).Count))
Write-Output ("Doble puntuacion detectada: {0}" -f (($doublePunctuation | Measure-Object).Count))
Write-Output ("Posibles links/campos vacios: {0}" -f (($emptyLinkIndicators | Measure-Object).Count))

if ($placeholderMatches) {
    Write-Output ""
    Write-Output "Placeholders:"
    $placeholderMatches | Select-Object -First 20 | ForEach-Object {
        Write-Output ("  L{0}: {1}" -f $_.LineNumber, $_.Line.Trim())
    }
}

if ($genericMatches) {
    Write-Output ""
    Write-Output "Frases genericas:"
    $genericMatches | Select-Object -First 20 | ForEach-Object {
        Write-Output ("  L{0}: {1}" -f $_.LineNumber, $_.Line.Trim())
    }
}

if ($doublePunctuation) {
    Write-Output ""
    Write-Output "Doble puntuacion:"
    $doublePunctuation | Select-Object -First 20 | ForEach-Object {
        Write-Output ("  L{0}: {1}" -f $_.LineNumber, $_.Line.Trim())
    }
}

$hasWarnings = $placeholderMatches -or $genericMatches -or $doublePunctuation -or $emptyLinkIndicators
if ($FailOnWarnings -and $hasWarnings) {
    throw "La revision encontro avisos. Corregir antes de enviar."
}

if (-not $hasWarnings) {
    Write-Output ""
    Write-Output "OK: no se detectaron avisos obvios."
}

