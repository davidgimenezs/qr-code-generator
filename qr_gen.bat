@echo off
REM SVG QR Code Generator - Windows Batch Script
REM Usage: qr_gen.bat "Your data here" output.svg

setlocal

REM Check if Python virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found.
    echo Please run the setup first or ensure Python is installed.
    pause
    exit /b 1
)

REM Set the Python executable path
set PYTHON_EXE=.venv\Scripts\python.exe

REM Check if at least one argument is provided
if "%~1"=="" (
    echo.
    echo SVG QR Code Generator
    echo ====================
    echo.
    echo Usage: %~n0 "data" [output.svg] [logo.png]
    echo.
    echo Examples:
    echo   %~n0 "https://github.com"
    echo   %~n0 "Hello World" my_qr.svg
    echo   %~n0 "https://example.com" branded_qr.svg logo.png
    echo.
    echo For interactive mode, run: %PYTHON_EXE% interactive_guide.py
    echo For full help, run: %PYTHON_EXE% qr_generator.py --help
    echo.
    pause
    exit /b 1
)

REM Build the command
set QR_COMMAND=%PYTHON_EXE% qr_generator.py "%~1"

REM Add output file if provided
if not "%~2"=="" (
    set QR_COMMAND=%QR_COMMAND% -o "%~2"
)

REM Add logo if provided
if not "%~3"=="" (
    set QR_COMMAND=%QR_COMMAND% -l "%~3"
)

REM Run the command
echo Generating QR code...
%QR_COMMAND%

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ QR code generated successfully!
) else (
    echo.
    echo ❌ Error generating QR code.
)

echo.
pause
