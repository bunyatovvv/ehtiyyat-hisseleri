@echo off
REM ==============================================================
REM  Ehtiyat hisseleri - Windows launcher
REM  Ilk defe: virtual environment qurur + asililiqlari install edir
REM  Sonrakilar: birbaşa serveri qaldirir
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

REM ---- venv olub olmadigini yoxla ----
if exist "venv\Scripts\activate.bat" goto :venv_exists

REM ---- Method 1: standart venv ----
echo [SETUP] Method 1: standart venv sinayiriq...
!PY! -m venv venv
if not errorlevel 1 goto :venv_created

REM Ugursuz oldu — kohne yarim qovluq varsa temizle
if exist "venv" rmdir /s /q venv

REM ---- Method 2: --without-pip + ensurepip ----
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

REM ---- Method 3: virtualenv paketi ----
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
echo ================================================
echo [XETA] Virtual environment 3 metodda da yaradila bilmedi.
echo ================================================
echo.
echo Muhtemel sebebler:
echo   1. Antivirus bloklayir (Windows Defender / avast / kaspersky)
echo      -^> Antivirusu bu qovluq ucun mueyyet mueddet sondururn
echo.
echo   2. Qovluq yolunda Azerbaycan herfleri (o, e, u, i, ə...) var
echo      -^> Layiheni yalniz Latin herfli qovluqda saxlayin:
echo         mes: C:\zapcast   ve ya  C:\parts
echo.
echo   3. Python yalniz "Just for me" quraşdirilib
echo      -^> Python-u yenidən qurun, bu defe "Install for all users" secin
echo.
echo   4. Disk oxumaga icaze yoxdur
echo      -^> Layiheni Documents ve ya Desktop-da saxlayin
echo.
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
        echo.
        echo [WARN] pip install ugursuz oldu, --trusted-host ile sinayiriq...
        pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
        if errorlevel 1 (
            echo.
            echo [XETA] pip install nə birinci, nə də ikinci variantda islemedi.
            pause
            exit /b 1
        )
    )
    echo.
    echo [SETUP] Asililiqlar qurashdi.
    echo.
)

REM ---- .env ----
if not exist ".env" (
    if exist ".env.example" (
        copy /y .env.example .env >nul
        echo [SETUP] .env fayli yaradildi.
        echo.
    )
)

REM ---- Server ----
echo ================================================
echo  Server ise dushur...
echo  URL: http://127.0.0.1:5001
echo  Brauzer avtomatik acilacaq (4 sn sonra).
echo  Dayandirmaq ucun: Ctrl+C
echo ================================================
echo.

REM Brauzeri arxa fonda ac (server hazir olsun deye 4 saniye gozle).
REM Default brauzer istifade olunur — Chrome default-dursa Chrome-da acilir.
start "" /min powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep 4; Start-Process 'http://127.0.0.1:5001'"

python app.py

echo.
pause
