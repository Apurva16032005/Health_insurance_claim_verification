@echo off
echo ===================================================
echo   Starting FraudShield AI (Backend + Frontend)
echo ===================================================
echo.
echo [1/2] Launching Backend Server...
start "FraudShield Backend" cmd /k "%~dp0run_backend.bat"

timeout /t 3 /nobreak >nul

echo [2/2] Launching Frontend Dashboard...
start "FraudShield Frontend" cmd /k "%~dp0run_frontend.bat"

echo.
echo Application started! Check the opened terminal windows.
