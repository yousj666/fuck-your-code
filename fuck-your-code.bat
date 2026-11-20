@echo off
REM fuck-your-code launcher for Windows -- forwards to the Python module.
setlocal
set "DIR=%~dp0"
python "%DIR%src\fuck_your_code.py" %*
endlocal
