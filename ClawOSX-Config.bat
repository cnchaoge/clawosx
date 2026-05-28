@echo off
> nul 2>&1 where python
if %errorlevel% neq 0 (
    echo ClawOSX Config requires Python.
    echo Please install Python 3 from:
    echo https://www.python.org/downloads/
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
)
python "%~dp0clawosx_config.py"