@echo off
chcp 65001 >nul 2>&1
set "UCLAW_DIR=%~dp0"
set "DATA_DIR=%UCLAW_DIR%data"
set "STATE_DIR=%DATA_DIR%\.openclaw"
set "RUNTIME_DIR=%UCLAW_DIR%app\runtime"
set "NODE_TARGET=%RUNTIME_DIR%\node-win-x64"
set "NODE_EXE=%NODE_TARGET%\node.exe"
set "OPENCLAW_MJS=%NODE_TARGET%\node_modules\openclaw\openclaw.mjs"
set "DEFAULT_PORT=18789"

if not exist "%NODE_EXE%" (
    echo [ERROR] Node.js not found. Run Windows-Setup.bat first.
    pause
    exit /b 1
)

if not exist "%OPENCLAW_MJS%" (
    echo [ERROR] OpenClaw not found. Run Windows-Setup.bat first.
    pause
    exit /b 1
)

set "GATEWAY_LOG=%DATA_DIR%\logs\gateway.log"
set "PID_FILE=%DATA_DIR%\.openclaw\gateway.pid"

if not exist "%DATA_DIR%\logs" mkdir "%DATA_DIR%\logs" 2>nul
if not exist "%DATA_DIR%\.openclaw" mkdir "%DATA_DIR%\.openclaw" 2>nul

for /f "tokens=2 delims==." %%a in ('"%NODE_EXE%" -e "process.stdout.write(Date.now().toString())" 2^>nul') do set RANDOM_PORT=1878%%a:~-3

echo Starting Gateway on port %RANDOM_PORT%...
start /min cmd /c ""%NODE_EXE%" "%OPENCLAW_MJS%" gateway run --port %RANDOM_PORT% --auth none --allow-unconfigured 2>>"%GATEWAY_LOG%"

set "WAIT_COUNT=0"
:wait_loop
ping -n 2 127.0.0.1 >nul 2>&1
set /a WAIT_COUNT+=1

powershell -Command "Try { $c = New-Object System.Net.Sockets.TcpClient; $c.Connect('127.0.0.1', %RANDOM_PORT%); $c.Close(); exit 0 } Catch { exit 1 }" 2>nul
if not errorlevel 1 goto :ready

if %WAIT_COUNT% geq 30 (
    echo.
    echo [ERROR] Gateway failed to start. Check %GATEWAY_LOG%
    pause
    exit /b 1
)

goto :wait_loop

:ready
echo [OK] Gateway ready at http://127.0.0.1:%RANDOM_PORT%/
echo %RANDOM_PORT% > "%STATE_DIR%\port.txt"
echo Gateway started. Close this window to stop.
cmd /k