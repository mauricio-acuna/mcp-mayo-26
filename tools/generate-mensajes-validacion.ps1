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

function Get-FirstName {
    param([string]$FullName)

    if (-not $FullName) {
        return ""
    }

    return ($FullName.Trim() -split "\s+")[0]
}

function Format-Sentence {
    param([string]$Text)

    if (-not $Text) {
        return ""
    }

    return $Text.Trim().TrimEnd(".", " ", "`t")
}

function Get-OrPlaceholder {
    param(
        [string]$Value,
        [string]$Label
    )

    if ($Value) {
        return $Value
    }

    return "[PENDIENTE: $Label]"
}

function Get-SectorText {
    param([string]$Profile)

    switch -Regex ($Profile) {
        "healthtech|FHIR|clinica|salud" { return "healthtech y datos clinicos" }
        "fintech|CISO" { return "fintech e insurtech regulada" }
        "SRE|DevRel|MCP|OSS|GitHub" { return "developer tooling e infraestructura" }
        "auditor|SOC|ENS|GRC|seguridad" { return "seguridad, GRC y compliance" }
        "consultora|IA" { return "gobierno de IA y plataforma" }
        "SaaS" { return "SaaS B2B" }
        default { return "equipos tecnicos regulados" }
    }
}

if (-not (Test-Path $TrackerPath)) {
    throw "No existe el tracker: $TrackerPath"
}

$tracker = Get-Content $TrackerPath
$config = if (Test-Path $ConfigPath) { Get-Content $ConfigPath } else { @() }

$calendly = Get-OrPlaceholder (Get-TableValue $config "Calendly / Cal.com URL") "calendario"
$franja1 = Get-OrPlaceholder (Get-TableValue $config "Franja 1 ofrecida") "franja 1"
$franja2 = Get-OrPlaceholder (Get-TableValue $config "Franja 2 ofrecida") "franja 2"
$linkCapitulo = Get-OrPlaceholder (Get-TableValue $config "Link capitulo / borrador PDF") "link capitulo"
$linkSpec = Get-OrPlaceholder (Get-TableValue $config "Link OWASP MCP Top 10") "link spec"
$firma = Get-OrPlaceholder (Get-TableValue $config "Nombre firma") "firma"
$linkedin = Get-OrPlaceholder (Get-TableValue $config "LinkedIn URL") "linkedin"

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
    $firstName = Get-FirstName $row.Nombre
    $sector = Get-SectorText $row.Perfil
    $signal = Format-Sentence $row.Hueco
    $isOss = $row.Perfil -match "DevRel|SRE|MCP|OSS|GitHub|observabilidad|developer"

    if ($isOss) {
        $connection = "Hola $firstName, vi tu trabajo/contexto en $($row.Empresa) y me llamo la atencion que $signal. Estoy escribiendo material en espanol sobre seguridad de MCP en produccion y queria conectar para intercambiar perspectivas. Sin agenda comercial."
    } else {
        $connection = "Hola $firstName, vi tu rol en $($row.Empresa) y me llamo la atencion que $signal. Estoy investigando como equipos de $sector estan abordando la seguridad de servidores MCP en produccion. Conectamos? No vendo nada, solo me interesa el panorama."
    }

    $followUp = "Gracias por aceptar, $firstName.`n`nTe dejo dos cosas, sin coste y sin pedir nada a cambio:`n`n1. Borrador del capitulo `"Modelo de amenazas de un MCP server`" - $linkCapitulo`n2. Spec abierto OWASP MCP Top 10 - $linkSpec`n`nSi en $($row.Empresa) ya teneis algun MCP server en produccion, piloto o evaluacion, me encantaria hacerte 5 preguntas, 25 min, para entender como lo enfocais. A cambio comparto contigo el agregado de entrevistas al final.`n`nTe encaja $($franja1) o $($franja2)? Tambien dejo calendario por si te resulta mas comodo: $calendly"

    $email = "Asunto: seguridad MCP en $($row.Empresa)`n`nHola $firstName,`n`nVi que en $($row.Empresa) estais trabajando cerca de esto: $signal.`n`nEstoy escribiendo material tecnico en espanol sobre como asegurar servidores Model Context Protocol antes y durante produccion, y querria escuchar como lo estais enfocando. 25 minutos por Zoom, sin pitch.`n`nA cambio te paso:`n- Borrador del capitulo `"Modelo de amenazas de un MCP server`".`n- Acceso early al spec OWASP MCP Top 10.`n`nSi te encaja: $calendly - o respondeme con un hueco que te vaya.`n`nGracias,`n$firma`n$linkedin"

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
