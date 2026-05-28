@echo off
> nul 2>&1 where python
if %errorlevel% neq 0 (
    echo ClawOSX Config requires Python 3.
    echo Please install from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
cmd /k python "%~dp0clawosx_config.py"