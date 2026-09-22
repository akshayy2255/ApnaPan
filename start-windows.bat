@echo off
REM ApnaPan - double-click to run the site locally.
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
  python serve.py 8000
) else (
  where py >nul 2>nul
  if %errorlevel%==0 (
    py serve.py 8000
  ) else (
    echo Python 3 is not installed. Get it from https://python.org/downloads
    echo Or, with Node.js installed, run:  npx --yes serve -l 8000 .
    pause
  )
)
