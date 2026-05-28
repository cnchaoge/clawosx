@echo off
chcp 65001 >nul 2>&1
title ClawOSX - AI Assistant

echo.
echo ========================================
echo   ClawOSX v1.0 - Portable AI Agent
echo ========================================
echo.

set "UCLAW_DIR=%~dp0"
set "APP_DIR=%UCLAW_DIR%app"
set "RUNTIME_DIR=%APP_DIR%\runtime"
set "DATA_DIR=%UCLAW_DIR%data"
set "STATE_DIR=%DATA_DIR%\.openclaw"
set "NODE_DIR=%RUNTIME_DIR%\node-win-x64"
set "NODE_EXE=%NODE_DIR%\node.exe"
set "OPENCLAW_MJS=%NODE_DIR%\node_modules\openclaw\openclaw.mjs"
set "LOG_FILE=%DATA_DIR%\logs\gateway.log"

set "OPENCLAW_HOME=%DATA_DIR%"
set "OPENCLAW_STATE_DIR=%STATE_DIR%"
set "OPENCLAW_CONFIG_PATH=%STATE_DIR%\openclaw.json"
set "OPENCLAW_DISABLE_BONJOUR=1"

if not exist "%NODE_EXE%" (
    echo.
    echo [ERROR] Node.js not found
    echo Please run Windows-Setup.bat first
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('"%NODE_EXE%" --version 2^>nul') do set NODE_VER=%%v
echo Node.js: %NODE_VER%

if not exist "%OPENCLAW_MJS%" (
    echo.
    echo [ERROR] OpenClaw not installed
    echo Please run Windows-Setup.bat first
    echo.
    pause
    exit /b 1
)
echo OpenClaw: installed

if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
if not exist "%STATE_DIR%" mkdir "%STATE_DIR%"
if not exist "%DATA_DIR%\memory" mkdir "%DATA_DIR%\memory"
if not exist "%DATA_DIR%\backups" mkdir "%DATA_DIR%\backups"
if not exist "%DATA_DIR%\logs" mkdir "%DATA_DIR%\logs"

REM Fix EISDIR error: remove stale plugin-skills directory
if exist "%STATE_DIR%\plugin-skills\browser-automation" (
    powershell -Command "Remove-Item -Recurse -Force '%STATE_DIR%\plugin-skills\browser-automation' -ErrorAction SilentlyContinue"
    echo [OK] Fixed stale plugin-skills directory
)

REM Read port from config (written by clawosx-start.hta)
set "PORT="
if exist "%STATE_DIR%\port.txt" (
    set /p PORT=<"%STATE_DIR%\port.txt"
    if defined PORT (
        echo [OK] Port loaded from config: %PORT%
    )
)
if not defined PORT set "PORT=18789"

REM Check port is available
:check_port
powershell -Command "try { $t = New-Object System.TcpClient; $t.Connect('127.0.0.1', %PORT%); $t.Close(); exit 1 } catch { exit 0 }" >nul 2>&1
if errorlevel 1 (
    set /a PORT+=1
    if %PORT% gtr 18799 (
        echo.
        echo [ERROR] No free port in 18789-18799
        echo.
        pause
        exit /b 1
    )
    goto :check_port
)

echo Using port: %PORT%
echo.

cd /d "%NODE_DIR%"
start /min "" "%NODE_EXE%" "%OPENCLAW_MJS%" gateway run --allow-unconfigured --force --port %PORT% --auth none >>"%LOG_FILE%" 2>&1

echo Waiting for Gateway to be ready...
set "MAX_WAIT=20"
set "WAITED=0"

:wait_loop
powershell -Command "try { Invoke-WebRequest -Uri 'http://127.0.0.1:%PORT%/' -UseBasicParsing -TimeoutSec 1 -ErrorAction Stop | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 0 (
    echo Gateway ready!
    goto :open_browser
)
timeout /t 1 /nobreak >nul
set /a WAITED+=1
if %WAITED% lss %MAX_WAIT% goto :wait_loop

echo [WARNING] Gateway took too long.
timeout /t 3 /nobreak >nul

:open_browser
start "" "http://127.0.0.1:%PORT%/"

:done
echo.
echo ========================================
echo   ClawOSX is running
echo ========================================
echo.
echo Open: http://127.0.0.1:%PORT%/
echo.
echo Gateway is running in the background
echo Close this window to stop
pause >nul

taskkill /f /im node.exe >nul 2>&1
exit /b 0