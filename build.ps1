$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

# Usa explicitamente a família Python 3.15 para evitar compilar com outra versão.
$PythonLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($PythonLauncher) {
    $PythonCommand = $PythonLauncher.Source
    $PythonPrefixArgs = @("-3.15")
} else {
    $PythonLauncher = Get-Command python -ErrorAction SilentlyContinue
    if (-not $PythonLauncher) {
        throw "Python 3.15 não foi encontrado. Instale-o e habilite o launcher 'py' ou o PATH."
    }
    $PythonCommand = $PythonLauncher.Source
    $PythonPrefixArgs = @()
}

$PythonVersion = (& $PythonCommand @PythonPrefixArgs --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $PythonVersion -notmatch '^Python 3\.15\.') {
    throw "Este build requer Python 3.15.x. Versão encontrada: $PythonVersion"
}
Write-Host "Usando $PythonVersion"

Write-Host "Atualizando pip e instalando dependências de build..."
& $PythonCommand @PythonPrefixArgs -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Falha ao atualizar pip." }
& $PythonCommand @PythonPrefixArgs -m pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) { throw "Falha ao instalar dependências; confirme se PyInstaller já suporta esta versão do Python." }

Write-Host "Gerando o executável com PyInstaller..."
& $PythonCommand @PythonPrefixArgs -m PyInstaller `
    --clean `
    --noconfirm `
    --distpath "$ProjectRoot\dist" `
    --workpath "$ProjectRoot\build\work" `
    "$ProjectRoot\build\LeitorLivre.spec"
if ($LASTEXITCODE -ne 0) { throw "Falha ao gerar o executável com PyInstaller." }

# Procura primeiro Inno Setup 7.1 e mantém fallback para instalações comuns.
$IsccCommand = Get-Command ISCC.exe -ErrorAction SilentlyContinue
$IsccPath = if ($IsccCommand) { $IsccCommand.Source } else { $null }

if (-not $IsccPath) {
    $ProgramFilesRoots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}) |
        Where-Object { $_ } |
        Select-Object -Unique

    $Candidates = foreach ($Root in $ProgramFilesRoots) {
        Join-Path $Root "Inno Setup 7\ISCC.exe"
        Join-Path $Root "Inno Setup 6\ISCC.exe"
    }

    $IsccPath = $Candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}

if (-not $IsccPath) {
    throw "ISCC.exe não encontrado. Instale Inno Setup 7.1 ou adicione ISCC.exe ao PATH."
}

Write-Host "Usando compilador Inno Setup: $IsccPath"
Write-Host "Criando o instalador..."
& $IsccPath "$ProjectRoot\installer\LeitorLivre.iss"
if ($LASTEXITCODE -ne 0) { throw "Falha ao criar o instalador Inno Setup." }

$InstallerPath = Join-Path $ProjectRoot "dist\installer\LeitorLivre-Setup-0.1.0.exe"
if (-not (Test-Path $InstallerPath)) {
    throw "Build terminou, mas o instalador esperado não foi encontrado: $InstallerPath"
}

Write-Host ""
Write-Host "Build concluído com sucesso."
Write-Host "Executável: $ProjectRoot\dist\LeitorLivre\LeitorLivre.exe"
Write-Host "Instalador: $InstallerPath"
