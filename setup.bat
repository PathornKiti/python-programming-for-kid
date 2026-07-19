@echo off
REM Optional grown-up helper for Windows.
REM It never installs Python or system tools. It only checks what is present,
REM then builds the lesson toolbox.

setlocal
echo.
echo === Py's Python Adventure - setup checker ===
echo.

py -3 --version >nul 2>nul
if %ERRORLEVEL%==0 (
    echo [OK] Python is ready
    py -3 --version
) else (
    echo [!] Python 3 was not found.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo IMPORTANT: tick "Add python.exe to PATH" during install.
    echo Then open a new Command Prompt in this folder and run: setup.bat
    pause
    exit /b 1
)

echo.
echo Building the lesson toolbox in .venv...
py -3 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt

echo.
echo === All done! ===
echo Student start command:
echo     .venv\Scripts\jupyter notebook lessons\00_welcome\00_welcome.ipynb
echo If your computer has make, you can also run:
echo     make start
echo.

set /p reply="Open the welcome lesson now? [Y/n] "
if /I "%reply%"=="n" (
    echo Okay! Use the start command above whenever you're ready.
) else (
    .venv\Scripts\jupyter notebook lessons\00_welcome\00_welcome.ipynb
)

endlocal
pause
