param()

$ErrorActionPreference = "Continue"

function Show-Check {
    param(
        [string]$Name,
        [bool]$Ok,
        [string]$Detail = ""
    )

    $status = if ($Ok) { "OK" } else { "PENDIENTE" }
    if ($Detail) {
        Write-Output ("[{0}] {1} - {2}" -f $status, $Name, $Detail)
    } else {
        Write-Output ("[{0}] {1}" -f $status, $Name)
    }
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$git = Get-Command git -ErrorAction SilentlyContinue
Show-Check "Git instalado" ($null -ne $git) ($(if ($git) { git --version } else { "" }))

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
Show-Check "Python virtualenv" (Test-Path $venvPython) $venvPython
if (Test-Path $venvPython) {
    & $venvPython --version
}

$gh = Get-Command gh -ErrorAction SilentlyContinue
if ($gh) {
    Show-Check "GitHub CLI en PATH" $true (& gh --version | Select-Object -First 1)
} else {
    $ghProgramFiles = Join-Path $env:ProgramFiles "GitHub CLI\gh.exe"
    Show-Check "GitHub CLI instalado" (Test-Path $ghProgramFiles) $ghProgramFiles
}

$docker = Get-Command docker -ErrorAction SilentlyContinue
Show-Check "Docker instalado" ($null -ne $docker) "Opcional hasta retomar MediMind tecnico"

Show-Check "_local ignorado por git" ((git check-ignore _local 2>$null) -eq "_local")
Show-Check ".venv ignorado por git" ((git check-ignore .venv 2>$null) -eq ".venv")

Write-Output ""
Write-Output "Resumen git:"
git status --short --ignored

