@echo off
chcp 65001 >nul 2>&1
set "UCLAW_DIR=%~dp0"
set "DATA_DIR=%UCLAW_DIR%data"
set "STATE_DIR=%DATA_DIR%\.openclaw"
set "RUNTIME_DIR=%UCLAW_DIR%app\runtime"

set "NODE_VERSION=v22.22.1"
set "OPENCLAW_VERSION=2026.5.26"
set "NPM_MIRROR=https://registry.npmmirror.com"
set "NODE_TARGET=%RUNTIME_DIR%\node-win-x64"
set "NODE_EXE=%NODE_TARGET%\node.exe"

set "NEED_NODE_DOWNLOAD=0"
set "NEED_OPENCLAW_INSTALL=0"

echo ========================================
echo   ClawOSX v1.0 - Setup
echo   Portable AI Agent Init Script
echo ========================================
echo.

echo Checking Node.js runtime...
if exist "%NODE_EXE%" (
    for /f "tokens=*" %%v in ('"%NODE_EXE%" --version 2^>nul') do set NODE_VER=%%v
    echo [OK] Node.js %%NODE_VER%% already installed
) else (
    echo [INS] Need to install Node.js
    set "NEED_NODE_DOWNLOAD=1"
)

echo.
echo Checking OpenClaw...
if exist "%NODE_TARGET%\node_modules\openclaw\openclaw.mjs" (
    echo [OK] OpenClaw already installed
) else (
    echo [INS] Need to install OpenClaw
    set "NEED_OPENCLAW_INSTALL=1"
)

if "%NEED_NODE_DOWNLOAD%"=="0" if "%NEED_OPENCLAW_INSTALL%"=="0" (
    echo.
    echo Already up to date
    echo Run Windows-Start.bat to launch
    pause
    exit /b 0
)

echo.
echo Checking disk space...
set "DRIVE=%UCLAW_DIR:~0,2%"
for /f "delims=" %%a in ('powershell -Command "(Get-PSDrive -Name '%DRIVE:~0,1%' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Free) / 1MB -as [int]"') do (
    if %%a lss 300 (
        echo.
        echo [ERROR] Not enough disk space (need 300MB+)
        pause
        exit /b 1
    )
)
echo [OK] Disk space OK

if "%NEED_NODE_DOWNLOAD%"=="1" (
    echo.
    echo ========================================
    echo Downloading Node.js %NODE_VERSION%
    echo ========================================
    echo.

    if not exist "C:\Temp" mkdir "C:\Temp"
    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://npmmirror.com/binaries/node/%NODE_VERSION%/node-%NODE_VERSION%-win-x64.zip' -OutFile 'C:\Temp\node.zip' -UseBasicParsing"

    echo Extracting Node.js...
    powershell -Command "Expand-Archive -Path 'C:\Temp\node.zip' -DestinationPath '%RUNTIME_DIR%' -Force"

    for %%d in ("%RUNTIME_DIR%") do for /f "tokens=*" %%n in ('dir /b /ad "%%~d\*" 2^>nul ^| findstr node') do (
        if exist "%RUNTIME_DIR%\%%~n\node.exe" (
            if not "%%~n"=="node-win-x64" (
                move "%RUNTIME_DIR%\%%~n\*" "%RUNTIME_DIR%\node-win-x64\" >nul 2>&1
                rmdir "%RUNTIME_DIR%\%%~n" 2>nul
            )
        )
    )

    del "C:\Temp\node.zip" 2>nul
    echo [OK] Node.js installed
)

if "%NEED_OPENCLAW_INSTALL%"=="1" (
    echo.
    echo ========================================
    echo Installing OpenClaw %OPENCLAW_VERSION%
    echo ========================================
    echo.

    echo Creating package.json...
    > "%NODE_TARGET%\package.json" (
        echo {"name":"clawosx","version":"1.0.0","private":true,"dependencies":{"openclaw":"%OPENCLAW_VERSION%"}}
    )

    echo Installing OpenClaw (1-3 min, keep network)...

    set "RETRY_COUNT=0"
    :npm_retry
    set /a RETRY_COUNT+=1
    cmd /c "cd /d "%NODE_TARGET%" && npm.cmd install --registry="%NPM_MIRROR%" --ignore-scripts --no-audit --no-fund"

    if not exist "%NODE_TARGET%\node_modules\openclaw\openclaw.mjs" (
        if %RETRY_COUNT% lss 3 (
            echo [RETRY] npm install attempt %RETRY_COUNT% failed, retrying...
            goto :npm_retry
        )
        echo.
        echo [ERROR] OpenClaw install failed after 3 attempts
        pause
        exit /b 1
    )

    echo [OK] OpenClaw installed
)

echo.
echo ========================================
echo   Setup complete!
echo ========================================
echo.
echo Run ClawOSX-Config.bat to configure AI provider
echo Then run Windows-Start.bat to launch
echo.
pause