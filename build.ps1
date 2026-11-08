$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$PythonLauncher = Get-Command py -ErrorAction SilentlyContinue
if (-not $PythonLauncher) {
    throw "Python Launcher 'py' não foi encontrado. Instale o Python 3.14.6 com o launcher habilitado."
}

# Cria um ambiente isolado com a versão 3.14 instalada.
$BuildVenv = Join-Path $ProjectRoot ".venv-build"
$BuildPython = Join-Path $BuildVenv "Scripts\python.exe"
Write-Host "Criando/atualizando ambiente de build com Python 3.14..."
& $PythonLauncher.Source -3.14 -m venv $BuildVenv
if ($LASTEXITCODE -ne 0) {
    throw "Não foi possível criar o ambiente virtual com py -3.14. Confirme a instalação do Python 3.14.6."
}
if (-not (Test-Path $BuildPython)) {
    throw "Python do ambiente de build não encontrado: $BuildPython"
}

$PythonVersion = (& $BuildPython --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $PythonVersion -ne "Python 3.14.6") {
    throw "Este build requer Python 3.14.6. Encontrado: $PythonVersion"
}
Write-Host "Usando $PythonVersion"

Write-Host "Atualizando pip e instalando dependências de build..."
& $BuildPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Falha ao atualizar pip." }
& $BuildPython -m pip install --upgrade -r requirements-build.txt
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao instalar dependências de build. Leia a mensagem do pip acima."
}

Write-Host "Versão do PyInstaller:"
& $BuildPython -m PyInstaller --version
if ($LASTEXITCODE -ne 0) { throw "PyInstaller não inicializou corretamente." }

$SpecPath = Join-Path $ProjectRoot "build\LeitorLivre.spec"
if (-not (Test-Path $SpecPath)) {
    throw "Arquivo de especificação não encontrado: $SpecPath"
}

Write-Host "Gerando o executável com PyInstaller..."
& $BuildPython -m PyInstaller `
    --clean `
    --noconfirm `
    --distpath (Join-Path $ProjectRoot "dist") `
    --workpath (Join-Path $ProjectRoot "build\work") `
    $SpecPath
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller falhou ao gerar o executável. Consulte o erro exibido acima."
}

# Procura ISCC.exe no PATH ou nos locais comuns do Inno Setup 7 e 6.
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
& $IsccPath (Join-Path $ProjectRoot "installer\LeitorLivre.iss")
if ($LASTEXITCODE -ne 0) { throw "Falha ao criar o instalador Inno Setup." }

$InstallerPath = Join-Path $ProjectRoot "dist\installer\LeitorLivre-Setup-0.1.0.exe"
if (-not (Test-Path $InstallerPath)) {
    throw "Build terminou, mas o instalador esperado não foi encontrado: $InstallerPath"
}

Write-Host ""
Write-Host "Build concluído com sucesso."
Write-Host "Executável: $(Join-Path $ProjectRoot 'dist\LeitorLivre\LeitorLivre.exe')"
Write-Host "Instalador: $InstallerPath"
