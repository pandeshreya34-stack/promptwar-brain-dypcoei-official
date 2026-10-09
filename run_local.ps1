# SafeSteps Pune - Local Startup Script (PowerShell)
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Starting SafeSteps Pune (Full-Stack Platform)" -ForegroundColor Cyan
Write-Host "  Explore Smarter. Navigate Safer." -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start Flask Backend
Write-Host "`n[1/2] Starting Flask Backend on http://localhost:5000..." -ForegroundColor Green
$backendJob = Start-Process -FilePath "python" -ArgumentList "app.py" -WorkingDirectory "$scriptDir\backend" -PassThru

Start-Sleep -Seconds 2

# 2. Start Vite Frontend
Write-Host "`n[2/2] Starting Vite React Frontend on http://localhost:5173..." -ForegroundColor Green
$env:PATH = "C:\Users\Parth Labhshetwar\.local\nodejs\node-v20.18.0-win-x64;" + $env:PATH
Set-Location "$scriptDir\frontend"
npm run dev
