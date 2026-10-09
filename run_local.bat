@echo off
echo ===============================================
echo   Starting SafeSteps Pune (Full-Stack Platform)
echo   Explore Smarter. Navigate Safer.
echo ===============================================

set "ROOT_DIR=%~dp0"
set "PATH=C:\Users\Parth Labhshetwar\.local\nodejs\node-v20.18.0-win-x64;%PATH%"

echo.
echo [1/2] Starting Flask Backend on http://localhost:5000...
start "SafeSteps Backend" cmd /k "cd /d %ROOT_DIR%backend && python app.py"

timeout /t 2 /nobreak > nul

echo.
echo [2/2] Starting Vite Frontend on http://localhost:5173...
cd /d %ROOT_DIR%frontend
npm run dev
