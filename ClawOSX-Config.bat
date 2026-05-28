@echo off
chcp 65001 >nul 2>&1
if exist "%~dp0clawosx_config.py" (
    cmd /k python "%~dp0clawosx_config.py"
) else (
    echo [ERROR] clawosx_config.py not found in same folder.
    pause
)