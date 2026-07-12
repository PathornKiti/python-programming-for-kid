@echo off
REM One-time setup for Py's Python Adventure (Windows).
REM
REM A grown-up double-clicks this ONCE on a new computer. It:
REM   1. Checks whether Python is installed (and helps install it if not).
REM   2. Builds the .venv virtual environment and installs the lesson tools.
REM   3. Offers to open the lessons right away.
REM
REM Note: Windows does not come with `make`, and kids don't need it here --
REM this script does everything `make setup` would do, without make.

setlocal
echo.
echo === Py's Python Adventure - setup ===
echo.

REM ------------------------------------------------------------ 1. Python
where python >nul 2>&1
if %ERRORLEVEL%==0 (
    echo [OK] Python is already installed
    python --version
    goto :venv
)

echo [!] Python is not installed on this computer.
where winget >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Installing Python with winget...
    winget install -e --id Python.Python.3.12
    echo.
    echo Python was installed. Please CLOSE this window, open a new one,
    echo and run setup.bat again to finish.
    pause
    exit /b 1
) else (
    echo Please install Python from https://www.python.org/downloads/
    echo During install, TICK the box "Add Python to PATH".
    echo Then run setup.bat again.
    pause
    exit /b 1
)

REM -------------------------------------------------- 2. venv + lesson tools
:venv
echo.
echo Building the virtual environment (.venv) and installing lesson tools...
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt

echo.
echo === All done! ===
echo To start the lessons, run this from the same folder:
echo     .venv\Scripts\jupyter notebook
echo.

set /p reply="Open the lessons now? [Y/n] "
if /I "%reply%"=="n" (
    echo Okay! Run the command above whenever you're ready.
) else (
    .venv\Scripts\jupyter notebook
)

endlocal
pause
