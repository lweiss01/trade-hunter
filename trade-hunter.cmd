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
curl -s -o NUL -w "%%{http_code}" -X POST http://127.0.0.1:!PORT!/api/admin/shutdown > temp_status.txt
set /p STATUS=<temp_status.txt
del temp_status.txt

if "!STATUS!"=="200" (
    echo [launcher] sent shutdown signal to existing instance. waiting for it to exit...
    timeout /t 2 /nobreak > /dev/null
)

echo [launcher] starting Trade Hunter...
py -m app %*
