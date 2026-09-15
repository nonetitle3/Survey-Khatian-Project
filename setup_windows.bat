@echo off
setlocal
python --version >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Install Python 3.12+ 64-bit and enable Add Python to PATH.
  pause
  exit /b 1
)
for /f "tokens=2" %%V in ('python -c "import platform; print(platform.architecture()[0])"') do set ARCH=%%V
if not "%ARCH%"=="64bit" echo WARNING: Python is not 64-bit. A 64-bit build is recommended.
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
python -m pip install --only-binary=:all: -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed without binary wheels.
  echo Use a supported 64-bit Python version and run setup_windows.bat again.
  pause
  exit /b 1
)
echo Setup complete.
pause
