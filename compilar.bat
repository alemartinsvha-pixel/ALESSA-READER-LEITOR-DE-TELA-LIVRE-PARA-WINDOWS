@echo off
setlocal
cd /d "%~dp0"
title Compilar LeitorLivre

echo ============================================
echo        Compilacao do LeitorLivre
echo ============================================
echo.

echo Verificando Python 3.14 e iniciando o build...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"
set "BUILD_EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%BUILD_EXIT_CODE%"=="0" (
    echo ERRO: a compilacao falhou. Consulte a mensagem acima.
    echo O build exige Python 3.14.x, dependencias compativeis e Inno Setup 7.1.
    pause
    exit /b %BUILD_EXIT_CODE%
)

echo Compilacao concluida com sucesso!
echo O instalador deve estar em:
echo %~dp0dist\installer\LeitorLivre-Setup-0.1.0.exe
pause
exit /b 0
