@echo off
setlocal enabledelayedexpansion

:: Determine the port (default 8765, check .env if present)
set PORT=8765
if exist .env (
    for /f "tokens=1,2 delims==" %%a in (.env) do (
        if "%%a"=="PORT" set PORT=%%b
    )
)

echo [launcher] checking for existing instance on port !PORT!...
set "PS_CMD=powershell -NoProfile -Command "$resp = try { Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:!PORT!/api/admin/shutdown' -ErrorAction SilentlyContinue } catch { $_.Exception.Response }; if ($resp.StatusCode -eq 200) { write-host 200 }""
for /f "usebackq tokens=*" %%i in (`!PS_CMD!`) do set STATUS=%%i

if "!STATUS!"=="200" (
    echo [launcher] sent shutdown signal to existing instance. waiting for it to exit...
    timeout /t 2 /nobreak > nul
)

echo [launcher] starting Trade Hunter...
:START
py -m app %*
if !ERRORLEVEL! equ 3 (
    echo [launcher] server restart requested (exit code 3)...
    goto START
)
exit /b !ERRORLEVEL!
