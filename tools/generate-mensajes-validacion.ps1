param(
    [string]$TrackerPath = "_local\validacion\semana-1\01-tracker-contactos.local.md",
    [string]$ConfigPath = "_local\validacion\semana-1\CONFIG.local.md",
    [string]$OutputPath = "_local\validacion\semana-1\mensajes-generados.local.md"
)

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Get-TableValue {
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

if (-not (Test-Path $TrackerPath)) {
    throw "No existe el tracker: $TrackerPath"
}

$tracker = Get-Content $TrackerPath
$config = if (Test-Path $ConfigPath) { Get-Content $ConfigPath } else { @() }

$calendly = Get-TableValue $config "Calendly / Cal.com URL"
$franja1 = Get-TableValue $config "Franja 1 ofrecida"
$franja2 = Get-TableValue $config "Franja 2 ofrecida"
$linkCapitulo = Get-TableValue $config "Link capitulo / borrador PDF"
$linkSpec = Get-TableValue $config "Link OWASP MCP Top 10"
$firma = Get-TableValue $config "Nombre firma"
$linkedin = Get-TableValue $config "LinkedIn URL"

$rows = Get-TrackerRows $tracker
$ready = $rows | Where-Object {
    $_.Nombre -and $_.Empresa -and $_.Rol -and $_.Perfil -and $_.Hueco -and $_.Estado -eq "pendiente"
}

$lines = @()
$lines += "# Mensajes generados - Semana 1"
$lines += ""
$lines += "> Archivo local generado. Revisar a mano antes de enviar. Si un mensaje suena generico, no se envia."
$lines += ""
$lines += ("Generado: {0}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"))
$lines += ("Contactos listos: {0}" -f (($ready | Measure-Object).Count))
$lines += ""

foreach ($row in $ready) {
    $sector = if ($row.Perfil) { $row.Perfil } else { "tu sector" }
    $isOss = $row.Perfil -match "DevRel|SRE|MCP|OSS|GitHub|observabilidad|developer"

    if ($isOss) {
        $connection = "Hola $($row.Nombre), vi tu trabajo/contexto en $($row.Empresa) y me llamó la atención $($row.Hueco). Estoy escribiendo material en español sobre seguridad de MCP en producción y quería conectar para intercambiar perspectivas. Sin agenda comercial."
    } else {
        $connection = "Hola $($row.Nombre), vi que lideras $($row.Rol) en $($row.Empresa) y me llamó la atención $($row.Hueco). Estoy investigando cómo equipos en $sector están abordando la seguridad de servidores MCP en producción. ¿Conectamos? No vendo nada, solo me interesa el panorama."
    }

    $followUp = "Gracias por aceptar, $($row.Nombre).`n`nTe dejo dos cosas, sin coste y sin pedir nada a cambio:`n`n1. Borrador del capítulo `"Modelo de amenazas de un MCP server`" — $linkCapitulo`n2. Spec abierto OWASP MCP Top 10 — $linkSpec`n`nSi en $($row.Empresa) ya tenéis algún MCP server en producción, piloto o evaluación, me encantaría hacerte 5 preguntas, 25 min, para entender cómo lo enfocáis. A cambio comparto contigo el agregado de entrevistas al final.`n`n¿Te encaja $franja1 o $franja2? También dejo calendario por si te resulta más cómodo: $calendly"

    $email = "Asunto: seguridad MCP en $($row.Empresa)`n`nHola $($row.Nombre),`n`nVi que en $($row.Empresa) estáis cerca de $($row.Hueco).`n`nEstoy escribiendo material técnico en español sobre cómo asegurar servidores Model Context Protocol antes y durante producción, y querría escuchar cómo lo estáis enfocando. 25 minutos por Zoom, sin pitch.`n`nA cambio te paso:`n- Borrador del capítulo `"Modelo de amenazas de un MCP server`".`n- Acceso early al spec OWASP MCP Top 10.`n`nSi te encaja: $calendly — o respóndeme con un hueco que te vaya.`n`nGracias,`n$firma`n$linkedin"

    $lines += "## $($row.Numero). $($row.Nombre) - $($row.Empresa)"
    $lines += ""
    $lines += "- Rol: $($row.Rol)"
    $lines += "- Perfil: $($row.Perfil)"
    $lines += "- Personalizacion: $($row.Hueco)"
    $lines += ""
    $lines += "### LinkedIn conexion"
    $lines += ""
    $lines += $connection
    $lines += ""
    $lines += "### LinkedIn post-aceptacion"
    $lines += ""
    $lines += $followUp
    $lines += ""
    $lines += "### Email frio"
    $lines += ""
    $lines += $email
    $lines += ""
}

$outputDir = Split-Path -Parent $OutputPath
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

Set-Content -Path $OutputPath -Value $lines
Write-Output ("Mensajes generados: {0}" -f $OutputPath)
Write-Output ("Contactos listos: {0}" -f (($ready | Measure-Object).Count))
