@echo off
REM ==============================================================
REM  Ehtiyat hisseleri - Windows launcher
REM  Ilk defe: virtual environment qurur + asililiqlari install edir
REM  Sonrakilar: birbaşa serveri qaldirir
REM  Ise salmaq ucun: bu fayla iki defe klik edin
REM ==============================================================

setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo.
echo ================================================
echo  Ehtiyat hisseleri
echo ================================================
echo.

REM ---- Python komandasi tapilir ----
REM Windows-da bezen "python" PATH-de olmur, amma "py" (Python Launcher) olur.
REM Her ikisini yoxlayirq, hansi isleyirse onu istifade edirik.
set "PY="

py -3.7 --version >nul 2>&1
if not errorlevel 1 (
    set "PY=py -3.7"
    goto :py_found
)

py --version >nul 2>&1
if not errorlevel 1 (
    set "PY=py"
    goto :py_found
)

python --version >nul 2>&1
if not errorlevel 1 (
    set "PY=python"
    goto :py_found
)

echo [XETA] Python tapilmadi.
echo.
echo Python 3.7.9 endirin ve "Add Python to PATH" secerek qurun:
echo   https://www.python.org/ftp/python/3.7.9/python-3.7.9.exe
echo.
pause
exit /b 1

:py_found
echo [INFO] Python komandasi: !PY!
!PY! --version
echo.

REM ---- venv yoxdursa yaradilir + deps install olunur ----
if not exist "venv\Scripts\activate.bat" (
    echo [SETUP] Ilk defe qurulur, 2-5 deqiqe cekebilir...
    echo.
    !PY! -m venv venv
    if errorlevel 1 (
        echo.
        echo [XETA] Virtual environment yaradila bilmedi.
        pause
        exit /b 1
    )

    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip

    echo [SETUP] Asililiqlar install olunur...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [XETA] pip install ugursuz oldu.
        echo.
        echo TLS / SSL problemi ola biler. Beleliki elle sinayin:
        echo   venv\Scripts\activate
        echo   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [SETUP] Asililiqlar qurashdi.
    echo.
) else (
    call venv\Scripts\activate.bat
)

REM ---- .env yoxdursa .env.example-den yaradilir ----
if not exist ".env" (
    if exist ".env.example" (
        copy /y .env.example .env >nul
        echo [SETUP] .env fayli .env.example-den yaradildi.
        echo.
    )
)

REM ---- Server qaldirilir ----
echo ================================================
echo  Server ise dushur...
echo  Brauzerde acin: http://127.0.0.1:5001
echo  Dayandirmaq ucun bu pencerede: Ctrl+C
echo ================================================
echo.
python app.py

REM Ctrl+C ile bitse pencere avtomatik baglanmasin
echo.
pause
