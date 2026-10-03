@echo off
setlocal

cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python launcher 'py' was not found in PATH.
    echo Install Python 3 and ensure 'py' is available, then rerun this script.
    exit /b 1
)

py -m pip install -q -r requirements.txt
py -m pip install -q pytest
py -m pytest -q

if errorlevel 1 (
    echo.
    echo Test run failed. Review the pytest output above.
    exit /b %errorlevel%
)

echo.
echo Tests passed.
exit /b 0
