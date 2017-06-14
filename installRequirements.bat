@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
set path_var=%PATH%
set requirements=%1

:: Check if Python exists in PATH
echo %path_var% | findstr /C:"Python" 1>nul

:: No argument provided - show file Usage
if [%1]==[] goto :usage

:: Process each line of text file
for /f "tokens=*" %%a in (%requirements%) do call :processline %%a

pause
goto :eoc

:processline
echo.
echo Installing %*...
echo.
call pip install %*

goto :eoc

:eoc

goto :eof

:: Script usage displayed if no argument is supplied
:usage
@echo.
@echo Usage: %0 ^<requirements-file^>
@echo.
@echo The requirements file should be a text file containing each required Python library on each line.
@echo.
exit /B 1

:eof
exit /B 1