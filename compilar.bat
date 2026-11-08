@echo off
setlocal
cd /d "%~dp0"
title Compilar LeitorLivre

echo ============================================
echo        Compilacao do LeitorLivre
echo ============================================
echo.

echo Iniciando o script de build do Windows...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"
set "BUILD_EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%BUILD_EXIT_CODE%"=="0" (
    echo ERRO: a compilacao falhou. Consulte as mensagens acima.
    echo Verifique se Python 3.15.x e Inno Setup 7.1 estao instalados.
    pause
    exit /b %BUILD_EXIT_CODE%
)

echo Compilacao concluida com sucesso!
echo O instalador deve estar em:
echo %~dp0dist\installer\LeitorLivre-Setup-0.1.0.exe
pause
exit /b 0
