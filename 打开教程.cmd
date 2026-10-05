@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 goto use_py
where python >nul 2>&1
if errorlevel 1 goto missing
start "" powershell.exe -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8000/'"
python -m http.server 8000 --bind 127.0.0.1
goto done
:use_py
start "" powershell.exe -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8000/'"
py -3 -m http.server 8000 --bind 127.0.0.1
goto done
:missing
echo 请安装Python 3，或参考“学习与运行说明.html”。
:done
pause
endlocal
