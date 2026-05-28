@echo off
chcp 65001 >nul 2>&1
title ClawOSX Setup

echo.
echo ========================================
echo   ClawOSX v1.0 - Setup
echo   Portable AI Agent Init Script
echo ========================================
echo.

set "UCLAW_DIR=%~dp0"
set "APP_DIR=%UCLAW_DIR%app"
set "RUNTIME_DIR=%APP_DIR%\runtime"
set "DATA_DIR=%UCLAW_DIR%data"
set "STATE_DIR=%DATA_DIR%\.openclaw"

set "NODE_VERSION=v22.22.1"
set "OPENCLAW_VERSION=2026.5.26"
set "NPM_MIRROR=https://registry.npmmirror.com"
set "NODE_TARGET=%RUNTIME_DIR%\node-win-x64"
set "NODE_EXE=%NODE_TARGET%\node.exe"

set "NEED_NODE_DOWNLOAD=0"
set "NEED_OPENCLAW_INSTALL=0"

echo Checking Node.js runtime...
if exist "%NODE_EXE%" (
    for /f "tokens=*" %%v in ('"%NODE_EXE%" --version 2^>nul') do set NODE_VER=%%v
    echo [OK] Node.js already installed
) else (
    echo [DL] Need to download Node.js %NODE_VERSION%
    set "NEED_NODE_DOWNLOAD=1"
)

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
    if %%a GEQ 300 (
        echo [OK] Disk space OK
    ) else (
        echo.
        echo [ERROR] Not enough disk space (need 300MB+)
        pause
        exit /b 1
    )
)

if "%NEED_NODE_DOWNLOAD%"=="1" (
    echo.
    echo ========================================
    echo Downloading Node.js %NODE_VERSION%
    echo ========================================
    echo.

    if not exist "%NODE_TARGET%" mkdir "%NODE_TARGET%"
    if not exist "C:\Temp" mkdir "C:\Temp"

    echo Mirror: https://npmmirror.com/mirrors/node
    echo Downloading, please wait...

    curl -L -o "C:\Temp\node-dl.zip" "https://npmmirror.com/mirrors/node/v22.22.1/node-v22.22.1-win-x64.zip"
    if errorlevel 1 (
        echo.
        echo [ERROR] Download failed. Check network.
        echo.
        pause
        exit /b 1
    )

    echo [OK] Download complete, extracting...

    powershell -ExecutionPolicy Bypass -Command "Expand-Archive -Path 'C:\Temp\node-dl.zip' -DestinationPath '%NODE_TARGET%' -Force"

    REM Flatten nested directory (node-v22.22.1-win-x64/ inside target)
    for /f "tokens=*" %%d in ('dir /b /ad "%NODE_TARGET%" 2^>nul') do (
        for /f "tokens=*" %%f in ('dir /b "%NODE_TARGET%\%%d" 2^>nul') do (
            move /y "%NODE_TARGET%\%%d\%%f" "%NODE_TARGET%\" >nul 2>&1
        )
        rd /s /q "%NODE_TARGET%\%%d" >nul 2>&1
    )

    del /f /q "C:\Temp\node-dl.zip" 2>nul

    if not exist "%NODE_EXE%" (
        echo.
        echo [ERROR] Extraction failed
        pause
        exit /b 1
    )

    for /f "tokens=*" %%v in ('"%NODE_EXE%" --version 2^>nul') do set NODE_VER=%%v
    echo [OK] Node.js %NODE_VER% installed
)

if "%NEED_OPENCLAW_INSTALL%"=="1" (
    echo.
    echo ========================================
    echo Installing OpenClaw %OPENCLAW_VERSION%
    echo ========================================
    echo.

    echo Creating package.json...
    powershell -ExecutionPolicy Bypass -Command "Set-Content -Path '%NODE_TARGET%\package.json' -Value '{\""name\"":\""clawosx\"",\""version\"":\""1.0.0\"",\""private\"":true,\""dependencies\"":{\""openclaw\"":\""%OPENCLAW_VERSION%\""}}' -Encoding UTF8"

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
echo Initializing data directory
echo ========================================
echo.

if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
if not exist "%STATE_DIR%" mkdir "%STATE_DIR%"
if not exist "%DATA_DIR%\memory" mkdir "%DATA_DIR%\memory"
if not exist "%DATA_DIR%\backups" mkdir "%DATA_DIR%\backups"
if not exist "%DATA_DIR%\logs" mkdir "%DATA_DIR%\logs"

if not exist "%STATE_DIR%\openclaw.json" (
    powershell -ExecutionPolicy Bypass -Command "Set-Content -Path '%STATE_DIR%\openclaw.json' -Value '{\""gateway\"":{\""mode\"":\""local\"",\""auth\"":{\""mode\"":\""none\""}},\"\"models\"":{\""mode\"":\""merge\"",\""providers\"":{}},\"\"agents\"":{\""defaults\"":{}}}' -Encoding UTF8"
    echo [OK] Config created
) else (
    echo [OK] Config already exists
)

echo.
echo ========================================
echo Setup Complete
echo ========================================
echo.
echo Run Windows-Start.bat to launch ClawOSX
echo.
pause
exit /b 0