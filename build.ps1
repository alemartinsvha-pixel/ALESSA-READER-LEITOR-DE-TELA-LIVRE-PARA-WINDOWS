$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host "Instalando dependências de build..."
python -m pip install -r requirements-build.txt

Write-Host "Gerando o executável com PyInstaller..."
python -m PyInstaller `
    --clean `
    --noconfirm `
    --distpath "$ProjectRoot\dist" `
    --workpath "$ProjectRoot\build\work" `
    "$ProjectRoot\build\LeitorLivre.spec"

$Iscc = Get-Command ISCC.exe -ErrorAction SilentlyContinue

if (-not $Iscc) {
    $Candidatos = @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
    )

    foreach ($Candidato in $Candidatos) {
        if (Test-Path $Candidato) {
            $Iscc = Get-Item $Candidato
            break
        }
    }
}

if (-not $Iscc) {
    throw "Inno Setup 6 não encontrado. Instale-o ou adicione ISCC.exe ao PATH."
}

Write-Host "Criando o instalador..."
& $Iscc.Source "$ProjectRoot\installer\LeitorLivre.iss"

Write-Host ""
Write-Host "Build concluído."
Write-Host "Executável: $ProjectRoot\dist\LeitorLivre\LeitorLivre.exe"
Write-Host "Instalador: $ProjectRoot\dist\installer\LeitorLivre-Setup-0.1.0.exe"
