@echo off
setlocal

set "APP_PORT=8501"
set "APP_URL=http://localhost:%APP_PORT%"
set "APP_DIR=%~dp0"

cd /d "%APP_DIR%"

call :find_python
if errorlevel 1 goto :end

call :check_port
if errorlevel 1 goto :end

call :check_streamlit
if errorlevel 1 goto :end

echo Starting app from "%APP_DIR%"
start "" %PYTHON_CMD% -m streamlit run app.py --server.headless true --server.port %APP_PORT%

timeout /t 3 /nobreak >nul
start "" "%APP_URL%"

echo.
echo The app should now be opening in your browser:
echo   %APP_URL%
echo.
echo If the page does not open automatically, copy the address above into your browser.
goto :end

:find_python
set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    goto :eof
)

where python >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :eof
)

echo.
echo Python was not found on this computer.
echo Install Python first, then run this script again.
exit /b 1

:check_port
powershell -NoProfile -ExecutionPolicy Bypass -Command "if (Get-NetTCPConnection -LocalPort %APP_PORT% -State Listen -ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"
if not errorlevel 1 goto :eof

echo.
echo Port %APP_PORT% is already in use.
echo If this app is already running, the browser will open the existing page.
echo Otherwise, stop the process using that port and try again.
start "" "%APP_URL%"
exit /b 1

:check_streamlit
%PYTHON_CMD% -c "import streamlit" >nul 2>nul
if not errorlevel 1 goto :eof

echo.
echo Streamlit is not installed in the current Python environment.
echo Run the following command, then try again:
echo   python -m pip install -r requirements.txt
exit /b 1

:end
endlocal
