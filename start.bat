@echo off
REM ==============================================================
REM  Ehtiyat hisseleri - Windows launcher
REM  Ilk defe: virtual environment qurur + asililiqlari install edir
REM  Sonrakilar: birbaşa serveri qaldirir
REM
REM  LAN rejimi: HOST=0.0.0.0 - başqa kompüterlər də bu serverə qoşula bilər
REM ==============================================================

setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo.
echo ================================================
echo  Ehtiyat hisseleri
echo ================================================
echo Qovluq: %CD%
echo.

REM ---- Python komandasi tapilir ----
set "PY="
py -3.7 --version >nul 2>&1
if not errorlevel 1 (set "PY=py -3.7" & goto :py_found)
py --version >nul 2>&1
if not errorlevel 1 (set "PY=py" & goto :py_found)
python --version >nul 2>&1
if not errorlevel 1 (set "PY=python" & goto :py_found)

echo [XETA] Python tapilmadi.
echo Python 3.7.9 endirin ve "Add Python to PATH" secerek qurun:
echo   https://www.python.org/ftp/python/3.7.9/python-3.7.9.exe
pause
exit /b 1

:py_found
echo [INFO] Python komandasi: !PY!
!PY! --version
echo.

REM ---- venv yoxdursa yaradilir ----
if exist "venv\Scripts\activate.bat" goto :venv_exists

echo [SETUP] Method 1: standart venv sinayiriq...
!PY! -m venv venv
if not errorlevel 1 goto :venv_created

if exist "venv" rmdir /s /q venv

echo.
echo [SETUP] Method 2: --without-pip sinayiriq...
!PY! -m venv --without-pip venv
if errorlevel 1 goto :try_virtualenv

call venv\Scripts\activate.bat
python -m ensurepip --upgrade
if errorlevel 1 (
    call venv\Scripts\deactivate.bat 2>nul
    if exist "venv" rmdir /s /q venv
    goto :try_virtualenv
)
python -m pip install --upgrade pip
goto :venv_created

:try_virtualenv
echo.
echo [SETUP] Method 3: virtualenv paketi ile sinayiriq...
!PY! -m pip install --user virtualenv
if errorlevel 1 (
    !PY! -m pip install --user --trusted-host pypi.org --trusted-host files.pythonhosted.org virtualenv
    if errorlevel 1 goto :venv_all_failed
)
!PY! -m virtualenv venv
if errorlevel 1 goto :venv_all_failed
goto :venv_created

:venv_all_failed
echo.
echo [XETA] Virtual environment 3 metodda da yaradila bilmedi.
echo Muhtemel sebebler:
echo   1. Antivirus bloklayir
echo   2. Qovluq yolunda Azerbaycan herfleri var (ə, ö, ü, i, ...)
echo      -^> Layiheni C:\zapcast kimi Latin herfli qovluqda saxlayin
echo   3. Python "Just for me" qurulub -^> "Install for all users" ile yeniden qurun
pause
exit /b 1

:venv_created
echo.
echo [SETUP] Virtual environment yaradildi.
echo.

:venv_exists
call venv\Scripts\activate.bat

REM ---- Asililiqlar ----
if not exist "venv\Scripts\flask.exe" (
    echo [SETUP] Asililiqlar install olunur...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [WARN] Standart install ugursuz, --trusted-host ile sinayiriq...
        pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
        if errorlevel 1 (
            echo [XETA] pip install islemedi.
            pause
            exit /b 1
        )
    )
    echo [SETUP] Asililiqlar qurashdi.
    echo.
)

REM ---- .env ----
if not exist ".env" (
    if exist ".env.example" (
        copy /y .env.example .env >nul
    )
)

REM ---- LAN mode: HOST-u 0.0.0.0 override et ki, basqa kompuuter de qosula bilsin ----
set HOST=0.0.0.0
set PORT=5001

REM ---- LAN IP-ni tap ----
set "LAN_IP="
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /c:"IPv4"') do (
    if not defined LAN_IP (
        set "LAN_IP=%%A"
        set "LAN_IP=!LAN_IP: =!"
    )
)
if not defined LAN_IP set "LAN_IP=<bu kompüterin IP-si>"

REM ---- URL-lar ----
echo ================================================
echo  Server ise dushur...
echo.
echo  Bu kompuuterde:
echo    http://127.0.0.1:5001
echo.
echo  Basqa kompuuterden:
echo    http://!LAN_IP!:5001
echo.
echo  ILK DEFE: Windows Firewall pop-up cixarsa "Allow"
echo  QEYD: Basqa kompuuterlere port 5001 acilmalidir
echo        (Windows Firewall -^> Inbound Rules -^> New Rule -^> TCP 5001)
echo.
echo  Dayandirmaq ucun: Ctrl+C
echo ================================================
echo.

REM Brauzeri arxa fonda ac (server hazir olsun deye 4 saniye gozle)
start "" /min powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep 4; Start-Process 'http://127.0.0.1:5001'"

python app.py

echo.
pause
